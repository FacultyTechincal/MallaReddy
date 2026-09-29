import os
import hashlib
import requests
import streamlit as st

from langchain_community.document_loaders import TextLoader,PyPDFLoader,CSVLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db" not in st.session_state:
    st.session_state.db = None
if "file_hash" not in st.session_state:
    st.session_state.file_hash = None
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
os.makedirs("uploaded_files", exist_ok=True)
os.makedirs("embedding_db", exist_ok=True)
embedding = OllamaEmbeddings(
    model="nomic-embed-text:v1.5"
)
with st.sidebar:
    st.header("⚙️ Settings")
    chunk_size = st.slider(
        "Chunk Size",
        min_value=500,
        max_value=5000,
        value=2000,
        step=500
    )
    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=0,
        max_value=1000,
        value=200,
        step=100
    )
    k = st.slider(
        "Number of Retrieved Chunks",
        min_value=1,
        max_value=10,
        value=3
    )

uploaded_file = st.file_uploader(
    "Upload the document",
    type=["pdf", "csv", "txt", "docx"]
)
if uploaded_file:
    if st.button("Process Document"):
        uploaded_name = uploaded_file.name
        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(
            file_bytes
        ).hexdigest()
        extension = os.path.splitext(
            uploaded_name
        )[1].lower()
        filename = file_hash + extension

        file_path = os.path.join(
            "uploaded_files",
            filename
        )
        st.session_state.file_hash = file_hash
        if os.path.exists(file_path):
            st.info(
                "This exact document was already uploaded."
            )
            st.session_state.document_processed = True
            db = Chroma(
                persist_directory="./embedding_db",
                embedding_function=embedding
            )
            st.session_state.db = db
        else:
            st.info(
                "New document detected. Processing..."
            )
            with open(file_path, "wb") as file:
                file.write(file_bytes)
            if extension == ".pdf":
                loader = PyPDFLoader(
                    file_path
                )
            elif extension == ".txt":
                loader = TextLoader(
                    file_path,
                    encoding="utf-8"
                )
            elif extension == ".csv":
                loader = CSVLoader(
                    file_path
                )
            elif extension == ".docx":
                loader = Docx2txtLoader(
                    file_path
                )
            else:
                st.error(
                    "Unsupported file type."
                )
                st.stop()
            doc = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            document = splitter.split_documents(
                doc
            )
            for item in document:
                item.metadata["file_hash"] = file_hash
                item.metadata["file_name"] = uploaded_name
            db = Chroma(
                persist_directory="./embedding_db",
                embedding_function=embedding
            )
            db.add_documents(
                document
            )
            st.session_state.db = db
            st.session_state.document_processed = True
            st.success(
                "Document embedded successfully."
            )

for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )
question = st.chat_input(
    "Enter your question"
)
if question:
    if st.session_state.db is None:
        st.warning(
            "Please upload and process a document first."
        )
        st.stop()
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    with st.chat_message("user"):

        st.write(question)
    retriever = st.session_state.db.as_retriever(
        search_kwargs={
            "k": k
        }
    )
    result = retriever.invoke(
        question
    )
    context = ""
    for document in result:
        context += (
            document.page_content
            + "\n\n"
        )
    prompt = f"""
    Answer the question using ONLY the context below.

    If the answer is not available in the context,
    say that the information is not available
    in the uploaded document.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """
    urls = "https://ollama.com/api/chat"
    header = {
        "Authorization": "Bearer YOUR_API_KEY"
    }
    data = {
        "model": "gpt-oss:20b-cloud",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    response = requests.post(
        url=urls,
        headers=header,
        json=data
    )
    ans = response.json()
    answer = ans["message"]["content"]
    with st.chat_message("assistant"):
        st.write(answer)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
# loading the document
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
#Loading completed
embedding = OllamaEmbeddings(model = "nomic-embed-text:v1.5")
from langchain_chroma import Chroma
if os.path.exists('embedding_db'):
    print("This is executing")
    db = Chroma(
        persist_directory="./embedding_db",
        embedding_function= embedding
    )
else:
    pdf = PyPDFLoader("Accouting.pdf")
    doc = pdf.load()
    print("Currently here")
    # Splitting the text 
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size= 2000, chunk_overlap= 0)
    document = splitter.split_documents(doc)
    # Splitting Completed
    #Embedding model
    #Created Embedding model 

    #Embedding ans storing in vector database

    db = Chroma.from_documents(
        embedding = embedding,
        persist_directory="./embedding_db",
        documents= document
    )
    # Created embedding
#Retriving the relavent documents
retriver = db.as_retriever(
    search_kwargs={"k": 3}
)
query = "What is accounting?"
result = retriver.invoke(query)
context =""
for i in result:
    context += (str(i.page_content)+str("\n\n"))

#developing prompt
prompt = f"""
context: {context}
question: {query}"""
#Sending to the llm
from langchain_ollama import ChatOllama
llm = ChatOllama(model = "gemma4:e2b")
llm.invoke(prompt)

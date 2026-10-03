import streamlit as st
import whisper
from ollama import chat, Client
from  huggingface_hub import InferenceClient
import os
import uuid
os.makedirs("Images", exist_ok=True)
client1 = InferenceClient(
    api_key="Your_HuggingFace_API_Key"
)
client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": "Your_Ollama_API_Key"
    }
)

model = whisper.load_model("base")
audio_input = st.audio_input("Speak:")
if "transcribe" not in st.session_state:
    st.session_state.transcribe = ""
if "message" not in st.session_state:
    st.session_state.message = []
if audio_input:
    audio_bytes = audio_input.getvalue()
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)
    transcribe = model.transcribe("audio.wav")
    st.session_state.transcribe = transcribe["text"]
question = st.text_input("Ask me anything:", value=st.session_state.transcribe)
generate_image = st.toggle("Generate Image")
if question:
    Message = {
        "role": "user",
        "content": question
    }
    st.session_state.message.append(Message)
    answer = client.chat(
        model="gemma4:31b",
        messages=st.session_state.message
    )
    Answer ={
        "role": "assistant",
        "content": answer.message.content
    }
    if generate_image:
        image = client1.text_to_image(model="black-forest-labs/FLUX.1-dev", prompt=answer.message.content)
        image_name= "Image_" + uuid.uuid4().hex
        image_path = os.path.join("Images", image_name + ".png")
        image.save(image_path)
        st.image(image_path, caption="Generated Image")
        Answer["image"]= image_path
    st.session_state.message.append(Answer)
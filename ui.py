import streamlit as st
import requests
choice = st.sidebar.radio("Give me the agent tone",["Expert", "Friendly", "Short"])
st.title("🕵️‍♀️ ChatBot", text_alignment="center")
if "messages" not in st.session_state:
    st.session_state.messages = None
if "tone" not in st.session_state:
    st.session_state.tone = choice
urls = "https://ollama.com/api/chat"
header = {
    "Authorization" : "Bearer 3896419029b24aa4bfa7654a5f852bd5.AWq-ctbnHwsB0dbAvqwA1lrV"
}
if st.session_state.messages!=None:
    for i in st.session_state.messages['messages']:
        if i["role"] == "user":
            with st.chat_message("user"):
                st.write(i["content"])
        if i["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(i["content"])
if choice =="Expert":
    data = {
    "model": "gpt-oss:20b-cloud",
    "messages": [{"role": "system", "content": "Consider your self as the expert of the domian given in the question and answer the question in a very detailed manner"}],
    "stream": False
  }
    st.session_state.messages = data
elif choice=="Friendly":
    data = {
        "model": "gpt-oss:20b-cloud",
        "messages": [{"role": "system", "content": "Answer the question in a very short formate within 100 words"}],
        "stream": False
      }
    st.session_state.messages = data
elif choice== "Short":
    data = {
        "model": "gpt-oss:20b-cloud",
        "messages": [{"role": "system", "content": "Gvie the answer in a friendly way along with lot of examples"}],
        "stream": False
      }
    st.session_state.messages = data

question = st.chat_input("Enter the question")
if question:
    with st.chat_message("user"):
        st.write(question)
    data["messages"].append({
            "role":"user",
            "content":f"{question}"
    })
    response = requests.post(url=urls,headers=header, json = st.session_state.messages)
    ans = response.json()
    with st.chat_message("assistant"):
        st.write(ans["message"]["content"])
    data["messages"].append({
                "role":"assistant",
                "content": ans["message"]["content"]
        })
    
    
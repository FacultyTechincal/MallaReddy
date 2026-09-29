import requests

choice = int(input("""Enter you choice Type:
1-> if you want answers in a detailed way
2-> if you want answers in a shot way
3-> if you want answers in a friendly tone with lot of examples\n"""))

urls = "https://ollama.com/api/chat"
header = {
    "Authorization" : "Bearer 3896419029b24aa4bfa7654a5f852bd5.AWq-ctbnHwsB0dbAvqwA1lrV"
}
if choice ==1:
    data = {
    "model": "gpt-oss:20b-cloud",
    "messages": [{"role": "system", "content": "Consider your self as the expert of the domian given in the question and answer the question in a very detailed manner"}],
    "stream": False
  }
elif choice==2:
    data = {
        "model": "gpt-oss:20b-cloud",
        "messages": [{"role": "system", "content": "Answer the question in a very short formate within 100 words"}],
        "stream": False
      }
elif choice== 3:
    data = {
        "model": "gpt-oss:20b-cloud",
        "messages": [{"role": "system", "content": "Gvie the answer in a friendly way along with lot of examples"}],
        "stream": False
      }
while True:#why not to write while true
    question = input("Enter the question\n")
    if question == "exit":
        break
    data["messages"].append({
        "role":"user",
        "content":f"{question}"
    })
    response = requests.post(url=urls,headers=header, json = data)
    ans = response.json()
    print(ans["message"]["content"])
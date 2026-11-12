import requests
import json

URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"
messages = []

print(f"Chatting with {MODEL} via REST API. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }

    print("Gemma: ", end="", flush=True)
    full_reply = ""

    # Send POST request and stream the JSON lines response
    with requests.post(URL, json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_reply += content
    print("\n")

    messages.append({"role": "assistant", "content": full_reply})


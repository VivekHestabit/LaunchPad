import requests
import sys
import uuid

API_URL_CHAT = "http://localhost:8000/chat"

SYSTEM_PROMPT = (
    "You are a helpful medical assistant. "
    "Answer medical questions accurately and safely. "
    "Answer using clear bullet points."
)


def single_prompt_mode(prompt: str):
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "top_k": 40
    }

    response = requests.post(API_URL_CHAT, json=payload)

    if response.status_code == 200:
        print("\n--- Assistant ---")
        print(response.json()["assistant_reply"])
    else:
        print("Error communicating with backend")


def interactive_chat_mode():
    print("\n🩺 Medical LLM CLI")
    print("Type 'exit' to quit.\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        payload = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.9,
            "top_k": 40
        }

        response = requests.post(API_URL_CHAT, json=payload)

        if response.status_code == 200:
            reply = response.json()["assistant_reply"]
            print("\n--- Assistant ---")
            print(reply + "\n")

            messages.append({"role": "assistant", "content": reply})
        else:
            print("Error communicating with backend")


# ===================== ENTRY POINT =====================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        single_prompt_mode(prompt)
    else:
        interactive_chat_mode()

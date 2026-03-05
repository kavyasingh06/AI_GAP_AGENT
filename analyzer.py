import os
import requests

# 🔐 Get Hugging Face Token
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found. Please set it in your environment variables.")

# ✅ NEW Hugging Face Router Endpoint
MODEL_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def analyze_question(user_input):

    payload = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful and intelligent Study Mentor AI. Explain clearly and simply."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()
    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Study Mentor AI Started ✅")

    user_input = input("Enter your question: ")
    answer = analyze_question(user_input)

    print("\nAI Response:\n")
    print(answer)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_ai_overview_urls(keyword):

    api_key = os.getenv("SERP_API_KEY")

    url = "https://google.serper.dev/search"

    payload = {
        "q": keyword,
        "gl": "in",
        "hl": "en"
    }

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        data = response.json()

        ai_urls = []

        if "organic" in data:
            for result in data["organic"][:5]:
                ai_urls.append(result["link"])

        return ai_urls

    except Exception as e:
        print("SERP API Error:", e)
        return []
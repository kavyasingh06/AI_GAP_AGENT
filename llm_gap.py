import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def generate_gap_analysis(ai_sources, client_article):

    prompt = f"""
You are an SEO content strategist.

Compare AI Overview source articles with the client article.

AI SOURCE CONTENT:
{json.dumps(ai_sources)}

CLIENT ARTICLE:
{json.dumps(client_article)}

Tasks:
1. Identify content format differences
2. Identify structural gaps
3. Identify missing sections
4. Provide 3-5 actionable recommendations

Return JSON format:

{{
"gap_summary": "...",
"missing_elements": [],
"recommendations": []
}}
"""

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an SEO expert analyzing content gaps."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 600,
        "temperature": 0.4
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]

    return result

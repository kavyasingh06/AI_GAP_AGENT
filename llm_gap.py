import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def summarize_sources(ai_sources):

    summary = []

    for src in ai_sources:
        summary.append({
            "url": src.get("url"),
            "word_count": src.get("word_count"),
            "h2_count": src.get("headings", {}).get("h2", 0),
            "h3_count": src.get("headings", {}).get("h3", 0),
            "has_faq": src.get("has_faq"),
            "has_table": src.get("has_table"),
            "has_list": src.get("has_list")
        })

    return summary


def generate_gap_analysis(ai_sources, client_article):

    ai_summary = summarize_sources(ai_sources)

    client_summary = {
        "word_count": client_article.get("word_count"),
        "h2_count": client_article.get("headings", {}).get("h2", 0),
        "h3_count": client_article.get("headings", {}).get("h3", 0),
        "has_faq": client_article.get("has_faq"),
        "has_table": client_article.get("has_table"),
        "has_list": client_article.get("has_list")
    }

    prompt = f"""
You are an SEO content strategist analyzing Google AI Overview sources.

AI SOURCE SUMMARY:
{json.dumps(ai_summary, indent=2)}

CLIENT ARTICLE SUMMARY:
{json.dumps(client_summary, indent=2)}

Tasks:
1. Identify content format differences
2. Identify structural gaps
3. Identify missing elements
4. Provide 3-5 actionable recommendations

Return STRICT JSON format:

{{
"gap_summary": "...",
"missing_elements": [],
"recommendations": []
}}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.3
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return {"error": response.text}

        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

        return result

    except Exception as e:
        return {"error": str(e)}
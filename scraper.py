import requests
from bs4 import BeautifulSoup

def scrape_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20,
            verify=False  # ignore SSL issues (demo only)
        )

        # ✅ Check for successful response
        if response.status_code != 200:
            return {
                "url": url,
                "error": f"HTTP {response.status_code}"
            }

        # ✅ Skip PDFs or non-HTML content
        content_type = response.headers.get("Content-Type", "")

        if "application/pdf" in content_type:
            return {
                "url": url,
                "word_count": 0,
                "headings": {},
                "has_faq": False,
                "has_table": False,
                "has_list": False,
                "raw_text": "PDF skipped"
            }

        if "text/html" not in content_type:
            return {
                "url": url,
                "error": f"Unsupported content type: {content_type}"
            }

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        clean_text = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )

        headings = {
            "h1": len(soup.find_all("h1")),
            "h2": len(soup.find_all("h2")),
            "h3": len(soup.find_all("h3")),
        }

        word_count = len(clean_text.split())
        has_faq = "faq" in clean_text.lower()
        has_table = bool(soup.find_all("table"))
        has_list = bool(soup.find_all(["ul", "ol"]))

        return {
            "url": url,
            "word_count": word_count,
            "headings": headings,
            "has_faq": has_faq,
            "has_table": has_table,
            "has_list": has_list,
            "raw_text": clean_text[:5000]  # limit text for LLM
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }
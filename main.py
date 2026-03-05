import argparse
from serp_api import get_ai_overview_urls
from scraper import scrape_content
from llm_gap import generate_gap_analysis
import json


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--client_url", required=True)

    args = parser.parse_args()

    print("Fetching AI Overview URLs...")
    ai_urls = get_ai_overview_urls(args.keyword)

    # remove youtube links
    ai_urls = [url for url in ai_urls if "youtube.com" not in url]

    print("Scraping AI sources...")
    ai_data = []

    for url in ai_urls:
        try:
            data = scrape_content(url)
            if data:
                ai_data.append(data)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    if not ai_data:
        print("No AI sources scraped successfully.")
        return

    print("Scraping client article...")
    client_data = scrape_content(args.client_url)

    print("Generating gap analysis...")
    gap_report = generate_gap_analysis(ai_data, client_data)

    final_output = {
        "keyword": args.keyword,
        "ai_overview_urls": ai_urls,
        "ai_analysis": ai_data,
        "client_analysis": client_data,
        "gap_analysis": gap_report
    }

    with open("output_report.json", "w") as f:
        json.dump(final_output, f, indent=4)

    print("Report generated: output_report.json")


if __name__ == "__main__":
    main()
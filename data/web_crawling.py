"""
crawl_women_running_shoes.py

Description:
    Crawl women's running shoe pages from a target brand website,
    extract clean text content, chunk the content,
    and save everything into a JSON dataset ready for agent optimization.

Requirements:
    pip install apify-client markdownify requests

Environment:
    export APIFY_API_TOKEN="YOUR_TOKEN"

Usage:
    python crawl_women_running_shoes.py
"""

import os
import json
import time
from typing import List, Dict
from apify_client import ApifyClient
import markdownify


# ===============================
# 1. Chunking function
# ===============================
def chunk_text_for_agent(text: str, max_chunk_chars: int = 1200) -> List[str]:
    """Split long text into manageable chunks for downstream agent use."""
    chunks = []
    current = ""
    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) + 1 <= max_chunk_chars:
            current += paragraph + "\n"
        else:
            if current:
                chunks.append(current.strip())
            current = paragraph + "\n"
    if current:
        chunks.append(current.strip())
    return chunks


# ===============================
# 2. Web Crawler (Apify)
# ===============================
def crawl_womens_running_shoes(
    start_url: str,
    max_pages: int = 1,
    include_url_globs: List[str] = None,
    exclude_url_globs: List[str] = None,
    crawler_type: str = "cheerio",
    output_json: str = "women_running_shoes_dataset.json"
) -> List[Dict]:
    """
    Crawl a women’s running shoes category and extract clean text pages.

    Args:
        start_url (str): Female running shoes catalog page.
        max_pages (int): Max number of pages to crawl.
        include_url_globs (List[str]): Limit crawling to product pages.
        exclude_url_globs (List[str]): Exclude non-product URLs.
        crawler_type (str): "cheerio" or "playwright:adaptive".
        output_json (str): Name of JSON output file.

    Returns:
        List[Dict]: List of scraped product pages with clean text + chunks.
    """

    api_key = os.getenv("APIFY_API_TOKEN", 'Mask')
    if not api_key:
        raise ValueError("Missing APIFY_API_TOKEN environment variable.")

    client = ApifyClient(api_key)

    include_url_globs = include_url_globs or ["/women/", "/running", "/shoe", "/product"]
    exclude_url_globs = exclude_url_globs or ["/cart", "/login", "/sale"]

    run_input = {
        "startUrls": [{"url": start_url}],
        "maxCrawlPages": max_pages,
        "crawlerType": crawler_type,
        "useSitemaps": False,
        "includeUrlGlobs": include_url_globs,
        "excludeUrlGlobs": exclude_url_globs,
        "removeElementsCssSelector": "nav, footer, script, style",
        # Anti-bot bypass options
        "proxyConfiguration": {"useApifyProxy": True},
        "maxRequestRetries": 3,
        "requestHandlerTimeoutSecs": 60,
        # For playwright:adaptive - more browser-like behavior
        "headless": True,
        "waitUntil": "networkidle",
    }

    print("🚀 Launching Apify Website Content Crawler...")
    actor_call = client.actor("apify/website-content-crawler").call(run_input=run_input)

    dataset_id = actor_call["defaultDatasetId"]
    time.sleep(5)

    items = client.dataset(dataset_id).list_items(limit=max_pages).items

    output = []
    for it in items:
        url = it.get("url")
        title = it.get("metadata", {}).get("title", "")

        # Markdown prioritization
        markdown = it.get("markdown")
        if not markdown:
            markdown = markdownify.markdownify(it.get("text", ""), heading_style="ATX")

        text = it.get("text", "") or markdown

        entry = {
            "url": url,
            "title": title,
            "text": text,
            "chunks": chunk_text_for_agent(text, max_chunk_chars=1200),
            "metadata": {
                "depth": it.get("crawl", {}).get("depth"),
                "status": it.get("crawl", {}).get("httpStatusCode"),
            },
        }

        output.append(entry)

    # Save JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Done! Crawled {len(output)} pages.")
    print(f"Saved dataset to: {output_json}")

    return output


# ===============================
# 3. Run Script
# ===============================
if __name__ == "__main__":
    # EXAMPLE START URL (replace with real brand URL)
    START_URL = "https://www.newbalance.com/pd/tag-heuer-x-new-balance-sc-elite-v5/WRCELV5-51975.html?dwvar_WRCELV5-51975_style=WRCELTG5"

    crawl_womens_running_shoes(
        start_url=START_URL,
        max_pages=1,
        include_url_globs=["/women", "/running", "/shoe", "/product", "newbalance"],
        exclude_url_globs=["/cart", "/login", "/search"],
        crawler_type="cheerio",
        output_json="women_running_shoes_dataset.json"
    )

# This script will be prepared for GitHub Actions to:
# 1. Pull MST news articles from a global RSS feed system using NewsCatcher.
# 2. Format headlines with hashtags and sources.
# 3. Shorten links using an open TinyURL alternative.
# 4. Post the headline and link directly to Bluesky via API.

import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# === CONFIGURATION ===
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

# Replace this with the actual URL once integrated
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=military+sexual+trauma",
    "https://news.google.com/rss/search?q=army+sexual+assault",
    "https://news.google.com/rss/search?q=navy+MST",
    "https://news.google.com/rss/search?q=coast+guard+MST",
    "https://news.google.com/rss/search?q=air+force+MST"
]

HASHTAGS = "#MST #MilitarySexualTrauma #SilencedVoices"

# === UTILITIES ===
def shorten_url(long_url):
    try:
        res = requests.get("https://cleanuri.com/api/v1/shorten", params={"url": long_url})
        return res.json().get("result_url", long_url)
    except:
        return long_url

def extract_articles(feed_url):
    try:
        feed = requests.get(feed_url, timeout=10)
        soup = BeautifulSoup(feed.content, features="xml")
        items = soup.findAll('item')
        return [
            {
                "title": item.title.text.strip(),
                "link": item.link.text.strip(),
                "source": feed_url.split("?")[0].replace("https://", "").replace("www.", "")
            }
            for item in items
        ]
    except Exception as e:
        return []

def post_to_bluesky(session, text):
    # Placeholder for actual Bluesky post using lexicons
    print(f"Would post: {text[:60]}...")
    # You must use the bsky.py library in production here

# === MAIN SCRIPT ===
def run():
    seen = set()
    for feed_url in RSS_FEEDS:
        articles = extract_articles(feed_url)
        for article in articles:
            key = article["link"]
            if key in seen:
                continue
            seen.add(key)
            short_url = shorten_url(article["link"])
            post_text = f"{article['title']}\n{HASHTAGS}\n{short_url}"
            if len(post_text) > 300:
                cutoff = 280 - len(HASHTAGS) - len(short_url) - 4
                truncated_title = article['title'][:cutoff] + "..."
                post_text = f"{truncated_title}\n{HASHTAGS}\n{short_url}"
            post_to_bluesky(None, post_text)

if __name__ == "__main__":
    run()

import requests
from bs4 import BeautifulSoup

import os
from atproto import Client

# Keywords for the news search
KEYWORDS = [
    "military sexual trauma",
    "male victims of MST",
    "Air Force MST",
    "Army MST",
    "Navy MST",
    "Coast Guard MST",
    "Marine Corps MST",
    "MST court martial",
    "military sexual harassment"
]

# Initialize Bluesky client
HANDLE = 'silencedvoicesmst.bsky.social'
PASSWORD = os.getenv('BLUESKY_PASSWORD')

if not PASSWORD:
    print("ERROR: No password found in environment.")
    exit(1)

client = Client()
try:
    client.login(HANDLE, PASSWORD)
    print("Login to Bluesky successful.")
except Exception as e:
    print(f"Login failed: {e}")
    exit(1)

# Get latest news articles
def get_news():
    articles = []
    for keyword in KEYWORDS:
        print(f"Searching for keyword: {keyword}")
        url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features='xml')
        items = soup.findAll('item')
        for item in items[:1]:  # Limit to 1 per keyword
            title = item.title.text
            link = item.link.text
            articles.append(f"{title}\n{link}")
    return articles

# Post to Bluesky
posts = get_news()

if not posts:
    print("No posts found to share.")
else:
    for post in posts:
        try:
            client.send_post(post)
            print(f"Posted: {post[:60]}...")
        except Exception as e:
            print(f"Error posting: {e}")

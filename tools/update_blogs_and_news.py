# tools/scripts/update_blogs_and_news.py

import datetime
import requests
import xml.etree.ElementTree as ET

# Target file path
FILE_PATH = "tools/blogs-and-news.md"

# RSS feed for Google News on AI
RSS_FEED_URL = "https://news.google.com/rss/search?q=AI&hl=en-US&gl=US&ceid=US:en"

# Keywords to search for
KEYWORDS = [
    # Major AI Companies
    "OpenAI", "Anthropic", "Google AI", "Microsoft AI", "Meta AI", "DeepMind", "Stability AI", "Midjourney", "Cohere",
    # Popular AI Models
    "ChatGPT", "Claude", "GPT-4", "DALL-E", "Stable Diffusion", "Gemini", "Llama", "Mistral", "Falcon",
    # AI Technologies & Concepts
    "AI tools", "AI news", "Machine Learning", "Deep Learning", "Neural Networks", "Large Language Models", "LLMs",
    "Generative AI", "Computer Vision", "Natural Language Processing", "NLP", "AI Ethics", "AI Safety",
    "Prompt Engineering", "Fine-tuning", "RAG", "Vector Databases", "AI Agents", "Multimodal AI",
    # AI Applications
    "AI Assistant", "AI Chatbot", "AI Image Generation", "AI Video Generation", "AI Audio Generation",
    "AI Code Generation", "AI Writing", "AI Translation", "AI Research", "AI Development",
    # Industry Terms
    "AGI", "Artificial General Intelligence", "Narrow AI", "Supervised Learning", "Unsupervised Learning",
    "Reinforcement Learning", "Transfer Learning", "Few-shot Learning", "Zero-shot Learning"
]

# Helper to fetch news from a Google News RSS feed URL
def fetch_rss_items(feed_url):
    res = requests.get(feed_url)
    if res.status_code != 200:
        return []
    root = ET.fromstring(res.content)
    items = root.findall(".//item")
    news_items = []
    for item in items:
        title = item.find("title").text or ""
        link = item.find("link").text
        news_items.append((title, link))
    return news_items

# Fetch from main AI RSS feed
main_rss_news = fetch_rss_items(RSS_FEED_URL)

# Fetch from per-keyword Google News RSS feeds
keyword_news = []
for kw in KEYWORDS:
    kw_url = f"https://news.google.com/rss/search?q={requests.utils.quote(kw)}&hl=en-US&gl=US&ceid=US:en"
    keyword_news.extend(fetch_rss_items(kw_url))

# Combine and deduplicate (by link)
all_news = main_rss_news + keyword_news
seen_links = set()
unique_news = []
for title, link in all_news:
    if link not in seen_links:
        unique_news.append((title, link))
        seen_links.add(link)
    if len(unique_news) >= 10:
        break

# Read existing content
try:
    with open(FILE_PATH, "r") as f:
        existing = f.read()
except FileNotFoundError:
    existing = "# 🔗 Blog Posts / News Articles\n"

# Format today's section
date_today = datetime.date.today()
header = f"\n\n## One-Minute Daily AI News {date_today.strftime('%B %d, %Y')}\nNews\n\n"
news_lines = ""
sources_lines = "\nSources:\n\n"
for i, (title, link) in enumerate(unique_news, start=1):
    news_lines += f"{title}[{i}]\n\n"
    sources_lines += f"[{i}] {link}\n\n"

# Combine all
section = header + news_lines + sources_lines
updated_content = section + existing

# Save updated file
with open(FILE_PATH, "w") as f:
    f.write(updated_content)

print("✅ blogs-and-news.md updated successfully.")
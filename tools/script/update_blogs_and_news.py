# tools/scripts/update_blogs_and_news.py

import datetime
import requests
import xml.etree.ElementTree as ET
import time
import urllib.parse
import re

# Target file path
FILE_PATH = "blogs-and-news.md"

# RSS feed for Google News on AI
RSS_FEED_URL = "https://news.google.com/rss/search?q=AI&hl=en-US&gl=US&ceid=US:en"

# Expanded keywords for broader AI news coverage
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
    "Reinforcement Learning", "Transfer Learning", "Few-shot Learning", "Zero-shot Learning",
    # New: Startups, Investments, Funds, Regions
    "AI startup", "AI startups", "AI investment", "AI investments", "VC fund", "Venture Capital", "Hedge Fund",
    "AI funding", "AI IPO", "AI acquisition", "AI regulation", "AI merger", "AI India", "AI US", "AI United States", "AI America"
]

# Severity keywords for prioritization
SEVERITY_KEYWORDS = [
    "breakthrough", "investment", "funding", "regulation", "acquisition", "IPO", "ban", "lawsuit", "record", "exclusive", "crisis", "merger",
    "AI startup", "AI startups", "VC fund", "Venture Capital", "Hedge Fund", "OpenAI", "Anthropic", "India", "US", "United States", "America"
]

# Helper: Shorten URLs using TinyURL API
def shorten_url(url):
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
        res = requests.get(api_url, timeout=5)
        if res.status_code == 200:
            return res.text.strip()
    except Exception:
        pass
    return url  # fallback to original if failed

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

# Prioritize by severity
def severity_score(title):
    t = title.lower()
    return sum(1 for kw in SEVERITY_KEYWORDS if kw.lower() in t)

unique_news.sort(key=lambda x: severity_score(x[0]), reverse=True)

# Limit to top 10
top_news = unique_news[:10]

# Shorten URLs for citations
short_links = []
for _, link in top_news:
    short_links.append(shorten_url(link))
    time.sleep(0.5)  # avoid rate limiting

# Read existing content and remove today's section if present
try:
    with open(FILE_PATH, "r") as f:
        existing = f.read()
except FileNotFoundError:
    existing = "# 🔗 Blog Posts / News Articles\n"

date_today = datetime.date.today()
date_str = date_today.strftime('%B %d, %Y')

# Remove any existing section for today
pattern = re.compile(rf"## Quick Daily AI News {re.escape(date_str)}.*?(?=\n## |\Z)", re.DOTALL)
existing = re.sub(pattern, '', existing).strip()

# Format today's section
header = f"\n\n## Quick Daily AI News {date_str}\nNews\n\n"
news_lines = ""
for i, (title, _) in enumerate(top_news, start=1):
    news_lines += f"{i}. {title} [{i}]\n\n"
# Sources in a single line
sources_line = "Sources:\n" + " ".join([f"[{i+1}] {short_links[i]}" for i in range(len(short_links))]) + "\n"

# Combine all, prepend today's news, add horizontal rule after each day
section = header + news_lines + sources_line + '\n---\n'
updated_content = section + '\n' + existing.lstrip('#').strip()  # keep top heading only once
if not updated_content.startswith('#'):
    updated_content = '# 🔗 Blog Posts / News Articles\n' + updated_content

# Save updated file
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("✅ blogs-and-news.md updated successfully.")
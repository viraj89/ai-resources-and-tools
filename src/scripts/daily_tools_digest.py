#!/usr/bin/env python3
"""
Daily AI Tools Digest Generator
- Discovers 3-5 top trending AI tools/apps
- Appends a daily markdown section to ai-tools-daily.md in the root
- Updates data/master_resources.csv (deduplicated)
- No duplicates in either file
- Clean, short, markdown-compatible output
"""

import os
import csv
import datetime
import requests
import json
import time
import re
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT_MD_PATH = "ai-tools-daily.md"
MASTER_CSV_PATH = "data/master_resources.csv"
CACHE_FILE = "data/cache/tools_cache.json"

# AI-related keywords for filtering
AI_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "ML", "GPT", "ChatGPT", "Claude", "DALL-E",
    "Stable Diffusion", "Midjourney", "generative", "neural", "deep learning", "LLM", "large language model",
    "computer vision", "NLP", "natural language", "automation", "intelligent", "smart", "assistant",
    "chatbot", "transformer", "diffusion", "generation", "synthesis", "analysis", "prediction"
]

# Trending keywords for better tool detection
TRENDING_KEYWORDS = [
    "launch", "release", "new", "just dropped", "announcement", 
    "beta", "alpha", "preview", "demo", "showcase", "introducing",
    "trending", "viral", "popular", "hot", "must-try", "game-changer",
    "breakthrough", "revolutionary", "innovative", "cutting-edge"
]

# Enhanced Reddit subreddits for AI tools discovery
REDDIT_SUBREDDITS = [
    "artificial", "MachineLearning", "AINews", "OpenAI", "StableDiffusion", 
    "LocalLLaMA", "ChatGPT", "AI", "artificialintelligence", "deeplearning"
]

# Categories mapping
CATEGORIES = {
    "text": ["Text / Chat Assistants", "Productivity / Writing"],
    "code": ["Code / Developer Tools"],
    "image": ["Design / Image Generation"],
    "video": ["Video / Creative Tools"],
    "audio": ["Voice / Audio Tools"],
    "presentation": ["Presentations"],
    "research": ["Search / Research"],
    "business": ["Business / Analytics"],
    "education": ["Education / Learning"]
}

class AIToolsDiscoverer:
    def __init__(self):
        self.existing_tools = self.load_existing_tools()
        self.cache = self.load_cache()
        self.new_tools = []
        
    def load_existing_tools(self):
        """Load existing tools from CSV to avoid duplicates"""
        tools = set()
        try:
            with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tools.add(row['Tool Name'].lower().strip())
        except FileNotFoundError:
            pass
        return tools
    
    def load_cache(self):
        """Load cache to avoid re-processing same items"""
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"processed_items": [], "last_update": None}
    
    def save_cache(self):
        """Save cache"""
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def is_ai_related(self, text):
        """Check if text is AI-related"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in AI_KEYWORDS)
    
    def calculate_trending_score(self, title, description, upvotes=0, comments=0, source=""):
        """Calculate trending score for a tool"""
        score = 0
        text = (title + " " + description).lower()
        
        # Base AI relevance score
        ai_keywords_found = sum(1 for keyword in AI_KEYWORDS if keyword.lower() in text)
        score += ai_keywords_found * 10
        
        # Trending keywords bonus
        trending_keywords_found = sum(1 for keyword in TRENDING_KEYWORDS if keyword.lower() in text)
        score += trending_keywords_found * 20
        
        # Reddit engagement score
        if source == "reddit":
            score += min(upvotes, 1000) * 0.1  # Cap at 100 points for 1000+ upvotes
            score += min(comments, 100) * 0.5   # Cap at 50 points for 100+ comments
        
        # GitHub trending bonus
        if source == "github":
            score += 50  # Base bonus for GitHub trending
        
        return score
    
    def extract_tool_info(self, title, description, url, source="", upvotes=0, comments=0):
        """Extract structured tool information with trending score"""
        # Basic cleaning
        title = title.strip()
        description = description.strip() if description else ""
        
        # Skip if already exists
        if title.lower() in self.existing_tools:
            return None
        
        # Skip if not AI-related
        if not self.is_ai_related(title + " " + description):
            return None
        
        # Skip if it's clearly not a tool (Reddit posts, news articles, etc.)
        if self.is_non_tool_content(title, description, url):
            return None
        
        # Calculate trending score
        trending_score = self.calculate_trending_score(title, description, upvotes, comments, source)
        
        # Determine category based on keywords
        category = self.categorize_tool(title, description)
        
        # Determine pricing (basic heuristic)
        pricing = self.determine_pricing(description)
        
        return {
            "Tool Name": title,
            "Category": category,
            "URL": url,
            "What it does": description[:200] + "..." if len(description) > 200 else description,
            "Free/Paid": pricing,
            "Trending Score": trending_score,
            "Source": source
        }
    
    def is_non_tool_content(self, title, description, url):
        """Check if this is non-tool content (posts, articles, etc.)"""
        
        # Skip if no URL or invalid URL
        if not url or url == "N/A" or not url.startswith('http'):
            return True
        
        # Skip if it's clearly a Reddit post or social media
        if any(indicator in url.lower() for indicator in ["reddit.com", "redd.it", "twitter.com", "youtu.be", "youtube.com"]):
            return True
        
        # Skip if it's a news article or research paper
        if any(indicator in url.lower() for indicator in ["arxiv.org", "news", "article", "blog", "medium.com"]):
            return True
        
        # Skip if name contains non-tool indicators
        name_lower = title.lower()
        non_tool_indicators = [
            "reddit", "post", "article", "news", "report", "discussion", "question", 
            "how to", "tutorial", "guide", "analysis", "review", "announcement", 
            "update", "release", "launch", "introducing", "new feature", "research",
            "paper", "study", "analysis", "tweet", "thread", "video", "image"
        ]
        
        if any(indicator in name_lower for indicator in non_tool_indicators):
            return True
        
        # Skip if it's a GitHub repository without clear tool indicators
        if "github.com" in url.lower():
            tool_indicators = [
                "ai", "gpt", "claude", "assistant", "tool", "platform", "app", "bot", "agent",
                "generator", "creator", "studio", "hub", "workspace", "lab", "kit", "suite",
                "api", "sdk", "framework", "library", "engine", "model", "service", "solution"
            ]
            if not any(indicator in name_lower for indicator in tool_indicators):
                return True
        
        # Skip if description is too short or contains non-tool content
        if not description or len(description) < 10:
            return True
        
        # Skip if description contains non-tool indicators
        desc_lower = description.lower()
        if any(indicator in desc_lower for indicator in non_tool_indicators):
            return True
        
        return False
    
    def categorize_tool(self, title, description):
        """Categorize tool based on keywords"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ["chat", "assistant", "writing", "text", "gpt", "claude"]):
            return "Text / Chat Assistants"
        elif any(word in text for word in ["code", "programming", "developer", "github", "copilot"]):
            return "Code / Developer Tools"
        elif any(word in text for word in ["image", "photo", "art", "design", "dall", "midjourney", "stable diffusion"]):
            return "Design / Image Generation"
        elif any(word in text for word in ["video", "animation", "movie", "runway", "pika"]):
            return "Video / Creative Tools"
        elif any(word in text for word in ["voice", "audio", "speech", "music", "elevenlabs"]):
            return "Voice / Audio Tools"
        elif any(word in text for word in ["presentation", "slide", "pitch", "gamma", "tome"]):
            return "Presentations"
        elif any(word in text for word in ["search", "research", "perplexity", "query"]):
            return "Search / Research"
        else:
            return "Other"
    
    def determine_pricing(self, description):
        """Determine pricing model"""
        text = description.lower()
        if any(word in text for word in ["free", "open source", "free tier"]):
            return "Freemium"
        elif any(word in text for word in ["paid", "subscription", "premium", "pro"]):
            return "Paid"
        else:
            return "N/A"
    
    def discover_from_github_trending(self):
        """Discover AI tools from GitHub trending"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get("https://github.com/trending?since=daily&spoken_language_code=en", headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                repos = soup.find_all('article', class_='Box-row')
                
                for repo in repos[:25]:  # Increased limit for better selection
                    try:
                        title_elem = repo.find('h2', class_='h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        description_elem = repo.find('p')
                        description = description_elem.get_text(strip=True) if description_elem else ""
                        
                        # Extract URL
                        link_elem = title_elem.find('a')
                        if link_elem:
                            url = "https://github.com" + link_elem.get('href')
                        else:
                            continue
                        
                        tool_info = self.extract_tool_info(title, description, url, "github")
                        if tool_info:
                            self.new_tools.append(tool_info)
                            
                    except Exception as e:
                        print(f"Error processing GitHub repo: {e}")
                        
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
    
    def discover_from_reddit(self, subreddit):
        """Discover AI tools from Reddit with enhanced trending detection"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Try multiple Reddit endpoints for better coverage
            endpoints = [
                f"https://www.reddit.com/r/{subreddit}/hot.json",
                f"https://www.reddit.com/r/{subreddit}/new.json",
                f"https://www.reddit.com/r/{subreddit}/top.json?t=day"
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])
                        
                        for post in posts[:20]:  # Increased limit
                            try:
                                post_data = post['data']
                                title = post_data.get('title', '')
                                description = post_data.get('selftext', '')
                                url = post_data.get('url', '')
                                upvotes = post_data.get('score', 0)
                                comments = post_data.get('num_comments', 0)
                                
                                # Skip if it's a Reddit post URL
                                if 'reddit.com' in url:
                                    continue
                                
                                # Only process posts with some engagement
                                if upvotes > 5 or comments > 2:
                                    tool_info = self.extract_tool_info(title, description, url, "reddit", upvotes, comments)
                                    if tool_info:
                                        self.new_tools.append(tool_info)
                                        
                            except Exception as e:
                                print(f"Error processing Reddit post: {e}")
                                
                except Exception as e:
                    print(f"Error fetching Reddit {subreddit} from {endpoint}: {e}")
                    continue
                        
        except Exception as e:
            print(f"Error fetching Reddit {subreddit}: {e}")
    
    def discover_from_news_articles(self):
        """Extract tool mentions from existing news articles"""
        try:
            with open("blogs-and-news.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for potential tool names in news
            lines = content.split('\n')
            for line in lines:
                # Enhanced pattern matching for better tool detection
                patterns = [
                    r'([A-Z][a-zA-Z0-9\s]+(?:AI|GPT|Assistant|Tool|Platform|App|Bot|Agent))',
                    r'([A-Z][a-zA-Z0-9\s]+(?:\.ai|\.com|\.io|\.app))',
                    r'([A-Z][a-zA-Z0-9\s]+(?: launches| releases| introduces| announces))'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        if len(match.strip()) > 3 and self.is_ai_related(match):
                            tool_info = self.extract_tool_info(match.strip(), line, "N/A", "news")
                            if tool_info:
                                self.new_tools.append(tool_info)
                            
        except FileNotFoundError:
            print("News file not found, skipping news-based discovery")
        except Exception as e:
            print(f"Error processing news articles: {e}")
    
    def enrich_tool_data(self, tool_info):
        """Enrich tool data by scraping the website"""
        try:
            url = tool_info['URL']
            if url == "N/A" or not url.startswith('http'):
                return tool_info
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to get better description from meta tags
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    tool_info['What it does'] = meta_desc['content'][:200] + "..." if len(meta_desc['content']) > 200 else meta_desc['content']
                
                # Try to get pricing info
                page_text = soup.get_text().lower()
                if any(word in page_text for word in ["free", "open source"]):
                    tool_info['Free/Paid'] = "Freemium"
                elif any(word in page_text for word in ["paid", "subscription", "premium"]):
                    tool_info['Free/Paid'] = "Paid"
                    
        except Exception as e:
            print(f"Error enriching data for {tool_info['Tool Name']}: {e}")
        
        return tool_info
    
    def run_discovery(self):
        """Run the complete discovery process"""
        print("🔍 Starting Enhanced AI Tools Discovery...")
        
        # Discover from various sources
        self.discover_from_github_trending()
        
        # Discover from multiple Reddit subreddits
        for subreddit in REDDIT_SUBREDDITS[:5]:  # Limit to top 5 to avoid rate limiting
            self.discover_from_reddit(subreddit)
            time.sleep(1)  # Be respectful to Reddit
        
        self.discover_from_news_articles()
        
        # Remove duplicates
        seen_names = set()
        unique_tools = []
        for tool in self.new_tools:
            if tool['Tool Name'].lower() not in seen_names:
                seen_names.add(tool['Tool Name'].lower())
                unique_tools.append(tool)
        
        self.new_tools = unique_tools
        
        # Sort by trending score (highest first)
        self.new_tools.sort(key=lambda x: x.get('Trending Score', 0), reverse=True)
        
        print(f"📊 Discovered {len(self.new_tools)} potential new AI tools")
        
        # Enrich and add tools
        added_count = 0
        for tool in self.new_tools:
            enriched_tool = self.enrich_tool_data(tool)
            if self.add_to_csv(enriched_tool):
                added_count += 1
                time.sleep(1)  # Be respectful to servers
        
        print(f"✅ Successfully added {added_count} new tools to master_resources.csv")
        
        # Save cache
        self.save_cache()
        
        return added_count
    
    def add_to_csv(self, tool_info):
        """Add new tool to CSV file"""
        try:
            # Get next serial number
            next_sr = 1
            if os.path.exists(MASTER_CSV_PATH):
                with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    if rows:
                        next_sr = int(rows[-1]['Sr. No.']) + 1
            
            # Prepare new row
            new_row = {
                'Sr. No.': next_sr,
                'Tool Name': tool_info['Tool Name'],
                'Category': tool_info['Category'],
                'URL': tool_info['URL'],
                'What it does': tool_info['What it does'],
                'Free/Paid': tool_info['Free/Paid']
            }
            
            # Append to CSV
            file_exists = os.path.exists(MASTER_CSV_PATH)
            with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['Sr. No.', 'Tool Name', 'Category', 'URL', 'What it does', 'Free/Paid'])
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(new_row)
            
            print(f"✅ Added: {tool_info['Tool Name']} (Score: {tool_info.get('Trending Score', 0)})")
            return True
            
        except Exception as e:
            print(f"Error adding tool to CSV: {e}")
            return False

# Helper: Load all tool names and URLs from master CSV
def load_master_tools():
    tools = set()
    urls = set()
    try:
        with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tools.add(row['Tool Name'].strip().lower())
                urls.add(row['URL'].strip().lower())
    except FileNotFoundError:
        pass
    return tools, urls

# Helper: Append new tool to master CSV
def append_to_master_csv(tool_info):
    file_exists = os.path.exists(MASTER_CSV_PATH)
    next_sr = 1
    if file_exists:
        with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                next_sr = int(rows[-1]['Sr. No.']) + 1
    new_row = {
        'Sr. No.': next_sr,
        'Tool Name': tool_info['Tool Name'],
        'Category': tool_info['Category'],
        'URL': tool_info['URL'],
        'What it does': tool_info['What it does'],
        'Free/Paid': tool_info['Free/Paid']
    }
    with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Sr. No.', 'Tool Name', 'Category', 'URL', 'What it does', 'Free/Paid'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

# Helper: Write today's markdown section with master CSV link
def write_daily_markdown(tools):
    today = datetime.date.today().strftime('%B %d, %Y')
    section_title = f"## AI Tools and Apps of the Day: {today}\n---\n"
    lines = []
    for i, tool in enumerate(tools, 1):
        name = tool['Tool Name'].strip()
        url = tool['URL'].strip()
        desc = tool['What it does'].strip().replace('\n', ' ')
        if not url or url == 'N/A':
            url = '#'
        lines.append(f"{i}. {name} – [{url}]({url}) – {desc}")
    
    # Add master CSV link
    master_link = f"\n📋 **Master List**: View the complete, deduplicated collection of all AI tools and resources in our [master_resources.csv](data/master_resources.csv) file.\n"
    
    section = section_title + '\n'.join(lines) + master_link + '\n'
    
    # Prepend today's section to the file
    if os.path.exists(ROOT_MD_PATH):
        with open(ROOT_MD_PATH, 'r', encoding='utf-8') as f:
            existing = f.read()
    else:
        existing = ''
    
    # Remove any existing section for today
    import re
    pattern = re.compile(rf"## AI Tools and Apps of the Day: {today}.*?(?=\n## |\Z)", re.DOTALL)
    existing = re.sub(pattern, '', existing).strip()
    
    with open(ROOT_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(section + (('\n' + existing) if existing else ''))

# Main logic
def main():
    # Load master tool names and URLs
    master_names, master_urls = load_master_tools()
    # Discover new tools (reuse existing logic)
    discoverer = AIToolsDiscoverer()
    discoverer.run_discovery()
    # Filter out tools already in master
    new_tools = [t for t in discoverer.new_tools if t['Tool Name'].strip().lower() not in master_names and t['URL'].strip().lower() not in master_urls]
    # Select top 3-5 trending tools (already sorted by score)
    top_tools = new_tools[:5] if len(new_tools) >= 3 else new_tools
    if len(top_tools) > 5:
        top_tools = top_tools[:5]
    elif len(top_tools) < 3:
        print("Not enough new tools found for today's digest.")
        return
    # Write markdown
    write_daily_markdown(top_tools)
    # Append to master CSV
    for tool in top_tools:
        append_to_master_csv(tool)
    print(f"✅ Daily digest written with {len(top_tools)} tools. Master CSV updated.")

if __name__ == "__main__":
    main() 
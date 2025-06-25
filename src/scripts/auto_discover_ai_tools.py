#!/usr/bin/env python3
"""
AI Tools Auto-Discovery and Enrichment System
Automatically discovers new AI tools from multiple sources and adds them to master_resources.csv

Main script for automated AI tools discovery.
- Integrates multiple sources (Product Hunt, Hacker News, GitHub, Reddit)
- Applies quality ranking and filtering
- Outputs daily digest and updates master resources
"""

import csv
import requests
import json
import time
import re
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import hashlib

# Configuration
MASTER_CSV_PATH = "data/master_resources.csv"
CACHE_FILE = "data/cache/tools_cache.json"
NEW_TOOLS_FILE = "data/cache/new_tools_discovered.json"

# Sources for AI tool discovery
SOURCES = {
    "github_trending": "https://github.com/trending?since=daily&spoken_language_code=en",
    "producthunt_api": "https://api.producthunt.com/v2/api/graphql",
    "reddit_ml": "https://www.reddit.com/r/MachineLearning/new.json",
    "reddit_ai": "https://www.reddit.com/r/artificial/new.json",
    "huggingface": "https://huggingface.co/models?sort=downloads&search=ai",
    "futurepedia": "https://www.futurepedia.io/tools",
    "theresanai": "https://theresanaiforthat.com/"
}

# AI-related keywords for filtering
AI_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "ML", "GPT", "ChatGPT", "Claude", "DALL-E",
    "Stable Diffusion", "Midjourney", "generative", "neural", "deep learning", "LLM", "large language model",
    "computer vision", "NLP", "natural language", "automation", "intelligent", "smart", "assistant",
    "chatbot", "transformer", "diffusion", "generation", "synthesis", "analysis", "prediction"
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
    
    def extract_tool_info(self, title, description, url):
        """Extract structured tool information"""
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
        
        # Determine category based on keywords
        category = self.categorize_tool(title, description)
        
        # Determine pricing (basic heuristic)
        pricing = self.determine_pricing(description)
        
        return {
            "Tool Name": title,
            "Category": category,
            "URL": url,
            "What it does": description[:200] + "..." if len(description) > 200 else description,
            "Free/Paid": pricing
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
            response = requests.get(SOURCES["github_trending"], headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                repos = soup.find_all('article', class_='Box-row')
                
                for repo in repos[:20]:  # Limit to top 20
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
                        
                        tool_info = self.extract_tool_info(title, description, url)
                        if tool_info:
                            self.new_tools.append(tool_info)
                            
                    except Exception as e:
                        print(f"Error processing GitHub repo: {e}")
                        
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
    
    def discover_from_reddit(self, subreddit):
        """Discover AI tools from Reddit"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            url = SOURCES[f"reddit_{subreddit}"]
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post in posts[:15]:  # Limit to top 15
                    try:
                        post_data = post['data']
                        title = post_data.get('title', '')
                        description = post_data.get('selftext', '')
                        url = post_data.get('url', '')
                        
                        # Skip if it's a Reddit post URL
                        if 'reddit.com' in url:
                            continue
                        
                        tool_info = self.extract_tool_info(title, description, url)
                        if tool_info:
                            self.new_tools.append(tool_info)
                            
                    except Exception as e:
                        print(f"Error processing Reddit post: {e}")
                        
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
                # Look for patterns like "New AI tool X" or "X launches Y"
                matches = re.findall(r'([A-Z][a-zA-Z0-9\s]+(?:AI|GPT|Assistant|Tool|Platform|App))', line)
                for match in matches:
                    if len(match.strip()) > 3 and self.is_ai_related(match):
                        tool_info = self.extract_tool_info(match.strip(), line, "N/A")
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
            
            print(f"✅ Added: {tool_info['Tool Name']}")
            return True
            
        except Exception as e:
            print(f"Error adding tool to CSV: {e}")
            return False
    
    def run_discovery(self):
        """Run the complete discovery process"""
        print("🔍 Starting AI Tools Discovery...")
        
        # Discover from various sources
        self.discover_from_github_trending()
        self.discover_from_reddit('ml')
        self.discover_from_reddit('ai')
        self.discover_from_news_articles()
        
        # Remove duplicates
        seen_names = set()
        unique_tools = []
        for tool in self.new_tools:
            if tool['Tool Name'].lower() not in seen_names:
                seen_names.add(tool['Tool Name'].lower())
                unique_tools.append(tool)
        
        self.new_tools = unique_tools
        
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

def main():
    """Main function"""
    discoverer = AIToolsDiscoverer()
    added_count = discoverer.run_discovery()
    
    if added_count > 0:
        print(f"\n🎉 Discovery complete! Added {added_count} new AI tools.")
    else:
        print("\n📝 No new tools discovered this time.")

if __name__ == "__main__":
    main() 
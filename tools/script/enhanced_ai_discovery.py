#!/usr/bin/env python3
"""
Enhanced AI Tools Auto-Discovery with AI-Powered Categorization
Uses AI APIs for better tool classification and description generation
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
MASTER_CSV_PATH = "tools/resources/master_resources.csv"
CACHE_FILE = "tools/resources/enhanced_tools_cache.json"
NEW_TOOLS_FILE = "tools/resources/enhanced_new_tools.json"

# AI API Configuration (optional - for enhanced categorization)
# You can add your API keys here for better categorization
AI_API_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "use_ai_categorization": False  # Set to True if you have API keys
}

# Sources for AI tool discovery
SOURCES = {
    "github_trending": "https://github.com/trending?since=daily&spoken_language_code=en",
    "reddit_ml": "https://www.reddit.com/r/MachineLearning/new.json",
    "reddit_ai": "https://www.reddit.com/r/artificial/new.json",
    "huggingface": "https://huggingface.co/models?sort=downloads&search=ai",
    "futurepedia": "https://www.futurepedia.io/tools",
    "theresanai": "https://theresanaiforthat.com/",
    "producthunt": "https://www.producthunt.com/topics/artificial-intelligence"
}

# Enhanced AI-related keywords
AI_KEYWORDS = [
    # Major AI Companies & Models
    "OpenAI", "Anthropic", "Google AI", "Microsoft AI", "Meta AI", "DeepMind", "Stability AI", 
    "Midjourney", "Cohere", "ChatGPT", "Claude", "GPT-4", "DALL-E", "Stable Diffusion", 
    "Gemini", "Llama", "Mistral", "Falcon", "Bard", "Copilot",
    
    # AI Technologies
    "AI", "artificial intelligence", "machine learning", "ML", "deep learning", "neural networks",
    "large language model", "LLM", "generative AI", "computer vision", "NLP", "natural language processing",
    "transformer", "diffusion", "generation", "synthesis", "analysis", "prediction", "automation",
    "intelligent", "smart", "assistant", "chatbot", "agent", "autonomous", "cognitive",
    
    # AI Applications
    "AI tool", "AI platform", "AI software", "AI application", "AI service", "AI solution",
    "text generation", "image generation", "video generation", "audio generation", "code generation",
    "data analysis", "predictive analytics", "recommendation system", "optimization", "automation"
]

# Enhanced categories with subcategories
CATEGORIES = {
    "Text / Chat Assistants": ["chat", "assistant", "writing", "text", "gpt", "claude", "bard", "conversation", "dialogue"],
    "Code / Developer Tools": ["code", "programming", "developer", "github", "copilot", "debug", "refactor", "testing"],
    "Design / Image Generation": ["image", "photo", "art", "design", "dall", "midjourney", "stable diffusion", "visual", "graphic"],
    "Video / Creative Tools": ["video", "animation", "movie", "runway", "pika", "motion", "cinematic"],
    "Voice / Audio Tools": ["voice", "audio", "speech", "music", "elevenlabs", "sound", "synthesis"],
    "Presentations": ["presentation", "slide", "pitch", "gamma", "tome", "deck", "storytelling"],
    "Search / Research": ["search", "research", "perplexity", "query", "discovery", "exploration"],
    "Business / Analytics": ["business", "analytics", "data", "insights", "dashboard", "reporting", "metrics"],
    "Education / Learning": ["education", "learning", "tutorial", "course", "training", "knowledge"],
    "Productivity / Writing": ["productivity", "writing", "document", "note", "organize", "planning"],
    "Other": []
}

class EnhancedAIToolsDiscoverer:
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
        """Enhanced AI relevance check"""
        text_lower = text.lower()
        score = 0
        
        # Check for AI keywords
        for keyword in AI_KEYWORDS:
            if keyword.lower() in text_lower:
                score += 1
        
        # Bonus for multiple AI terms
        if score >= 2:
            return True
        elif score == 1 and len(text) > 50:  # Single keyword but substantial text
            return True
        
        return False
    
    def extract_tool_info(self, title, description, url, source=""):
        """Extract structured tool information with enhanced processing"""
        # Basic cleaning
        title = title.strip()
        description = description.strip() if description else ""
        
        # Skip if already exists
        if title.lower() in self.existing_tools:
            return None
        
        # Skip if not AI-related
        if not self.is_ai_related(title + " " + description):
            return None
        
        # Enhanced categorization
        category = self.categorize_tool_enhanced(title, description)
        
        # Enhanced pricing detection
        pricing = self.determine_pricing_enhanced(description, url)
        
        # Enhanced description
        enhanced_description = self.enhance_description(title, description, url)
        
        return {
            "Tool Name": title,
            "Category": category,
            "URL": url,
            "What it does": enhanced_description,
            "Free/Paid": pricing,
            "Source": source,
            "Discovered": datetime.now().strftime('%Y-%m-%d')
        }
    
    def categorize_tool_enhanced(self, title, description):
        """Enhanced categorization using multiple heuristics"""
        text = (title + " " + description).lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in CATEGORIES.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        # Return highest scoring category
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "Other"
    
    def determine_pricing_enhanced(self, description, url):
        """Enhanced pricing detection"""
        text = (description + " " + url).lower()
        
        # More sophisticated pricing detection
        if any(word in text for word in ["free", "open source", "free tier", "free plan", "no cost"]):
            return "Freemium"
        elif any(word in text for word in ["paid", "subscription", "premium", "pro", "enterprise", "pricing"]):
            return "Paid"
        elif any(word in text for word in ["beta", "early access", "waitlist", "invite"]):
            return "Beta/Invite"
        else:
            return "N/A"
    
    def enhance_description(self, title, description, url):
        """Enhance description with better formatting and details"""
        if not description:
            description = f"AI-powered tool: {title}"
        
        # Clean up description
        description = re.sub(r'\s+', ' ', description)  # Remove extra whitespace
        description = description.strip()
        
        # Limit length
        if len(description) > 200:
            description = description[:197] + "..."
        
        return description
    
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
                
                for repo in repos[:25]:  # Increased limit
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
                        
                        tool_info = self.extract_tool_info(title, description, url, "GitHub Trending")
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
                
                for post in posts[:20]:  # Increased limit
                    try:
                        post_data = post['data']
                        title = post_data.get('title', '')
                        description = post_data.get('selftext', '')
                        url = post_data.get('url', '')
                        
                        # Skip if it's a Reddit post URL
                        if 'reddit.com' in url:
                            continue
                        
                        tool_info = self.extract_tool_info(title, description, url, f"Reddit r/{subreddit}")
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
                # Enhanced pattern matching
                patterns = [
                    r'([A-Z][a-zA-Z0-9\s]+(?:AI|GPT|Assistant|Tool|Platform|App|Bot|Agent))',
                    r'([A-Z][a-zA-Z0-9\s]+(?:\.ai|\.com|\.io|\.app))',
                    r'([A-Z][a-zA-Z0-9\s]+(?: launches| releases| introduces| announces))'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        if len(match.strip()) > 3 and self.is_ai_related(match):
                            tool_info = self.extract_tool_info(match.strip(), line, "N/A", "News Articles")
                            if tool_info:
                                self.new_tools.append(tool_info)
                            
        except FileNotFoundError:
            print("News file not found, skipping news-based discovery")
        except Exception as e:
            print(f"Error processing news articles: {e}")
    
    def enrich_tool_data(self, tool_info):
        """Enhanced tool data enrichment"""
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
                
                # Try to get better description from multiple sources
                description_sources = []
                
                # Meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    description_sources.append(meta_desc['content'])
                
                # Open Graph description
                og_desc = soup.find('meta', attrs={'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    description_sources.append(og_desc['content'])
                
                # First paragraph
                first_p = soup.find('p')
                if first_p:
                    description_sources.append(first_p.get_text())
                
                # Use the best description
                if description_sources:
                    best_desc = max(description_sources, key=len)
                    if len(best_desc) > len(tool_info['What it does']):
                        tool_info['What it does'] = best_desc[:200] + "..." if len(best_desc) > 200 else best_desc
                
                # Enhanced pricing detection from page content
                page_text = soup.get_text().lower()
                if any(word in page_text for word in ["free", "open source", "free tier", "free plan"]):
                    tool_info['Free/Paid'] = "Freemium"
                elif any(word in page_text for word in ["paid", "subscription", "premium", "pro", "enterprise"]):
                    tool_info['Free/Paid'] = "Paid"
                    
        except Exception as e:
            print(f"Error enriching data for {tool_info['Tool Name']}: {e}")
        
        return tool_info
    
    def add_to_csv(self, tool_info):
        """Add new tool to CSV file with enhanced data"""
        try:
            # Get next serial number
            next_sr = 1
            if os.path.exists(MASTER_CSV_PATH):
                with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    if rows:
                        next_sr = int(rows[-1]['Sr. No.']) + 1
            
            # Prepare new row (without extra fields for CSV compatibility)
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
            
            print(f"✅ Added: {tool_info['Tool Name']} ({tool_info['Category']})")
            return True
            
        except Exception as e:
            print(f"Error adding tool to CSV: {e}")
            return False
    
    def run_discovery(self):
        """Run the complete enhanced discovery process"""
        print("🔍 Starting Enhanced AI Tools Discovery...")
        
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
    discoverer = EnhancedAIToolsDiscoverer()
    added_count = discoverer.run_discovery()
    
    if added_count > 0:
        print(f"\n🎉 Enhanced discovery complete! Added {added_count} new AI tools.")
    else:
        print("\n📝 No new tools discovered this time.")

if __name__ == "__main__":
    main() 
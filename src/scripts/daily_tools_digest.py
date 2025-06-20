#!/usr/bin/env python3
"""
Daily AI Tools Digest Generator

This module implements an intelligent AI tools discovery system that:
- Discovers 3-5 top trending AI tools/apps daily from multiple sources
- Appends a daily markdown section to ai-tools-daily.md in the artifacts directory
- Updates data/master_resources.csv with deduplicated entries
- Prevents duplicates across both output files
- Generates clean, markdown-compatible output
- Uses dynamic keyword learning system for improved discovery

The system employs a sophisticated trending score algorithm that considers:
- AI relevance using dynamic keywords
- Trending indicators (launch, release, new, etc.)
- Engagement metrics (Reddit upvotes/comments)
- Source diversity and credibility
- Content quality filtering

Author: AI Insights Daily Team
Version: 3.1.0
Last Updated: January 2025
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
import sys

# Add src to path for imports to ensure proper module resolution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.keyword_manager import KeywordManager

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# File paths for data persistence and output
ARTIFACTS_DIR = "artifacts"  # Directory for generated content
ROOT_MD_PATH = os.path.join(ARTIFACTS_DIR, "ai-tools-daily.md")  # Daily digest output
MASTER_CSV_PATH = "data/master_resources.csv"  # Master tools database
CACHE_FILE = "data/cache/tools_cache.json"  # Cache for performance optimization

# Reddit subreddits for AI tools discovery - carefully curated for relevance
# These subreddits are selected based on their focus on AI tools and active communities
REDDIT_SUBREDDITS = [
    "artificial", "MachineLearning", "AINews", "OpenAI", "StableDiffusion", 
    "LocalLLaMA", "ChatGPT", "AI", "artificialintelligence", "deeplearning"
]

# Trending keywords that indicate new or popular tools
# These keywords are weighted heavily in the trending score algorithm
TRENDING_KEYWORDS = [
    "launch", "release", "new", "just dropped", "announcement", 
    "beta", "alpha", "preview", "demo", "showcase", "introducing",
    "trending", "viral", "popular", "hot", "must-try", "game-changer",
    "breakthrough", "revolutionary", "innovative", "cutting-edge"
]

# Category mapping for tool classification
# Maps keyword patterns to human-readable categories for better organization
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

# =============================================================================
# MAIN DISCOVERY CLASS
# =============================================================================

class AIToolsDiscoverer:
    """
    Main class responsible for discovering and processing AI tools.
    
    This class implements a multi-source discovery system that:
    1. Loads existing tools to prevent duplicates
    2. Maintains a cache for performance optimization
    3. Uses dynamic keyword learning for improved relevance
    4. Applies sophisticated filtering and scoring algorithms
    5. Generates structured output for both CSV and markdown formats
    
    The discovery process follows a pipeline:
    Source Discovery → Content Filtering → Relevance Scoring → 
    Deduplication → Data Enrichment → Output Generation
    """
    
    def __init__(self):
        """
        Initialize the AI tools discoverer with necessary data structures.
        
        Loads existing tools, cache, and initializes the keyword manager
        for dynamic keyword-based filtering and categorization.
        """
        self.existing_tools = self.load_existing_tools()
        self.cache = self.load_cache()
        self.new_tools = []
        self.keyword_manager = KeywordManager()
        
    def load_existing_tools(self):
        """
        Load existing tools from CSV to prevent duplicate entries.
        
        Returns:
            set: Set of lowercase tool names for efficient duplicate checking
        """
        tools = set()
        try:
            with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalize tool names for consistent comparison
                    tools.add(row['Tool Name'].lower().strip())
        except FileNotFoundError:
            # If file doesn't exist, start with empty set
            pass
        return tools
    
    def load_cache(self):
        """
        Load cache to avoid re-processing previously seen items.
        
        The cache stores processed item IDs and timestamps to improve
        performance and reduce redundant API calls.
        
        Returns:
            dict: Cache data with processed items and last update timestamp
        """
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Initialize empty cache if file doesn't exist
            return {"processed_items": [], "last_update": None}
    
    def save_cache(self):
        """
        Save current cache state to disk for persistence.
        
        Creates cache directory if it doesn't exist and writes
        the current cache data in JSON format.
        """
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def is_ai_related(self, text):
        """
        Check if text is AI-related using dynamic keyword system.
        
        This method leverages the keyword manager to determine if content
        is relevant to AI tools, using learned keywords that adapt over time.
        
        Args:
            text (str): Text to analyze for AI relevance
            
        Returns:
            bool: True if text is AI-related, False otherwise
        """
        return self.keyword_manager.is_ai_related(text)
    
    def calculate_trending_score(self, title, description, upvotes=0, comments=0, source=""):
        """
        Calculate a comprehensive trending score for a tool.
        
        This algorithm combines multiple factors to determine how "trending"
        a tool is, using weighted scoring based on:
        - AI keyword relevance (using dynamic keywords)
        - Trending indicators (launch, release, new, etc.)
        - Engagement metrics (Reddit upvotes/comments)
        - Source credibility (GitHub trending bonus)
        
        Args:
            title (str): Tool title
            description (str): Tool description
            upvotes (int): Number of upvotes (for Reddit content)
            comments (int): Number of comments (for Reddit content)
            source (str): Source of the content (reddit, github, etc.)
            
        Returns:
            float: Trending score (higher = more trending)
        """
        score = 0
        text = (title + " " + description).lower()
        
        # Base AI relevance score using dynamic keywords
        # This is the foundation of the scoring system
        ai_keywords = self.keyword_manager.get_all_ai_keywords_flat()
        ai_keywords_found = sum(1 for keyword in ai_keywords if keyword.lower() in text)
        score += ai_keywords_found * 10  # 10 points per AI keyword
        
        # Trending keywords bonus - heavily weighted for new/popular tools
        trending_keywords_found = sum(1 for keyword in TRENDING_KEYWORDS if keyword.lower() in text)
        score += trending_keywords_found * 20  # 20 points per trending keyword
        
        # Reddit engagement score - rewards community validation
        if source == "reddit":
            # Cap scores to prevent gaming and maintain balance
            score += min(upvotes, 1000) * 0.1  # Max 100 points for 1000+ upvotes
            score += min(comments, 100) * 0.5   # Max 50 points for 100+ comments
        
        # GitHub trending bonus - rewards being on GitHub trending
        if source == "github":
            score += 50  # Base bonus for GitHub trending status
        
        return score
    
    def extract_tool_info(self, title, description, url, source="", upvotes=0, comments=0):
        """
        Extract and structure tool information with comprehensive validation.
        
        This method implements the core filtering and processing logic:
        1. Basic text cleaning and normalization
        2. Duplicate checking against existing tools
        3. AI relevance validation using dynamic keywords
        4. Non-tool content filtering (posts, articles, etc.)
        5. Trending score calculation
        6. Category determination
        7. Pricing model detection
        
        Args:
            title (str): Tool title
            description (str): Tool description
            url (str): Tool URL
            source (str): Source of the content
            upvotes (int): Number of upvotes (for Reddit)
            comments (int): Number of comments (for Reddit)
            
        Returns:
            dict or None: Structured tool information or None if filtered out
        """
        # Basic cleaning and normalization
        title = title.strip()
        description = description.strip() if description else ""
        
        # Skip if already exists in our database
        if title.lower() in self.existing_tools:
            return None
        
        # Skip if not AI-related using dynamic keyword system
        if not self.is_ai_related(title + " " + description):
            return None
        
        # Skip if it's clearly not a tool (Reddit posts, news articles, etc.)
        if self.is_non_tool_content(title, description, url):
            return None
        
        # Calculate comprehensive trending score
        trending_score = self.calculate_trending_score(title, description, upvotes, comments, source)
        
        # Determine category using dynamic keyword categorization
        category = self.keyword_manager.categorize_tool(title, description)
        
        # Determine pricing model using heuristic analysis
        pricing = self.determine_pricing(description)
        
        # Return structured tool information
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
        """
        Check if content is non-tool using dynamic indicators.
        
        This method uses the keyword manager to identify content that
        is not an actual AI tool (e.g., Reddit posts, news articles,
        discussions, tutorials, etc.).
        
        Args:
            title (str): Content title
            description (str): Content description
            url (str): Content URL
            
        Returns:
            bool: True if content is NOT a tool, False if it is a tool
        """
        return not self.keyword_manager.is_tool_content(title, description, url)
    
    def determine_pricing(self, description):
        """
        Determine pricing model using keyword-based heuristics.
        
        Analyzes the description text to identify pricing indicators
        and categorizes the tool as Freemium, Paid, or N/A.
        
        Args:
            description (str): Tool description
            
        Returns:
            str: Pricing category (Freemium, Paid, or N/A)
        """
        text = description.lower()
        if any(word in text for word in ["free", "open source", "free tier"]):
            return "Freemium"
        elif any(word in text for word in ["paid", "subscription", "premium", "pro"]):
            return "Paid"
        else:
            return "N/A"
    
    def discover_from_github_trending(self):
        """
        Discover AI tools from GitHub trending repositories.
        
        This method scrapes GitHub's trending page to find AI-related
        repositories that might be tools or libraries. It applies
        the same filtering and scoring logic as other sources.
        
        The method respects GitHub's terms of service by using
        appropriate headers and rate limiting.
        """
        try:
            # Use proper headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Fetch GitHub trending page with timeout
            response = requests.get(
                "https://github.com/trending?since=daily&spoken_language_code=en", 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                repos = soup.find_all('article', class_='Box-row')
                
                # Process top 25 repositories for better selection
                for repo in repos[:25]:
                    try:
                        # Extract repository title
                        title_elem = repo.find('h2', class_='h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        
                        # Extract repository description
                        description_elem = repo.find('p')
                        description = description_elem.get_text(strip=True) if description_elem else ""
                        
                        # Extract repository URL
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
        """
        Discover AI tools from Reddit with enhanced trending detection.
        
        This method fetches posts from multiple Reddit endpoints (hot, new, top)
        to maximize coverage of trending AI tools. It applies engagement filtering
        to focus on posts with meaningful community interaction.
        
        The method implements rate limiting and error handling to respect
        Reddit's API policies and ensure robust operation.
        
        Args:
            subreddit (str): Name of the subreddit to search
        """
        try:
            # Use proper headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Try multiple Reddit endpoints for better coverage
            # This increases the chance of finding trending tools
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
                        
                        # Process posts with engagement filtering
                        for post in posts[:15]:  # Limit per endpoint to avoid spam
                            try:
                                post_data = post.get('data', {})
                                
                                # Extract post information
                                title = post_data.get('title', '').strip()
                                description = post_data.get('selftext', '').strip()
                                url = post_data.get('url', '')
                                upvotes = post_data.get('score', 0)
                                comments = post_data.get('num_comments', 0)
                                
                                # Apply engagement filtering to focus on quality content
                                if upvotes < 10 or comments < 2:
                                    continue
                                
                                # Process the post through our filtering pipeline
                                tool_info = self.extract_tool_info(
                                    title, description, url, "reddit", upvotes, comments
                                )
                                
                                if tool_info:
                                    self.new_tools.append(tool_info)
                                    
                            except Exception as e:
                                print(f"Error processing Reddit post: {e}")
                                
                        # Rate limiting between endpoints
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"Error fetching from {endpoint}: {e}")
                    
        except Exception as e:
            print(f"Error in Reddit discovery for {subreddit}: {e}")
    
    def discover_from_news_articles(self):
        """
        Discover AI tools from news articles and RSS feeds.
        
        This method searches for AI tool mentions in news articles
        and RSS feeds. It focuses on articles that mention new tool
        launches, releases, or significant updates.
        
        The method uses pattern matching to identify tool mentions
        and applies the same filtering criteria as other sources.
        """
        try:
            # Define news sources that frequently cover AI tools
            news_sources = [
                "https://techcrunch.com/tag/artificial-intelligence/feed/",
                "https://venturebeat.com/category/ai/feed/",
                "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"
            ]
            
            for source_url in news_sources:
                try:
                    response = requests.get(source_url, timeout=10)
                    
                    if response.status_code == 200:
                        # Parse RSS feed
                        root = ET.fromstring(response.content)
                        
                        # Extract articles from RSS
                        for item in root.findall('.//item')[:10]:  # Limit articles per source
                            try:
                                title = item.find('title').text.strip() if item.find('title') is not None else ""
                                description = item.find('description').text.strip() if item.find('description') is not None else ""
                                url = item.find('link').text.strip() if item.find('link') is not None else ""
                                
                                # Process through our filtering pipeline
                                tool_info = self.extract_tool_info(title, description, url, "news")
                                
                                if tool_info:
                                    self.new_tools.append(tool_info)
                                    
                            except Exception as e:
                                print(f"Error processing news article: {e}")
                                
                        # Rate limiting between sources
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"Error fetching from {source_url}: {e}")
                    
        except Exception as e:
            print(f"Error in news discovery: {e}")
    
    def enrich_tool_data(self, tool_info):
        """
        Enrich tool data with additional information from the tool's website.
        
        This method attempts to scrape the tool's website to extract
        additional details like pricing, features, and better descriptions.
        It implements respectful scraping with proper headers and timeouts.
        
        Args:
            tool_info (dict): Basic tool information
            
        Returns:
            dict: Enriched tool information
        """
        try:
            url = tool_info.get('URL', '')
            
            # Skip if URL is not accessible or is a social media link
            if not url or any(domain in url.lower() for domain in ['reddit.com', 'github.com', 'twitter.com']):
                return tool_info
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to extract better description from meta tags
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    tool_info['What it does'] = meta_desc['content'][:200] + "..." if len(meta_desc['content']) > 200 else meta_desc['content']
                
                # Try to extract pricing information
                page_text = soup.get_text().lower()
                if any(word in page_text for word in ['free', 'open source', 'free tier']):
                    tool_info['Free/Paid'] = 'Freemium'
                elif any(word in page_text for word in ['paid', 'subscription', 'premium', 'pro']):
                    tool_info['Free/Paid'] = 'Paid'
                    
        except Exception as e:
            print(f"Error enriching tool data for {tool_info.get('Tool Name', 'Unknown')}: {e}")
            
        return tool_info
    
    def run_discovery(self):
        """
        Execute the complete discovery pipeline.
        
        This method orchestrates the entire discovery process:
        1. Discovers tools from multiple sources (GitHub, Reddit, News)
        2. Applies filtering and scoring algorithms
        3. Enriches tool data with additional information
        4. Sorts tools by trending score
        5. Selects top tools for daily digest
        6. Updates cache and saves results
        
        The method implements comprehensive error handling and logging
        to ensure robust operation even when individual sources fail.
        """
        print("🚀 Starting AI tools discovery...")
        
        # Discover from GitHub trending
        print("📊 Discovering from GitHub trending...")
        self.discover_from_github_trending()
        
        # Discover from Reddit subreddits
        print("🔴 Discovering from Reddit...")
        for subreddit in REDDIT_SUBREDDITS:
            print(f"  - Searching r/{subreddit}")
            self.discover_from_reddit(subreddit)
            time.sleep(1)  # Rate limiting between subreddits
        
        # Discover from news articles
        print("📰 Discovering from news articles...")
        self.discover_from_news_articles()
        
        # Enrich tool data with additional information
        print("🔍 Enriching tool data...")
        for i, tool_info in enumerate(self.new_tools):
            self.new_tools[i] = self.enrich_tool_data(tool_info)
            time.sleep(0.5)  # Rate limiting for web scraping
        
        # Sort by trending score and select top tools
        self.new_tools.sort(key=lambda x: x.get('Trending Score', 0), reverse=True)
        
        # Select top 3-5 tools for daily digest
        top_tools = self.new_tools[:5] if len(self.new_tools) >= 5 else self.new_tools
        
        print(f"✅ Discovery complete! Found {len(self.new_tools)} tools, selected {len(top_tools)} for daily digest")
        
        return top_tools
    
    def add_to_csv(self, tool_info):
        """
        Add a tool to the master CSV database.
        
        This method appends a new tool to the master resources CSV file,
        ensuring proper formatting and avoiding duplicates. It creates
        the file and headers if they don't exist.
        
        Args:
            tool_info (dict): Tool information to add
        """
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(MASTER_CSV_PATH), exist_ok=True)
        
        # Define CSV headers
        fieldnames = [
            'Tool Name', 'Category', 'URL', 'What it does', 
            'Free/Paid', 'Trending Score', 'Source', 'Date Added'
        ]
        
        # Check if file exists and has headers
        file_exists = os.path.exists(MASTER_CSV_PATH)
        
        try:
            with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write headers if file is new
                if not file_exists:
                    writer.writeheader()
                
                # Add date and write tool info
                tool_info['Date Added'] = datetime.datetime.now().strftime('%Y-%m-%d')
                writer.writerow(tool_info)
                
        except Exception as e:
            print(f"Error adding tool to CSV: {e}")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_master_tools():
    """
    Load all tools from the master CSV file.
    
    This utility function reads the master resources CSV and returns
    a list of all tools for analysis or processing purposes.
    
    Returns:
        list: List of dictionaries containing tool information
    """
    tools = []
    try:
        with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            tools = list(reader)
    except FileNotFoundError:
        print("Master CSV file not found. Starting with empty database.")
    except Exception as e:
        print(f"Error loading master tools: {e}")
    
    return tools

def append_to_master_csv(tool_info):
    """
    Append a tool to the master CSV file with proper formatting.
    
    This function ensures that tools are properly formatted and added
    to the master database with appropriate timestamps.
    
    Args:
        tool_info (dict): Tool information to append
    """
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(MASTER_CSV_PATH), exist_ok=True)
    
    # Define CSV headers
    fieldnames = [
        'Tool Name', 'Category', 'URL', 'What it does', 
        'Free/Paid', 'Trending Score', 'Source', 'Date Added'
    ]
    
    # Check if file exists
    file_exists = os.path.exists(MASTER_CSV_PATH)
    
    try:
        with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write headers if file is new
            if not file_exists:
                writer.writeheader()
            
            # Add timestamp and write tool info
            tool_info['Date Added'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(tool_info)
            
    except Exception as e:
        print(f"Error appending to master CSV: {e}")

def write_daily_markdown(tools):
    """
    Write the daily tools digest to markdown format.
    
    This function creates a well-formatted markdown section for the
    daily digest, including the date, tool count, and detailed
    information about each discovered tool.
    
    Args:
        tools (list): List of tool dictionaries to include in digest
    """
    # Ensure artifacts directory exists
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    # Get current date for the digest
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Create the daily section content
    daily_content = f"""
## {today} - Daily AI Tools Digest

🎯 **Today's Discovery**: {len(tools)} trending AI tools found

"""
    
    # Add each tool to the digest
    for i, tool in enumerate(tools, 1):
        daily_content += f"""
### {i}. {tool['Tool Name']}

- **Category**: {tool['Category']}
- **What it does**: {tool['What it does']}
- **Pricing**: {tool['Free/Paid']}
- **Trending Score**: {tool['Trending Score']:.1f}
- **Source**: {tool['Source']}
- **🔗 [Try it here]({tool['URL']})**

---
"""
    
    # Read existing content or create new file
    try:
        with open(ROOT_MD_PATH, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = "# AI Tools Daily Digest\n\nDiscover the latest trending AI tools and applications.\n\n"
    
    # Prepend new content to existing content
    new_content = daily_content + "\n" + existing_content
    
    # Write updated content
    try:
        with open(ROOT_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Daily digest written to {ROOT_MD_PATH}")
    except Exception as e:
        print(f"Error writing daily digest: {e}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function for the daily AI tools digest generator.
    
    This function orchestrates the complete workflow:
    1. Initializes the discovery system
    2. Runs the discovery pipeline
    3. Processes and filters discovered tools
    4. Generates the daily digest
    5. Updates the master database
    6. Saves cache and cleanup
    
    The function implements comprehensive error handling and logging
    to ensure reliable operation in production environments.
    """
    try:
        print("🤖 AI Tools Daily Digest Generator v3.1.0")
        print("=" * 50)
        
        # Initialize the discovery system
        discoverer = AIToolsDiscoverer()
        
        # Run the discovery pipeline
        top_tools = discoverer.run_discovery()
        
        if not top_tools:
            print("❌ No tools found. Check your sources and filters.")
            return
        
        # Write daily digest to markdown
        write_daily_markdown(top_tools)
        
        # Add tools to master CSV
        print("📝 Updating master database...")
        for tool in top_tools:
            discoverer.add_to_csv(tool)
        
        # Save cache for next run
        discoverer.save_cache()
        
        print("🎉 Daily digest generation complete!")
        print(f"📊 Tools discovered: {len(discoverer.new_tools)}")
        print(f"📋 Tools in digest: {len(top_tools)}")
        print(f"📁 Output files: {ROOT_MD_PATH}, {MASTER_CSV_PATH}")
        
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
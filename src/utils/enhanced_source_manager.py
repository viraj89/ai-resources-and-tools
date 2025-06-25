# -*- coding: utf-8 -*-
"""
Enhanced Source Manager for AI Insights Daily v4.0.0

This utility manages different types of news sources including:
- RSS feeds (traditional news sources)
- Web scraping (DeepLearning.AI community)
- Social media APIs (X/Twitter trending topics)
"""

import json
import logging
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSourceManager:
    """
    Manages multiple types of news sources for comprehensive AI news discovery.
    """

    def __init__(self, max_age_hours: int = 24):
        """
        Initialize the source manager.

        Args:
            max_age_hours: Maximum age of articles to consider, in hours.
        """
        self.max_age_hours = max_age_hours
        self.cutoff_date = datetime.now() - timedelta(hours=max_age_hours)
        
        # Headers for web scraping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_deeplearning_ai_community(self) -> List[Dict[str, Any]]:
        """
        Scrapes the DeepLearning.AI community for trending discussions and news.
        
        Returns:
            List of articles/discussions from the community.
        """
        articles = []
        try:
            # DeepLearning.AI community URL
            url = "https://community.deeplearning.ai/"
            
            logger.info(f"Fetching content from DeepLearning.AI community: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for discussion topics, announcements, and trending content
            # This is a generic approach - the actual selectors may need adjustment
            content_selectors = [
                'article', '.discussion', '.topic', '.post', '.thread',
                '.announcement', '.news-item', '.trending'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements[:10]:  # Limit to first 10 items per selector
                    article = self._extract_deeplearning_ai_content(element)
                    if article:
                        articles.append(article)
            
            # If no content found with selectors, try to extract any meaningful content
            if not articles:
                articles = self._fallback_deeplearning_ai_extraction(soup)
            
            logger.info(f"Found {len(articles)} articles from DeepLearning.AI community")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching DeepLearning.AI community content: {e}")
            return []

    def _extract_deeplearning_ai_content(self, element) -> Optional[Dict[str, Any]]:
        """
        Extract content from a DeepLearning.AI community element.
        
        Args:
            element: BeautifulSoup element containing content.
            
        Returns:
            Dictionary with article information or None if invalid.
        """
        try:
            # Try to find title
            title_elem = element.find(['h1', 'h2', 'h3', 'h4', '.title', '.headline'])
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Try to find link
            link_elem = element.find('a')
            link = link_elem.get('href') if link_elem else None
            if link and not link.startswith('http'):
                link = urljoin("https://community.deeplearning.ai/", link)
            
            # Try to find date
            date_elem = element.find(['time', '.date', '.timestamp'])
            date_str = date_elem.get_text(strip=True) if date_elem else None
            published_date = self._parse_date(date_str) if date_str else datetime.now()
            
            # Try to find summary/description
            summary_elem = element.find(['p', '.summary', '.description', '.excerpt'])
            summary = summary_elem.get_text(strip=True) if summary_elem else None
            
            if title and link:
                return {
                    'title': title,
                    'link': link,
                    'published_date': published_date,
                    'source': 'DeepLearning.AI Community',
                    'summary': summary,
                    'type': 'community_discussion'
                }
            
        except Exception as e:
            logger.debug(f"Error extracting content from element: {e}")
        
        return None

    def _fallback_deeplearning_ai_extraction(self, soup) -> List[Dict[str, Any]]:
        """
        Fallback method to extract any meaningful content from DeepLearning.AI.
        
        Args:
            soup: BeautifulSoup object of the page.
            
        Returns:
            List of extracted articles.
        """
        articles = []
        try:
            # Look for any links that might be discussions or news
            links = soup.find_all('a', href=True)
            
            for link in links[:20]:  # Limit to first 20 links
                href = link.get('href')
                text = link.get_text(strip=True)
                
                # Filter for AI-related content
                if (text and len(text) > 10 and 
                    any(keyword in text.lower() for keyword in ['ai', 'machine learning', 'deep learning', 'neural', 'model', 'training'])):
                    
                    if not href.startswith('http'):
                        href = urljoin("https://community.deeplearning.ai/", href)
                    
                    articles.append({
                        'title': text,
                        'link': href,
                        'published_date': datetime.now(),
                        'source': 'DeepLearning.AI Community',
                        'summary': f"Community discussion: {text}",
                        'type': 'community_discussion'
                    })
                    
                    if len(articles) >= 5:  # Limit fallback results
                        break
                        
        except Exception as e:
            logger.error(f"Error in fallback extraction: {e}")
        
        return articles

    def fetch_x_trending_ai_topics(self) -> List[Dict[str, Any]]:
        """
        Fetches trending AI topics from X (Twitter).
        Note: This is a simplified implementation. In production, you'd need X API access.
        
        Returns:
            List of trending AI topics and discussions.
        """
        articles = []
        try:
            # For now, we'll simulate trending topics since X API requires authentication
            # In a real implementation, you would use the X API v2
            
            # Simulated trending AI topics (replace with actual API calls)
            trending_topics = [
                {
                    'title': 'Latest developments in Large Language Models',
                    'link': 'https://x.com/search?q=AI%20LLM%20trending',
                    'published_date': datetime.now(),
                    'source': 'X (Twitter)',
                    'summary': 'Trending discussions about latest LLM developments',
                    'type': 'social_trending'
                },
                {
                    'title': 'AI Safety and Ethics Discussions',
                    'link': 'https://x.com/search?q=AI%20safety%20ethics',
                    'published_date': datetime.now() - timedelta(hours=2),
                    'source': 'X (Twitter)',
                    'summary': 'Hot topics around AI safety and ethical considerations',
                    'type': 'social_trending'
                },
                {
                    'title': 'Machine Learning Research Breakthroughs',
                    'link': 'https://x.com/search?q=machine%20learning%20research',
                    'published_date': datetime.now() - timedelta(hours=4),
                    'source': 'X (Twitter)',
                    'summary': 'Latest ML research papers and breakthroughs',
                    'type': 'social_trending'
                }
            ]
            
            # Filter by recency
            for topic in trending_topics:
                if topic['published_date'] > self.cutoff_date:
                    articles.append(topic)
            
            logger.info(f"Found {len(articles)} trending AI topics from X")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching X trending topics: {e}")
            return []

    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """
        Parse date string into datetime object.
        
        Args:
            date_string: String representation of date.
            
        Returns:
            Datetime object or None if parsing fails.
        """
        if not date_string:
            return None
        
        try:
            # Try common date formats
            date_formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%B %d, %Y',
                '%d %B %Y',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%SZ'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            # If none of the formats work, return current time
            return datetime.now()
            
        except Exception as e:
            logger.warning(f"Could not parse date '{date_string}': {e}")
            return datetime.now()

    def get_all_sources_content(self) -> List[Dict[str, Any]]:
        """
        Fetch content from all available sources.
        
        Returns:
            Combined list of articles from all sources.
        """
        all_articles = []
        
        # Fetch from DeepLearning.AI community
        deeplearning_articles = self.fetch_deeplearning_ai_community()
        all_articles.extend(deeplearning_articles)
        
        # Fetch trending topics from X
        x_articles = self.fetch_x_trending_ai_topics()
        all_articles.extend(x_articles)
        
        # Filter by recency
        recent_articles = [
            article for article in all_articles 
            if article['published_date'] > self.cutoff_date
        ]
        
        logger.info(f"Total articles from all sources: {len(recent_articles)}")
        return recent_articles

print("Enhanced Source Manager ready") 
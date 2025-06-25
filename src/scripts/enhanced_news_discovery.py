# -*- coding: utf-8 -*-
"""
Enhanced News Discovery Script for AI Insights Daily v4.0.0
- Integrates multiple news sources with robust date validation
- Applies freshness scoring and fallback mechanisms
- Outputs only 24h-fresh news articles

This script orchestrates the news discovery process. It leverages the
EnhancedRSSParser to fetch recent articles and the FreshnessScorer to
rank them based on timeliness and relevance.
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from operator import itemgetter

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.enhanced_rss_parser import EnhancedRSSParser
from src.utils.freshness_scorer import FreshnessScorer
from src.utils.enhanced_source_manager import EnhancedSourceManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedNewsDiscovery:
    """
    Orchestrates the discovery, scoring, and ranking of fresh news articles.
    """

    def __init__(self, cache_dir: str = "data/cache", max_age_hours: int = 24):
        """
        Initializes the news discovery system.

        Args:
            cache_dir: Directory for caching data.
            max_age_hours: Maximum age of articles to consider, in hours.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.rss_parser = EnhancedRSSParser(max_age_hours=max_age_hours)
        self.freshness_scorer = FreshnessScorer(max_age_hours=max_age_hours)
        self.source_manager = EnhancedSourceManager(max_age_hours=max_age_hours)
        self.freshness_cutoff = datetime.now() - timedelta(hours=max_age_hours)

        self.primary_sources = {
            "TechCrunch": {
                "url": "https://techcrunch.com/feed/",
                "weight": 1.0,
                "keywords": ["ai", "artificial intelligence", "machine learning", "startup", "funding"]
            },
            "VentureBeat": {
                "url": "https://venturebeat.com/feed/",
                "weight": 1.0,
                "keywords": ["ai", "artificial intelligence", "machine learning", "data", "deep learning"]
            },
            "Ars Technica": {
                "url": "http://feeds.arstechnica.com/arstechnica/index",
                "weight": 0.9,
                "keywords": ["ai", "robotics", "science", "technology"]
            }
        }

        # New sources with their weights and keywords
        self.new_sources = {
            "DeepLearning.AI Community": {
                "weight": 1.2,  # Higher weight for community insights
                "keywords": ["ai", "machine learning", "deep learning", "neural networks", "training", "models"]
            },
            "X (Twitter) Trending": {
                "weight": 0.8,  # Lower weight for social media content
                "keywords": ["ai", "artificial intelligence", "machine learning", "llm", "gpt", "research"]
            }
        }

    def discover_fresh_news(self, max_articles: int = 15) -> dict:
        """
        Discovers, scores, and ranks fresh news articles from all sources.

        Args:
            max_articles: The maximum number of articles to return.

        Returns:
            A dictionary containing the ranked articles and discovery metadata.
        """
        logger.info("Starting enhanced news discovery...")
        all_articles = []

        # Fetch from traditional RSS sources
        for source_name, source_info in self.primary_sources.items():
            logger.info(f"Fetching articles from {source_name}...")
            articles = self.rss_parser.fetch_and_parse(source_info['url'])

            for article in articles:
                freshness_score = self.freshness_scorer.calculate_freshness_score(article['published_date'])
                relevance_score = self.freshness_scorer.calculate_relevance_score(article['title'], source_info['keywords'])
                
                # Combine scores with source weight
                weighted_score = (freshness_score * 0.6 + relevance_score * 0.4) * source_info['weight']

                article['scores'] = {
                    'freshness': freshness_score,
                    'relevance': relevance_score,
                    'overall': weighted_score
                }
                # Ensure source is correctly attributed from our config
                article['source'] = source_name
                article['type'] = 'rss_feed'
                all_articles.append(article)

        # Fetch from new sources (DeepLearning.AI Community and X Trending)
        logger.info("Fetching content from new sources...")
        new_source_articles = self.source_manager.get_all_sources_content()
        
        for article in new_source_articles:
            source_name = article['source']
            source_info = self.new_sources.get(source_name, {
                "weight": 1.0,
                "keywords": ["ai", "artificial intelligence", "machine learning"]
            })
            
            freshness_score = self.freshness_scorer.calculate_freshness_score(article['published_date'])
            relevance_score = self.freshness_scorer.calculate_relevance_score(article['title'], source_info['keywords'])
            
            # Combine scores with source weight
            weighted_score = (freshness_score * 0.6 + relevance_score * 0.4) * source_info['weight']

            article['scores'] = {
                'freshness': freshness_score,
                'relevance': relevance_score,
                'overall': weighted_score
            }
            all_articles.append(article)

        # Sort articles by the overall score in descending order
        all_articles.sort(key=lambda x: x['scores']['overall'], reverse=True)

        result = {
            'articles': all_articles[:max_articles],
            'total_found': len(all_articles),
            'total_returned': min(len(all_articles), max_articles),
            'sources_checked': list(self.primary_sources.keys()) + list(self.new_sources.keys()),
            'discovery_time': datetime.now().isoformat(),
            'freshness_cutoff': self.freshness_cutoff.isoformat()
        }

        logger.info(f"News discovery completed. Found {len(all_articles)} articles, returning top {len(result['articles'])}.")
        return result

def main():
    """
    Main function to run the enhanced news discovery process and display results.
    """
    try:
        news_discovery = EnhancedNewsDiscovery()
        result = news_discovery.discover_fresh_news(max_articles=15)

        print("\n=== Enhanced News Discovery Results ===")
        print(f"Total articles found: {result['total_found']}")
        print(f"Top articles returned: {result['total_returned']}")
        print(f"Sources checked: {', '.join(result['sources_checked'])}")
        print(f"Discovery time: {result['discovery_time']}")
        print(f"Freshness cutoff: {result['freshness_cutoff']}")

        print("\n=== Top Articles ===")
        if not result['articles']:
            print("No recent articles found matching the criteria.")
        else:
            for i, article in enumerate(result['articles'], 1):
                pub_date_str = article['published_date'].strftime('%Y-%m-%d %H:%M')
                source_type = article.get('type', 'unknown')
                print(f"{i}. {article['title']}")
                print(f"   Source: {article['source']} ({source_type}) | Published: {pub_date_str}")
                print(f"   Scores: Overall={article['scores']['overall']:.3f}, Freshness={article['scores']['freshness']:.3f}, Relevance={article['scores']['relevance']:.3f}")
                if article.get('summary'):
                    print(f"   Summary: {article['summary'][:100]}...")
                print(f"   Link: {article['link']}")
                print()

        print("News discovery process completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred during the news discovery process: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 
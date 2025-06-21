# -*- coding: utf-8 -*-
"""
Enhanced News Discovery Script for AI Insights Daily v4.0.0

This script orchestrates the news discovery process. It uses mock utility
classes to simulate fetching, scoring, and ranking news articles. This approach
allows for end-to-end testing of the main pipeline while the actual utility
logic is being developed.
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.enhanced_rss_parser import EnhancedRSSParser
from utils.freshness_scorer import FreshnessScorer

# Configure logging to display informational messages.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedNewsDiscovery:
    """
    Orchestrates the discovery of fresh news articles from various sources.
    
    This class integrates the RSS parser and freshness scorer to create a
    ranked list of recent news. It is currently configured to use mock data
    for demonstration and testing purposes.
    """
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initializes the news discovery system.
        
        Args:
            cache_dir: The directory to use for caching news data.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components. These are currently mock classes.
        self.rss_parser = EnhancedRSSParser()
        self.freshness_scorer = FreshnessScorer()
        
        # News sources configuration (for demonstration).
        self.primary_sources = {
            "techcrunch": {
                "url": "https://techcrunch.com/feed/",
                "weight": 1.0,
                "keywords": ["AI", "artificial intelligence", "machine learning", "startup", "tech"]
            },
            "venturebeat": {
                "url": "https://venturebeat.com/feed/",
                "weight": 1.0,
                "keywords": ["AI", "artificial intelligence", "machine learning", "startup"]
            }
        }
    
    def discover_fresh_news(self, max_articles: int = 10) -> dict:
        """
        Discovers fresh news articles using the integrated components.
        
        This method currently uses a hardcoded list of articles for testing
        and does not perform live data fetching.
        
        Args:
            max_articles: The maximum number of articles to return.
            
        Returns:
            A dictionary containing the discovered articles and metadata.
        """
        logger.info("Starting enhanced news discovery...")
        
        # Mock data for testing the pipeline.
        mock_articles = [
            {
                'title': 'AI Breakthrough in Machine Learning',
                'link': 'https://example.com/ai-breakthrough',
                'description': 'New advances in AI technology',
                'source': 'techcrunch',
                'scores': {'overall': 0.9}
            },
            {
                'title': 'Startup Raises $10M for AI Platform',
                'link': 'https://example.com/startup-funding',
                'description': 'Innovative AI startup secures funding',
                'source': 'venturebeat',
                'scores': {'overall': 0.8}
            }
        ]
        
        # Prepare the result dictionary.
        result = {
            'articles': mock_articles[:max_articles],
            'total_found': len(mock_articles),
            'total_returned': min(len(mock_articles), max_articles),
            'sources_checked': list(self.primary_sources.keys()),
            'discovery_time': datetime.now().isoformat(),
            'freshness_cutoff': (datetime.now() - timedelta(hours=24)).isoformat()
        }
        
        logger.info(f"News discovery completed. Found {len(result['articles'])} articles.")
        return result

def main():
    """
    Main function to run the enhanced news discovery process.
    
    This function initializes the `EnhancedNewsDiscovery` class and
    runs the news discovery process, printing the results to the console.
    """
    try:
        # Initialize the main news discovery class.
        news_discovery = EnhancedNewsDiscovery()
        
        # Discover fresh news with a limit of 5 articles.
        logger.info("Starting enhanced news discovery...")
        result = news_discovery.discover_fresh_news(max_articles=5)
        
        # Print summary
        print(f"\n=== Enhanced News Discovery Results ===")
        print(f"Total articles found: {result['total_found']}")
        print(f"Top articles returned: {result['total_returned']}")
        print(f"Sources checked: {', '.join(result['sources_checked'])}")
        print(f"Discovery time: {result['discovery_time']}")
        
        # Print top articles
        print(f"\n=== Top Articles ===")
        for i, article in enumerate(result['articles'], 1):
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Score: {article['scores']['overall']:.3f}")
            print(f"   Link: {article['link']}")
            print()
        
        print(f"\nNews discovery completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # This ensures the main function is called only when the script is executed directly.
    main() 
# -*- coding: utf-8 -*-
"""
Enhanced RSS Parser for AI Insights Daily v4.0.0

This utility fetches and parses RSS feeds, extracting key information
from articles published within the last 24 hours. It uses the `feedparser`
and `dateutil` libraries to handle feed and date processing.
"""

import feedparser
import logging
from datetime import datetime, timedelta
from dateutil import parser as date_parser

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedRSSParser:
    """
    Fetches and parses RSS feeds to extract recent articles.

    This class connects to a given RSS feed URL, parses the content,
    and returns a list of articles that were published within a defined
    time window (defaulting to the last 24 hours).
    """

    def __init__(self, max_age_hours: int = 24):
        """
        Initializes the parser with a maximum article age.

        Args:
            max_age_hours: The maximum age of articles in hours to be considered recent.
        """
        self.max_age_hours = max_age_hours
        logger.info(f"Enhanced RSS Parser initialized to fetch articles up to {max_age_hours} hours old.")

    def fetch_and_parse(self, url: str) -> list:
        """
        Fetches an RSS feed and parses it to find recent articles.

        Args:
            url: The URL of the RSS feed.

        Returns:
            A list of dictionaries, where each dictionary represents an article
            with 'title', 'link', and 'published_date' keys.
        """
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                logger.warning(f"Warning: Malformed feed at {url}. Reason: {feed.bozo_exception}")

            articles = []
            now = datetime.now()
            cutoff_date = now - timedelta(hours=self.max_age_hours)

            for entry in feed.entries:
                published_date = self._parse_date(entry.get('published') or entry.get('updated'))

                if published_date and published_date > cutoff_date:
                    articles.append({
                        'title': entry.get('title', 'No Title'),
                        'link': entry.get('link', ''),
                        'published_date': published_date,
                        'source': feed.feed.get('title', 'Unknown Source')
                    })

            logger.info(f"Found {len(articles)} recent articles from {url}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching or parsing RSS feed at {url}: {e}")
            return []

    def _parse_date(self, date_string: str):
        """
        Safely parses a date string into a datetime object.

        Args:
            date_string: The string representation of the date.

        Returns:
            A datetime object or None if parsing fails.
        """
        if not date_string:
            return None
        try:
            # The ignoretz=True flag helps in standardizing timezone-naive dates
            return date_parser.parse(date_string, ignoretz=True)
        except (ValueError, OverflowError) as e:
            logger.warning(f"Could not parse date '{date_string}': {e}")
            return None

print("Enhanced RSS Parser ready")
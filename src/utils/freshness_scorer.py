# -*- coding: utf-8 -*-
"""
Freshness Scorer for AI Insights Daily v4.0.0

This utility calculates freshness and relevance scores for news articles.
Freshness is determined by the article's publication date, while relevance
is based on the presence of predefined keywords in the title.
"""

import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FreshnessScorer:
    """
    Calculates scores for news articles based on freshness and relevance.
    """

    def __init__(self, max_age_hours: int = 24):
        """
        Initializes the scorer with a maximum article age for scoring.

        Args:
            max_age_hours: The maximum age in hours for an article to be scored.
        """
        self.max_age_hours = max_age_hours
        logger.info(f"Freshness Scorer initialized for articles up to {max_age_hours} hours old.")

    def calculate_freshness_score(self, published_date: datetime) -> float:
        """
        Calculates a freshness score based on the article's publication date.

        The score is normalized between 0.0 (oldest) and 1.0 (newest) using
        a linear decay function.

        Args:
            published_date: The publication date of the article as a datetime object.

        Returns:
            A freshness score between 0.0 and 1.0.
        """
        if not isinstance(published_date, datetime):
            logger.warning("Invalid type for published_date. Expected datetime.")
            return 0.0

        now = datetime.now()
        age_delta = now - published_date
        age_in_hours = age_delta.total_seconds() / 3600

        if age_in_hours > self.max_age_hours or age_in_hours < 0:
            return 0.0

        # Linear decay for freshness score
        score = 1.0 - (age_in_hours / self.max_age_hours)
        return max(0.0, score)

    def calculate_relevance_score(self, title: str, keywords: list) -> float:
        """
        Calculates a relevance score based on keyword matches in the title.

        The score is the ratio of unique matched keywords to the total number of
        keywords provided. The match is case-insensitive.

        Args:
            title: The title of the article.
            keywords: A list of keywords to search for.

        Returns:
            A relevance score between 0.0 and 1.0.
        """
        if not title or not keywords:
            return 0.0

        title_lower = title.lower()
        matched_keywords = {keyword for keyword in keywords if keyword.lower() in title_lower}
        
        score = len(matched_keywords) / len(keywords)
        return min(1.0, score)

print("Freshness Scorer ready") 
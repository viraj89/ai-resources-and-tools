# -*- coding: utf-8 -*-
"""
Research Discovery Script for AI Insights Daily v4.0.0

This script discovers and ranks academic papers from sources like arXiv,
Google Scholar, and other research repositories. It focuses on AI/ML papers
published in the last 30 days and ranks them by relevance and impact.
"""

import json
import logging
import sys
import requests
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchDiscovery:
    """
    Discovers and ranks academic papers from various research sources.
    """
    
    def __init__(self, cache_dir: str = "data/cache", max_age_days: int = 30):
        """
        Initializes the research discovery system.
        
        Args:
            cache_dir: Directory for caching research data.
            max_age_days: Maximum age of papers to consider, in days.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_days = max_age_days
        # Make cutoff_date timezone-aware to match arXiv dates
        self.cutoff_date = datetime.now(timezone.utc) - timedelta(days=max_age_days)
        
        # Research sources configuration
        self.research_sources = {
            "arXiv": {
                "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=50",
                "weight": 1.0,
                "keywords": ["artificial intelligence", "machine learning", "deep learning", "neural networks", "transformer", "llm", "large language model"]
            },
            "Papers With Code": {
                "url": "https://paperswithcode.com/api/v1/papers/?items_per_page=50&ordering=-published",
                "weight": 0.9,
                "keywords": ["ai", "ml", "deep learning", "neural", "transformer", "llm"]
            }
        }
        
        # AI/ML research keywords for relevance scoring
        self.ai_keywords = [
            "artificial intelligence", "machine learning", "deep learning", "neural networks",
            "transformer", "large language model", "llm", "gpt", "bert", "attention",
            "computer vision", "natural language processing", "nlp", "reinforcement learning",
            "generative ai", "diffusion", "gan", "autoencoder", "clustering", "classification",
            "regression", "optimization", "gradient descent", "backpropagation", "convolutional",
            "recurrent", "lstm", "gru", "attention mechanism", "self-attention", "multi-head"
        ]
    
    def fetch_arxiv_papers(self) -> list:
        """
        Fetches recent AI/ML papers from arXiv.
        
        Returns:
            List of paper dictionaries with metadata.
        """
        papers = []
        try:
            response = requests.get(self.research_sources["arXiv"]["url"], timeout=30)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                # Parse arXiv XML response
                for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                    try:
                        # Extract paper metadata
                        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text.strip()
                        summary = entry.find('.//{http://www.w3.org/2005/Atom}summary').text.strip()
                        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
                        paper_id = entry.find('.//{http://www.w3.org/2005/Atom}id').text
                        
                        # Parse publication date
                        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        
                        if pub_date > self.cutoff_date:
                            # Calculate relevance score
                            relevance_score = self.calculate_relevance_score(title + " " + summary)
                            
                            papers.append({
                                'title': title,
                                'summary': summary,
                                'published_date': pub_date,
                                'paper_id': paper_id,
                                'url': paper_id,
                                'source': 'arXiv',
                                'relevance_score': relevance_score,
                                'impact_score': self.calculate_impact_score(title, summary)
                            })
                    
                    except Exception as e:
                        logger.warning(f"Error parsing arXiv entry: {e}")
                        continue
            
            logger.info(f"Fetched {len(papers)} recent papers from arXiv")
            
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {e}")
        
        return papers
    
    def fetch_papers_with_code(self) -> list:
        """
        Fetches recent papers from Papers With Code API.
        
        Returns:
            List of paper dictionaries with metadata.
        """
        papers = []
        try:
            response = requests.get(self.research_sources["Papers With Code"]["url"], timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                for paper in data.get('results', []):
                    try:
                        title = paper.get('title', '')
                        abstract = paper.get('abstract', '')
                        published = paper.get('published', '')
                        paper_id = paper.get('id', '')
                        
                        if published:
                            pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                            
                            if pub_date > self.cutoff_date:
                                # Calculate relevance score
                                relevance_score = self.calculate_relevance_score(title + " " + abstract)
                                
                                papers.append({
                                    'title': title,
                                    'summary': abstract,
                                    'published_date': pub_date,
                                    'paper_id': paper_id,
                                    'url': f"https://paperswithcode.com/paper/{paper_id}",
                                    'source': 'Papers With Code',
                                    'relevance_score': relevance_score,
                                    'impact_score': self.calculate_impact_score(title, abstract)
                                })
                    
                    except Exception as e:
                        logger.warning(f"Error parsing Papers With Code entry: {e}")
                        continue
            
            logger.info(f"Fetched {len(papers)} recent papers from Papers With Code")
            
        except Exception as e:
            logger.error(f"Error fetching from Papers With Code: {e}")
        
        return papers
    
    def calculate_relevance_score(self, text: str) -> float:
        """
        Calculates relevance score based on AI/ML keyword presence.
        
        Args:
            text: The text to analyze.
            
        Returns:
            Relevance score between 0.0 and 1.0.
        """
        if not text:
            return 0.0
        
        text_lower = text.lower()
        matched_keywords = sum(1 for keyword in self.ai_keywords if keyword.lower() in text_lower)
        
        # Normalize score based on number of keywords found
        score = min(1.0, matched_keywords / 5.0)  # Cap at 5 keywords for full score
        return score
    
    def calculate_impact_score(self, title: str, summary: str) -> float:
        """
        Calculates impact score based on paper characteristics.
        
        Args:
            title: Paper title.
            summary: Paper abstract/summary.
            
        Returns:
            Impact score between 0.0 and 1.0.
        """
        score = 0.5  # Base score
        
        text = (title + " " + summary).lower()
        
        # Boost for important keywords
        important_terms = [
            "novel", "new", "improved", "better", "state-of-the-art", "sota",
            "breakthrough", "advance", "innovation", "propose", "introduce"
        ]
        
        for term in important_terms:
            if term in text:
                score += 0.1
        
        # Boost for technical depth
        technical_terms = [
            "architecture", "framework", "model", "algorithm", "methodology",
            "experiment", "evaluation", "benchmark", "dataset", "implementation"
        ]
        
        for term in technical_terms:
            if term in text:
                score += 0.05
        
        return min(1.0, score)
    
    def discover_research_papers(self, max_papers: int = 15) -> dict:
        """
        Discovers and ranks research papers from all sources.
        
        Args:
            max_papers: Maximum number of papers to return.
            
        Returns:
            Dictionary containing ranked papers and discovery metadata.
        """
        logger.info("Starting research paper discovery...")
        all_papers = []
        
        # Fetch from arXiv
        arxiv_papers = self.fetch_arxiv_papers()
        all_papers.extend(arxiv_papers)
        
        # Fetch from Papers With Code
        pwc_papers = self.fetch_papers_with_code()
        all_papers.extend(pwc_papers)
        
        # Calculate overall scores and rank
        for paper in all_papers:
            source_weight = self.research_sources[paper['source']]['weight']
            paper['overall_score'] = (paper['relevance_score'] * 0.6 + 
                                    paper['impact_score'] * 0.4) * source_weight
        
        # Sort by overall score
        all_papers.sort(key=lambda x: x['overall_score'], reverse=True)
        
        result = {
            'papers': all_papers[:max_papers],
            'total_found': len(all_papers),
            'total_returned': min(len(all_papers), max_papers),
            'sources_checked': list(self.research_sources.keys()),
            'discovery_time': datetime.now().isoformat(),
            'cutoff_date': self.cutoff_date.isoformat()
        }
        
        logger.info(f"Research discovery completed. Found {len(all_papers)} papers, returning top {len(result['papers'])}.")
        return result

def main():
    """
    Main function to run the research discovery process and display results.
    """
    try:
        research_discovery = ResearchDiscovery()
        result = research_discovery.discover_research_papers(max_papers=15)
        
        print("\n=== Research Paper Discovery Results ===")
        print(f"Total papers found: {result['total_found']}")
        print(f"Top papers returned: {result['total_returned']}")
        print(f"Sources checked: {', '.join(result['sources_checked'])}")
        print(f"Discovery time: {result['discovery_time']}")
        print(f"Cutoff date: {result['cutoff_date']}")
        
        print("\n=== Top Research Papers ===")
        if not result['papers']:
            print("No recent research papers found matching the criteria.")
        else:
            for i, paper in enumerate(result['papers'], 1):
                pub_date_str = paper['published_date'].strftime('%Y-%m-%d')
                print(f"{i}. {paper['title']}")
                print(f"   Source: {paper['source']} | Published: {pub_date_str}")
                print(f"   Scores: Overall={paper['overall_score']:.3f}, Relevance={paper['relevance_score']:.3f}, Impact={paper['impact_score']:.3f}")
                print(f"   URL: {paper['url']}")
                print(f"   Summary: {paper['summary'][:150]}...")
                print()
        
        print("Research discovery process completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred during the research discovery process: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 
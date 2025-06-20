#!/usr/bin/env python3
"""
Keyword Learning System
- Tracks successful AI tool discoveries
- Extracts new keywords from successful tools
- Auto-updates the keyword database
- Maintains learning statistics
"""

import json
import re
import os
from datetime import datetime
from collections import Counter
import hashlib

class KeywordLearner:
    def __init__(self, config_path="data/config/keywords.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.successful_discoveries = []
        self.learning_cache = {}
        
    def load_config(self):
        """Load keyword configuration from JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Keyword config not found: {self.config_path}")
            return {}
    
    def save_config(self):
        """Save updated keyword configuration"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def record_successful_discovery(self, tool_info):
        """Record a successful tool discovery for learning"""
        discovery = {
            'tool_name': tool_info['Tool Name'],
            'category': tool_info['Category'],
            'description': tool_info['What it does'],
            'url': tool_info['URL'],
            'discovered_at': datetime.now().isoformat(),
            'confidence_score': tool_info.get('Trending Score', 0),
            'source': tool_info.get('Source', 'unknown')
        }
        
        self.successful_discoveries.append(discovery)
        print(f"📚 Learning from successful discovery: {tool_info['Tool Name']}")
    
    def extract_keywords_from_text(self, text, method="title_analysis"):
        """Extract potential keywords from text using different methods"""
        if not text:
            return []
        
        text_lower = text.lower()
        keywords = []
        
        if method == "title_analysis":
            # Extract meaningful words from title
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
            # Filter out common words
            common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an'}
            keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        elif method == "description_analysis":
            # Extract technical terms and phrases
            # Look for AI-related patterns
            ai_patterns = [
                r'\b(ai|artificial intelligence|machine learning|ml|deep learning)\b',
                r'\b(gpt|claude|llama|mistral|falcon|gemini)\b',
                r'\b(generator|creator|studio|hub|workspace|lab|kit|suite)\b',
                r'\b(api|sdk|framework|library|engine|model|service|solution)\b',
                r'\b(assistant|tool|platform|app|bot|agent)\b'
            ]
            
            for pattern in ai_patterns:
                matches = re.findall(pattern, text_lower)
                keywords.extend(matches)
        
        elif method == "url_analysis":
            # Extract keywords from URL path
            url_keywords = re.findall(r'[a-zA-Z]{3,}', text_lower)
            keywords = [kw for kw in url_keywords if len(kw) > 2]
        
        return list(set(keywords))  # Remove duplicates
    
    def analyze_successful_discoveries(self):
        """Analyze successful discoveries to extract new keywords"""
        if not self.successful_discoveries:
            return
        
        print(f"🔍 Analyzing {len(self.successful_discoveries)} successful discoveries...")
        
        # Extract keywords from all successful discoveries
        all_keywords = []
        category_keywords = {}
        
        for discovery in self.successful_discoveries:
            # Extract keywords from different parts
            title_keywords = self.extract_keywords_from_text(discovery['tool_name'], "title_analysis")
            desc_keywords = self.extract_keywords_from_text(discovery['description'], "description_analysis")
            url_keywords = self.extract_keywords_from_text(discovery['url'], "url_analysis")
            
            combined_keywords = title_keywords + desc_keywords + url_keywords
            all_keywords.extend(combined_keywords)
            
            # Track keywords by category
            category = discovery['category']
            if category not in category_keywords:
                category_keywords[category] = []
            category_keywords[category].extend(combined_keywords)
        
        # Count keyword frequency
        keyword_counts = Counter(all_keywords)
        
        # Find new keywords that aren't already in config
        existing_keywords = set()
        for category in self.config.get('categories', {}).values():
            existing_keywords.update(category)
        
        for keyword_type in self.config.get('ai_keywords', {}).values():
            existing_keywords.update(keyword_type)
        
        # Filter out existing keywords and low-frequency ones
        min_frequency = 2  # Keyword must appear at least 2 times
        new_keywords = {kw: count for kw, count in keyword_counts.items() 
                       if kw not in existing_keywords and count >= min_frequency}
        
        return new_keywords, category_keywords
    
    def suggest_new_keywords(self):
        """Suggest new keywords based on successful discoveries"""
        result = self.analyze_successful_discoveries()
        
        if not result:
            print("📝 No new keywords to suggest")
            return
        
        new_keywords, category_keywords = result
        
        if not new_keywords:
            print("📝 No new keywords to suggest")
            return
        
        print(f"💡 Found {len(new_keywords)} potential new keywords:")
        
        suggestions = {
            'general_keywords': [],
            'category_keywords': {},
            'confidence_scores': {}
        }
        
        # Suggest general keywords
        for keyword, count in sorted(new_keywords.items(), key=lambda x: x[1], reverse=True):
            if count >= 3:  # High confidence
                suggestions['general_keywords'].append(keyword)
                suggestions['confidence_scores'][keyword] = count
        
        # Suggest category-specific keywords
        for category, keywords in category_keywords.items():
            if category not in suggestions['category_keywords']:
                suggestions['category_keywords'][category] = []
            
            keyword_counts = Counter(keywords)
            for keyword, count in keyword_counts.items():
                if keyword in new_keywords and count >= 2:
                    suggestions['category_keywords'][category].append(keyword)
        
        return suggestions
    
    def auto_update_keywords(self, suggestions):
        """Automatically update keywords based on suggestions"""
        if not suggestions:
            return
        
        updated = False
        
        # Update general AI keywords
        for keyword in suggestions.get('general_keywords', []):
            if keyword not in self.config.get('ai_keywords', {}).get('technologies', []):
                self.config['ai_keywords']['technologies'].append(keyword)
                updated = True
                print(f"✅ Added general keyword: {keyword}")
        
        # Update category keywords
        for category, keywords in suggestions.get('category_keywords', {}).items():
            if category in self.config.get('categories', {}):
                for keyword in keywords:
                    if keyword not in self.config['categories'][category]:
                        self.config['categories'][category].append(keyword)
                        updated = True
                        print(f"✅ Added category keyword: {keyword} -> {category}")
        
        # Update metadata
        if updated:
            self.config['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            self.config['metadata']['auto_learned_keywords'] += len(suggestions.get('general_keywords', []))
            self.save_config()
            print(f"🔄 Updated keyword database with {len(suggestions.get('general_keywords', []))} new keywords")
        
        return updated
    
    def get_keywords_for_category(self, category):
        """Get keywords for a specific category"""
        return self.config.get('categories', {}).get(category, [])
    
    def get_all_ai_keywords(self):
        """Get all AI-related keywords"""
        all_keywords = []
        for keyword_list in self.config.get('ai_keywords', {}).values():
            all_keywords.extend(keyword_list)
        return all_keywords
    
    def get_non_tool_indicators(self):
        """Get non-tool indicators"""
        return self.config.get('non_tool_indicators', [])
    
    def get_tool_indicators(self):
        """Get tool indicators"""
        return self.config.get('ai_keywords', {}).get('tool_indicators', [])
    
    def get_learning_stats(self):
        """Get learning statistics"""
        return {
            'total_discoveries': len(self.successful_discoveries),
            'auto_learned_keywords': self.config.get('metadata', {}).get('auto_learned_keywords', 0),
            'last_updated': self.config.get('metadata', {}).get('last_updated', 'Never'),
            'config_version': self.config.get('metadata', {}).get('version', '1.0.0')
        }
    
    def reset_learning_cache(self):
        """Reset the learning cache"""
        self.successful_discoveries = []
        print("🔄 Learning cache reset")

def main():
    """Test the keyword learning system"""
    learner = KeywordLearner()
    
    # Test with some sample discoveries
    sample_discoveries = [
        {
            'Tool Name': 'RAG Studio',
            'Category': 'Search / Research',
            'What it does': 'AI-powered RAG platform for building intelligent search applications',
            'URL': 'https://ragstudio.ai',
            'Trending Score': 85,
            'Source': 'github'
        },
        {
            'Tool Name': 'VectorFlow',
            'Category': 'Business / Analytics',
            'What it does': 'Vector database management and analytics platform',
            'URL': 'https://vectorflow.com',
            'Trending Score': 78,
            'Source': 'reddit'
        }
    ]
    
    # Record discoveries
    for discovery in sample_discoveries:
        learner.record_successful_discovery(discovery)
    
    # Analyze and suggest new keywords
    suggestions = learner.suggest_new_keywords()
    
    if suggestions:
        print("\n📊 Learning Statistics:")
        stats = learner.get_learning_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Auto-update keywords
        learner.auto_update_keywords(suggestions)

if __name__ == "__main__":
    main() 
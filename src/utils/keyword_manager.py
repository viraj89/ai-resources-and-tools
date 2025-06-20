#!/usr/bin/env python3
"""
Keyword Manager - Dynamic AI Keyword Management System

This module provides a high-level interface for managing dynamic keywords
used in AI tools discovery and categorization. It integrates with the
keyword learning system to provide adaptive keyword management.

Key Features:
- Dynamic keyword access from JSON configuration
- Integration with keyword learning system
- Tool categorization and content filtering
- Keyword statistics and management utilities
- Export and import functionality

The KeywordManager class serves as the primary interface for all
keyword-related operations, providing a clean API for other modules
to access and manage keywords without direct interaction with the
underlying learning system.

Author: AI Insights Daily Team
Version: 3.1.0
Last Updated: January 2025
"""

import json
import os
from typing import List, Dict, Set
from .keyword_learner import KeywordLearner

class KeywordManager:
    """
    High-level interface for dynamic keyword management.
    
    This class provides a clean API for accessing and managing keywords
    used in AI tools discovery. It integrates with the KeywordLearner
    to provide adaptive keyword learning while maintaining a simple
    interface for other modules.
    
    The manager implements caching for performance optimization and
    provides comprehensive utilities for keyword operations including
    categorization, filtering, and statistics.
    """
    
    def __init__(self, config_path="data/config/keywords.json"):
        """
        Initialize the keyword manager with configuration.
        
        Args:
            config_path (str): Path to the JSON configuration file
        """
        self.config_path = config_path
        self.learner = KeywordLearner(config_path)
        self._cache = {}  # Cache for performance optimization
        
    def get_ai_keywords(self) -> Dict[str, List[str]]:
        """
        Get all AI keywords organized by type.
        
        Returns a dictionary where keys are keyword types (e.g., 'models',
        'companies', 'technologies') and values are lists of keywords.
        
        Returns:
            Dict[str, List[str]]: AI keywords organized by type
        """
        return self.learner.config.get('ai_keywords', {})
    
    def get_all_ai_keywords_flat(self) -> List[str]:
        """
        Get all AI keywords as a flat list for easy searching.
        
        This method implements caching to avoid repeated list flattening
        operations, improving performance for frequent keyword lookups.
        
        Returns:
            List[str]: All AI keywords as a single list
        """
        if 'all_ai_keywords' not in self._cache:
            all_keywords = []
            for keyword_list in self.get_ai_keywords().values():
                all_keywords.extend(keyword_list)
            self._cache['all_ai_keywords'] = all_keywords
        return self._cache['all_ai_keywords']
    
    def get_categories(self) -> Dict[str, List[str]]:
        """
        Get all categories and their associated keywords.
        
        Categories are used for tool classification and help organize
        discovered tools into meaningful groups.
        
        Returns:
            Dict[str, List[str]]: Categories and their keywords
        """
        return self.learner.config.get('categories', {})
    
    def get_category_keywords(self, category: str) -> List[str]:
        """
        Get keywords for a specific category.
        
        Args:
            category (str): Name of the category
            
        Returns:
            List[str]: Keywords associated with the category
        """
        return self.learner.get_keywords_for_category(category)
    
    def get_non_tool_indicators(self) -> List[str]:
        """
        Get keywords that indicate content is NOT a tool.
        
        These indicators help filter out Reddit posts, news articles,
        discussions, and other non-tool content.
        
        Returns:
            List[str]: Non-tool indicator keywords
        """
        return self.learner.get_non_tool_indicators()
    
    def get_tool_indicators(self) -> List[str]:
        """
        Get keywords that indicate content IS a tool.
        
        These indicators help identify actual AI tools and applications
        among various types of content.
        
        Returns:
            List[str]: Tool indicator keywords
        """
        return self.learner.get_tool_indicators()
    
    def is_ai_related(self, text: str) -> bool:
        """
        Check if text is AI-related using dynamic keywords.
        
        This method performs a case-insensitive search for AI keywords
        in the provided text. It's used as the primary filter for
        determining if content is relevant to AI tools discovery.
        
        Args:
            text (str): Text to analyze for AI relevance
            
        Returns:
            bool: True if text contains AI keywords, False otherwise
        """
        if not text:
            return False
        
        text_lower = text.lower()
        ai_keywords = self.get_all_ai_keywords_flat()
        
        # Check for AI keywords in the text
        for keyword in ai_keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def categorize_tool(self, title: str, description: str) -> str:
        """
        Categorize a tool based on dynamic keywords.
        
        This method analyzes the title and description of a tool to
        determine its most appropriate category. It uses a scoring
        system where each matching keyword adds points to a category,
        and the category with the highest score is selected.
        
        Args:
            title (str): Tool title
            description (str): Tool description
            
        Returns:
            str: Category name or "Other" if no clear category
        """
        text = (title + " " + description).lower()
        categories = self.get_categories()
        
        # Score each category based on keyword matches
        category_scores = {}
        for category, keywords in categories.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        # Return the highest scoring category
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "Other"
    
    def is_tool_content(self, title: str, description: str, url: str) -> bool:
        """
        Check if content represents an actual AI tool.
        
        This method implements a multi-stage filtering process:
        1. URL validation - ensures URL is accessible and not social media
        2. Non-tool indicator filtering - excludes content with non-tool keywords
        3. Tool indicator detection - identifies content with tool-specific keywords
        
        Args:
            title (str): Content title
            description (str): Content description
            url (str): Content URL
            
        Returns:
            bool: True if content is a tool, False otherwise
        """
        # Validate URL format and accessibility
        if not url or url == "N/A" or not url.startswith('http'):
            return False
        
        # Check for non-tool indicators in URL (social media, news sites, etc.)
        non_tool_indicators = self.get_non_tool_indicators()
        if any(indicator in url.lower() for indicator in non_tool_indicators):
            return False
        
        # Check for tool indicators in title
        tool_indicators = self.get_tool_indicators()
        title_lower = title.lower()
        if any(indicator in title_lower for indicator in tool_indicators):
            return True
        
        # Check for tool indicators in description
        desc_lower = description.lower()
        if any(indicator in desc_lower for indicator in tool_indicators):
            return True
        
        return False
    
    def record_successful_discovery(self, tool_info: Dict):
        """
        Record a successful tool discovery for learning purposes.
        
        This method passes successful discoveries to the learning system
        so it can extract new keywords and improve future discovery.
        
        Args:
            tool_info (Dict): Information about the discovered tool
        """
        self.learner.record_successful_discovery(tool_info)
    
    def learn_from_discoveries(self) -> bool:
        """
        Trigger learning from recorded discoveries and update keywords.
        
        This method processes all recorded discoveries, extracts new
        keywords, and automatically updates the keyword configuration
        if new keywords are found.
        
        Returns:
            bool: True if keywords were updated, False otherwise
        """
        suggestions = self.learner.suggest_new_keywords()
        if suggestions:
            return self.learner.auto_update_keywords(suggestions)
        return False
    
    def get_learning_stats(self) -> Dict:
        """
        Get statistics about the keyword learning system.
        
        Returns:
            Dict: Statistics including total discoveries, learned keywords, etc.
        """
        return self.learner.get_learning_stats()
    
    def add_custom_keyword(self, keyword: str, category: str = None, keyword_type: str = None):
        """
        Manually add a custom keyword to the system.
        
        This method allows manual addition of keywords to specific
        categories or keyword types. It's useful for adding domain-specific
        terms or correcting the learning system.
        
        Args:
            keyword (str): The keyword to add
            category (str, optional): Category to add the keyword to
            keyword_type (str, optional): Keyword type to add the keyword to
        """
        # Add to category if specified
        if category and category in self.learner.config.get('categories', {}):
            if keyword not in self.learner.config['categories'][category]:
                self.learner.config['categories'][category].append(keyword)
                print(f"✅ Added custom keyword: {keyword} -> {category}")
        
        # Add to keyword type if specified
        if keyword_type and keyword_type in self.learner.config.get('ai_keywords', {}):
            if keyword not in self.learner.config['ai_keywords'][keyword_type]:
                self.learner.config['ai_keywords'][keyword_type].append(keyword)
                print(f"✅ Added custom keyword: {keyword} -> {keyword_type}")
        
        # Save the updated configuration
        self.learner.save_config()
    
    def remove_keyword(self, keyword: str, category: str = None, keyword_type: str = None):
        """
        Remove a keyword from the system.
        
        This method allows manual removal of keywords from specific
        categories or keyword types. It's useful for removing outdated
        or incorrect keywords.
        
        Args:
            keyword (str): The keyword to remove
            category (str, optional): Category to remove the keyword from
            keyword_type (str, optional): Keyword type to remove the keyword from
        """
        # Remove from category if specified
        if category and category in self.learner.config.get('categories', {}):
            if keyword in self.learner.config['categories'][category]:
                self.learner.config['categories'][category].remove(keyword)
                print(f"🗑️ Removed keyword: {keyword} from {category}")
        
        # Remove from keyword type if specified
        if keyword_type and keyword_type in self.learner.config.get('ai_keywords', {}):
            if keyword in self.learner.config['ai_keywords'][keyword_type]:
                self.learner.config['ai_keywords'][keyword_type].remove(keyword)
                print(f"🗑️ Removed keyword: {keyword} from {keyword_type}")
        
        # Save the updated configuration
        self.learner.save_config()
    
    def export_keywords(self, output_path: str = None):
        """
        Export current keywords to a JSON file.
        
        This method creates a comprehensive export of all keyword data
        including AI keywords, categories, indicators, and statistics.
        Useful for backup, analysis, or sharing configurations.
        
        Args:
            output_path (str, optional): Path for the export file
        """
        if not output_path:
            output_path = "data/config/keywords_export.json"
        
        # Prepare export data
        export_data = {
            'ai_keywords': self.get_ai_keywords(),
            'categories': self.get_categories(),
            'non_tool_indicators': self.get_non_tool_indicators(),
            'tool_indicators': self.get_tool_indicators(),
            'stats': self.get_learning_stats()
        }
        
        # Ensure output directory exists and write file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📤 Exported keywords to: {output_path}")
    
    def print_keyword_summary(self):
        """
        Print a comprehensive summary of current keywords and statistics.
        
        This method provides a human-readable overview of the keyword
        system including counts, categories, and learning statistics.
        Useful for monitoring and debugging the keyword system.
        """
        ai_keywords = self.get_ai_keywords()
        categories = self.get_categories()
        stats = self.get_learning_stats()
        
        # Print overall statistics
        print("📊 Keyword Summary:")
        print(f"   Total AI Keywords: {sum(len(kw) for kw in ai_keywords.values())}")
        print(f"   Categories: {len(categories)}")
        print(f"   Auto-learned Keywords: {stats.get('auto_learned_keywords', 0)}")
        print(f"   Last Updated: {stats.get('last_updated', 'Never')}")
        
        # Print category breakdown
        print("\n📁 Categories:")
        for category, keywords in categories.items():
            print(f"   {category}: {len(keywords)} keywords")
        
        # Print AI keyword type breakdown
        print("\n🔧 AI Keyword Types:")
        for kw_type, keywords in ai_keywords.items():
            print(f"   {kw_type}: {len(keywords)} keywords")

def main():
    """
    Test and demonstration function for the keyword manager.
    
    This function provides a simple way to test the keyword manager
    functionality and see how it categorizes different types of tools.
    """
    manager = KeywordManager()
    
    # Print summary of current keywords
    manager.print_keyword_summary()
    
    # Test categorization with sample tools
    test_tools = [
        ("ChatGPT", "AI chatbot for conversations", "https://chat.openai.com"),
        ("CodeGen Studio", "AI code generation platform", "https://codegen.studio"),
        ("ImageAI Creator", "AI image generation tool", "https://imageai.com"),
        ("VoiceBot Pro", "AI voice assistant", "https://voicebot.pro"),
    ]
    
    print("\n🧪 Testing Tool Categorization:")
    for title, description, url in test_tools:
        category = manager.categorize_tool(title, description)
        is_tool = manager.is_tool_content(title, description, url)
        is_ai = manager.is_ai_related(title + " " + description)
        
        print(f"   {title}:")
        print(f"     Category: {category}")
        print(f"     Is Tool: {is_tool}")
        print(f"     Is AI: {is_ai}")

if __name__ == "__main__":
    main() 
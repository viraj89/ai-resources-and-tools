#!/usr/bin/env python3
"""
Keyword Manager
- Provides easy access to dynamic keywords from JSON config
- Integrates with the keyword learning system
- Offers utility functions for keyword operations
"""

import json
import os
from typing import List, Dict, Set
from .keyword_learner import KeywordLearner

class KeywordManager:
    def __init__(self, config_path="data/config/keywords.json"):
        self.config_path = config_path
        self.learner = KeywordLearner(config_path)
        self._cache = {}
        
    def get_ai_keywords(self) -> Dict[str, List[str]]:
        """Get all AI keywords organized by type"""
        return self.learner.config.get('ai_keywords', {})
    
    def get_all_ai_keywords_flat(self) -> List[str]:
        """Get all AI keywords as a flat list"""
        if 'all_ai_keywords' not in self._cache:
            all_keywords = []
            for keyword_list in self.get_ai_keywords().values():
                all_keywords.extend(keyword_list)
            self._cache['all_ai_keywords'] = all_keywords
        return self._cache['all_ai_keywords']
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Get all categories and their keywords"""
        return self.learner.config.get('categories', {})
    
    def get_category_keywords(self, category: str) -> List[str]:
        """Get keywords for a specific category"""
        return self.learner.get_keywords_for_category(category)
    
    def get_non_tool_indicators(self) -> List[str]:
        """Get non-tool indicators"""
        return self.learner.get_non_tool_indicators()
    
    def get_tool_indicators(self) -> List[str]:
        """Get tool indicators"""
        return self.learner.get_tool_indicators()
    
    def is_ai_related(self, text: str) -> bool:
        """Check if text is AI-related using dynamic keywords"""
        if not text:
            return False
        
        text_lower = text.lower()
        ai_keywords = self.get_all_ai_keywords_flat()
        
        # Check for AI keywords
        for keyword in ai_keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def categorize_tool(self, title: str, description: str) -> str:
        """Categorize tool based on dynamic keywords"""
        text = (title + " " + description).lower()
        categories = self.get_categories()
        
        # Score each category
        category_scores = {}
        for category, keywords in categories.items():
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
    
    def is_tool_content(self, title: str, description: str, url: str) -> bool:
        """Check if content is a tool using dynamic indicators"""
        if not url or url == "N/A" or not url.startswith('http'):
            return False
        
        # Check for non-tool indicators in URL
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
        """Record a successful discovery for learning"""
        self.learner.record_successful_discovery(tool_info)
    
    def learn_from_discoveries(self) -> bool:
        """Learn from recorded discoveries and update keywords"""
        suggestions = self.learner.suggest_new_keywords()
        if suggestions:
            return self.learner.auto_update_keywords(suggestions)
        return False
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics"""
        return self.learner.get_learning_stats()
    
    def add_custom_keyword(self, keyword: str, category: str = None, keyword_type: str = None):
        """Manually add a custom keyword"""
        if category and category in self.learner.config.get('categories', {}):
            if keyword not in self.learner.config['categories'][category]:
                self.learner.config['categories'][category].append(keyword)
                print(f"✅ Added custom keyword: {keyword} -> {category}")
        
        if keyword_type and keyword_type in self.learner.config.get('ai_keywords', {}):
            if keyword not in self.learner.config['ai_keywords'][keyword_type]:
                self.learner.config['ai_keywords'][keyword_type].append(keyword)
                print(f"✅ Added custom keyword: {keyword} -> {keyword_type}")
        
        self.learner.save_config()
    
    def remove_keyword(self, keyword: str, category: str = None, keyword_type: str = None):
        """Remove a keyword"""
        if category and category in self.learner.config.get('categories', {}):
            if keyword in self.learner.config['categories'][category]:
                self.learner.config['categories'][category].remove(keyword)
                print(f"🗑️ Removed keyword: {keyword} from {category}")
        
        if keyword_type and keyword_type in self.learner.config.get('ai_keywords', {}):
            if keyword in self.learner.config['ai_keywords'][keyword_type]:
                self.learner.config['ai_keywords'][keyword_type].remove(keyword)
                print(f"🗑️ Removed keyword: {keyword} from {keyword_type}")
        
        self.learner.save_config()
    
    def export_keywords(self, output_path: str = None):
        """Export current keywords to a file"""
        if not output_path:
            output_path = "data/config/keywords_export.json"
        
        export_data = {
            'ai_keywords': self.get_ai_keywords(),
            'categories': self.get_categories(),
            'non_tool_indicators': self.get_non_tool_indicators(),
            'tool_indicators': self.get_tool_indicators(),
            'stats': self.get_learning_stats()
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📤 Exported keywords to: {output_path}")
    
    def print_keyword_summary(self):
        """Print a summary of current keywords"""
        ai_keywords = self.get_ai_keywords()
        categories = self.get_categories()
        stats = self.get_learning_stats()
        
        print("📊 Keyword Summary:")
        print(f"   Total AI Keywords: {sum(len(kw) for kw in ai_keywords.values())}")
        print(f"   Categories: {len(categories)}")
        print(f"   Auto-learned Keywords: {stats.get('auto_learned_keywords', 0)}")
        print(f"   Last Updated: {stats.get('last_updated', 'Never')}")
        
        print("\n📁 Categories:")
        for category, keywords in categories.items():
            print(f"   {category}: {len(keywords)} keywords")
        
        print("\n🔧 AI Keyword Types:")
        for kw_type, keywords in ai_keywords.items():
            print(f"   {kw_type}: {len(keywords)} keywords")

def main():
    """Test the keyword manager"""
    manager = KeywordManager()
    
    # Print summary
    manager.print_keyword_summary()
    
    # Test categorization
    test_tools = [
        ("ChatGPT", "AI chatbot for conversations", "https://chat.openai.com"),
        ("CodeGen Studio", "AI code generation platform", "https://codegen.studio"),
        ("ImageFlow", "AI image generation tool", "https://imageflow.ai")
    ]
    
    print("\n🧪 Testing categorization:")
    for title, desc, url in test_tools:
        category = manager.categorize_tool(title, desc)
        is_tool = manager.is_tool_content(title, desc, url)
        print(f"   {title}: {category} (Tool: {is_tool})")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Keyword Management CLI
- Command-line interface for managing dynamic keywords
- Add, remove, and view keywords
- Export and import keyword configurations
- View learning statistics
"""

import sys
import os
import argparse
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.keyword_manager import KeywordManager

def main():
    parser = argparse.ArgumentParser(description='Manage dynamic keywords for AI tools discovery')
    parser.add_argument('command', choices=['list', 'add', 'remove', 'stats', 'export', 'import', 'test'], 
                       help='Command to execute')
    parser.add_argument('--keyword', '-k', help='Keyword to add or remove')
    parser.add_argument('--category', '-c', help='Category for the keyword')
    parser.add_argument('--type', '-t', help='Keyword type (companies, models, technologies, applications, tool_indicators)')
    parser.add_argument('--file', '-f', help='File path for export/import')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    manager = KeywordManager()
    
    if args.command == 'list':
        list_keywords(manager, args.verbose)
    elif args.command == 'add':
        add_keyword(manager, args.keyword, args.category, args.type)
    elif args.command == 'remove':
        remove_keyword(manager, args.keyword, args.category, args.type)
    elif args.command == 'stats':
        show_stats(manager)
    elif args.command == 'export':
        export_keywords(manager, args.file)
    elif args.command == 'import':
        import_keywords(manager, args.file)
    elif args.command == 'test':
        test_keywords(manager)

def list_keywords(manager, verbose=False):
    """List all keywords"""
    print("📋 Keyword Listing")
    print("=" * 50)
    
    # List AI keywords by type
    ai_keywords = manager.get_ai_keywords()
    print("\n🤖 AI Keywords by Type:")
    for kw_type, keywords in ai_keywords.items():
        print(f"\n  {kw_type.upper()}:")
        if verbose:
            for keyword in keywords:
                print(f"    - {keyword}")
        else:
            print(f"    {len(keywords)} keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
    
    # List categories
    categories = manager.get_categories()
    print(f"\n📁 Categories ({len(categories)}):")
    for category, keywords in categories.items():
        print(f"\n  {category}:")
        if verbose:
            for keyword in keywords:
                print(f"    - {keyword}")
        else:
            print(f"    {len(keywords)} keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
    
    # List indicators
    print(f"\n🚫 Non-tool indicators ({len(manager.get_non_tool_indicators())}):")
    non_tool = manager.get_non_tool_indicators()
    if verbose:
        for indicator in non_tool:
            print(f"  - {indicator}")
    else:
        print(f"  {', '.join(non_tool[:10])}{'...' if len(non_tool) > 10 else ''}")
    
    print(f"\n🛠️ Tool indicators ({len(manager.get_tool_indicators())}):")
    tool_indicators = manager.get_tool_indicators()
    if verbose:
        for indicator in tool_indicators:
            print(f"  - {indicator}")
    else:
        print(f"  {', '.join(tool_indicators[:10])}{'...' if len(tool_indicators) > 10 else ''}")

def add_keyword(manager, keyword, category, keyword_type):
    """Add a keyword"""
    if not keyword:
        print("❌ Error: Please provide a keyword with --keyword")
        return
    
    if not category and not keyword_type:
        print("❌ Error: Please provide either --category or --type")
        return
    
    print(f"➕ Adding keyword: {keyword}")
    
    if category:
        print(f"   Category: {category}")
        manager.add_custom_keyword(keyword, category=category)
    
    if keyword_type:
        print(f"   Type: {keyword_type}")
        manager.add_custom_keyword(keyword, keyword_type=keyword_type)
    
    print("✅ Keyword added successfully!")

def remove_keyword(manager, keyword, category, keyword_type):
    """Remove a keyword"""
    if not keyword:
        print("❌ Error: Please provide a keyword with --keyword")
        return
    
    if not category and not keyword_type:
        print("❌ Error: Please provide either --category or --type")
        return
    
    print(f"🗑️ Removing keyword: {keyword}")
    
    if category:
        print(f"   Category: {category}")
        manager.remove_keyword(keyword, category=category)
    
    if keyword_type:
        print(f"   Type: {keyword_type}")
        manager.remove_keyword(keyword, keyword_type=keyword_type)
    
    print("✅ Keyword removed successfully!")

def show_stats(manager):
    """Show learning statistics"""
    print("📊 Learning Statistics")
    print("=" * 50)
    
    stats = manager.get_learning_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n📋 Keyword Summary:")
    manager.print_keyword_summary()

def export_keywords(manager, file_path=None):
    """Export keywords to file"""
    if not file_path:
        file_path = "data/config/keywords_export.json"
    
    print(f"📤 Exporting keywords to: {file_path}")
    manager.export_keywords(file_path)
    print("✅ Export completed!")

def import_keywords(manager, file_path):
    """Import keywords from file"""
    if not file_path:
        print("❌ Error: Please provide a file path with --file")
        return
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return
    
    print(f"📥 Importing keywords from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Import AI keywords
        if 'ai_keywords' in data:
            for kw_type, keywords in data['ai_keywords'].items():
                for keyword in keywords:
                    manager.add_custom_keyword(keyword, keyword_type=kw_type)
        
        # Import category keywords
        if 'categories' in data:
            for category, keywords in data['categories'].items():
                for keyword in keywords:
                    manager.add_custom_keyword(keyword, category=category)
        
        print("✅ Import completed!")
        
    except Exception as e:
        print(f"❌ Error importing keywords: {e}")

def test_keywords(manager):
    """Test keyword functionality"""
    print("🧪 Testing Keyword System")
    print("=" * 50)
    
    # Test AI relevance
    test_texts = [
        "ChatGPT is amazing",
        "Weather forecast for today",
        "Machine learning platform",
        "Simple calculator",
        "Neural network training"
    ]
    
    print("\n🤖 AI Relevance Test:")
    for text in test_texts:
        is_ai = manager.is_ai_related(text)
        print(f"  '{text}': {'✅ AI' if is_ai else '❌ Not AI'}")
    
    # Test categorization
    test_tools = [
        ("CodeGen AI", "AI-powered code generation platform"),
        ("ImageFlow", "AI image generation tool"),
        ("VoiceBot", "AI voice assistant"),
        ("DataViz Pro", "Data visualization tool")
    ]
    
    print("\n🏷️ Categorization Test:")
    for name, desc in test_tools:
        category = manager.categorize_tool(name, desc)
        print(f"  {name}: {category}")
    
    # Test tool detection
    test_content = [
        ("ChatGPT", "AI chatbot", "https://chat.openai.com"),
        ("Reddit Post", "Discussion about AI", "https://reddit.com/r/ai"),
        ("GitHub Repo", "AI tool repository", "https://github.com/ai/tool")
    ]
    
    print("\n🛠️ Tool Detection Test:")
    for name, desc, url in test_content:
        is_tool = manager.is_tool_content(name, desc, url)
        print(f"  {name}: {'✅ Tool' if is_tool else '❌ Not Tool'}")

if __name__ == "__main__":
    main() 
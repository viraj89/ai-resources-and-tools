#!/usr/bin/env python3
"""
Test Keyword Learning System
- Demonstrates the dynamic keyword learning functionality
- Shows how the system learns from successful discoveries
- Tests keyword extraction and categorization
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.keyword_manager import KeywordManager
from src.utils.keyword_learner import KeywordLearner

def test_keyword_learning():
    """Test the keyword learning system"""
    print("🧪 Testing Keyword Learning System")
    print("=" * 50)
    
    # Initialize keyword manager
    manager = KeywordManager()
    
    # Print initial keyword summary
    print("\n📊 Initial Keyword Summary:")
    manager.print_keyword_summary()
    
    # Test with sample discoveries
    sample_discoveries = [
        {
            'Tool Name': 'RAG Studio Pro',
            'Category': 'Search / Research',
            'What it does': 'Advanced RAG platform with vector database integration and semantic search capabilities',
            'URL': 'https://ragstudio.pro',
            'Trending Score': 92,
            'Source': 'github'
        },
        {
            'Tool Name': 'VectorFlow Analytics',
            'Category': 'Business / Analytics',
            'What it does': 'Vector database management and analytics platform with real-time insights',
            'URL': 'https://vectorflow.analytics',
            'Trending Score': 88,
            'Source': 'reddit'
        },
        {
            'Tool Name': 'NeuralCode Generator',
            'Category': 'Code / Developer Tools',
            'What it does': 'AI-powered code generation using neural networks and transformer models',
            'URL': 'https://neuralcode.dev',
            'Trending Score': 85,
            'Source': 'github'
        },
        {
            'Tool Name': 'Multimodal Vision AI',
            'Category': 'Design / Image Generation',
            'What it does': 'Advanced computer vision platform with multimodal AI capabilities',
            'URL': 'https://multimodal.vision',
            'Trending Score': 90,
            'Source': 'news'
        }
    ]
    
    print(f"\n📚 Recording {len(sample_discoveries)} sample discoveries...")
    
    # Record discoveries
    for discovery in sample_discoveries:
        manager.record_successful_discovery(discovery)
        print(f"   ✅ Recorded: {discovery['Tool Name']}")
    
    # Test categorization
    print("\n🏷️ Testing categorization:")
    for discovery in sample_discoveries:
        category = manager.categorize_tool(discovery['Tool Name'], discovery['What it does'])
        is_tool = manager.is_tool_content(discovery['Tool Name'], discovery['What it does'], discovery['URL'])
        print(f"   {discovery['Tool Name']}: {category} (Tool: {is_tool})")
    
    # Test AI relevance detection
    print("\n🤖 Testing AI relevance detection:")
    test_texts = [
        "ChatGPT is an AI chatbot",
        "This is a regular news article about weather",
        "VectorFlow uses machine learning for analytics",
        "Simple calculator app",
        "Neural network training platform"
    ]
    
    for text in test_texts:
        is_ai = manager.is_ai_related(text)
        print(f"   '{text}': {'AI-related' if is_ai else 'Not AI-related'}")
    
    # Learn from discoveries
    print("\n🧠 Learning from discoveries...")
    if manager.learn_from_discoveries():
        print("✅ Keywords updated successfully!")
    else:
        print("📝 No new keywords to learn from")
    
    # Print updated statistics
    print("\n📊 Updated Keyword Summary:")
    manager.print_keyword_summary()
    
    # Test keyword extraction
    print("\n🔍 Testing keyword extraction:")
    learner = KeywordLearner()
    suggestions = learner.suggest_new_keywords()
    
    if suggestions:
        print(f"💡 Suggested {len(suggestions.get('general_keywords', []))} new general keywords:")
        for keyword in suggestions.get('general_keywords', [])[:5]:  # Show first 5
            confidence = suggestions.get('confidence_scores', {}).get(keyword, 0)
            print(f"   {keyword} (confidence: {confidence})")
        
        print(f"\n📁 Suggested category keywords:")
        for category, keywords in suggestions.get('category_keywords', {}).items():
            if keywords:
                print(f"   {category}: {', '.join(keywords[:3])}")  # Show first 3
    else:
        print("📝 No new keywords suggested")
    
    # Test manual keyword addition
    print("\n➕ Testing manual keyword addition:")
    manager.add_custom_keyword("quantum_ai", keyword_type="technologies")
    manager.add_custom_keyword("automation", category="Business / Analytics")
    
    # Export keywords
    print("\n📤 Exporting keywords...")
    manager.export_keywords("data/config/keywords_test_export.json")
    
    print("\n✅ Keyword learning system test completed!")

def test_keyword_operations():
    """Test various keyword operations"""
    print("\n🔧 Testing Keyword Operations")
    print("=" * 50)
    
    manager = KeywordManager()
    
    # Test getting keywords for specific category
    print("\n📁 Keywords for 'Code / Developer Tools':")
    code_keywords = manager.get_category_keywords("Code / Developer Tools")
    print(f"   {', '.join(code_keywords[:10])}...")  # Show first 10
    
    # Test getting all AI keywords
    print("\n🤖 All AI keywords (first 10):")
    ai_keywords = manager.get_all_ai_keywords_flat()
    print(f"   {', '.join(ai_keywords[:10])}...")
    
    # Test non-tool indicators
    print("\n🚫 Non-tool indicators (first 10):")
    non_tool = manager.get_non_tool_indicators()
    print(f"   {', '.join(non_tool[:10])}...")
    
    # Test tool indicators
    print("\n🛠️ Tool indicators (first 10):")
    tool_indicators = manager.get_tool_indicators()
    print(f"   {', '.join(tool_indicators[:10])}...")

def main():
    """Main test function"""
    print("🚀 Starting Keyword Learning System Tests")
    print("=" * 60)
    
    try:
        # Test basic functionality
        test_keyword_learning()
        
        # Test operations
        test_keyword_operations()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
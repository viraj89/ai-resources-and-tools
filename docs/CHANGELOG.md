# Changelog

All notable changes to the Auto News AI Tools Discovery project will be documented in this file.

## [2.2.0] - 2025-06-20

### 🧠 Added - Phase 2: Dynamic Keyword Learning System

#### Core Features
- **JSON-based Keyword Configuration**: Replaced hardcoded keywords with `data/config/keywords.json`
- **Keyword Learning System**: Automatic learning from successful discoveries
- **Smart Keyword Extraction**: Extracts new keywords from tool names, descriptions, and URLs
- **Category Learning**: Learns category-specific keywords automatically
- **Confidence Scoring**: Uses frequency analysis for keyword confidence
- **Learning Statistics**: Tracks discovery success and keyword evolution

#### New Components
- `src/utils/keyword_learner.py`: Core learning system
- `src/utils/keyword_manager.py`: Keyword management utilities
- `src/scripts/manage_keywords.py`: CLI for keyword management
- `src/scripts/test_keyword_learning.py`: Comprehensive testing suite
- `data/config/keywords.json`: Dynamic keyword configuration

#### CLI Commands
- `keyword-manager list`: List all keywords
- `keyword-manager add`: Add keywords to categories or types
- `keyword-manager remove`: Remove keywords
- `keyword-manager stats`: Show learning statistics
- `keyword-manager export/import`: Export/import keyword configurations
- `keyword-manager test`: Test keyword functionality
- `test-keywords`: Run comprehensive tests

#### Enhanced Discovery
- Updated `daily_tools_digest.py` to use dynamic keywords
- Integrated keyword learning into daily discovery process
- Automatic recording of successful discoveries
- Real-time keyword updates based on discoveries

#### Configuration Structure
```json
{
  "ai_keywords": {
    "companies": ["openai", "anthropic", ...],
    "models": ["gpt", "claude", ...],
    "technologies": ["ai", "machine learning", ...],
    "applications": ["ai tool", "ai platform", ...],
    "tool_indicators": ["ai", "gpt", "assistant", ...]
  },
  "non_tool_indicators": ["reddit", "twitter", ...],
  "categories": {
    "Text / Chat Assistants": ["chat", "assistant", ...],
    "Code / Developer Tools": ["code", "programming", ...],
    ...
  },
  "learning_config": {
    "enabled": true,
    "min_confidence_score": 0.7,
    "max_keywords_per_category": 50,
    "auto_update_frequency": "daily"
  },
  "metadata": {
    "last_updated": "2025-06-20",
    "version": "1.0.0",
    "total_keywords": 0,
    "successful_discoveries": 0,
    "auto_learned_keywords": 0
  }
}
```

#### Learning Features
- **Title Analysis**: Extracts keywords from tool names
- **Description Analysis**: Extracts technical terms and AI patterns
- **URL Analysis**: Extracts keywords from URL paths
- **Category Patterns**: Learns category-specific patterns
- **Frequency Analysis**: Uses keyword frequency for confidence scoring
- **Auto-update**: Automatically updates keywords based on discoveries

#### Benefits
- **Scalability**: No more hardcoded keywords, system adapts automatically
- **Maintainability**: Easy to manage keywords via CLI or JSON
- **Accuracy**: Improves over time through learning
- **Flexibility**: Supports custom keywords and categories
- **Transparency**: Full visibility into keyword learning process

### 🔧 Technical Improvements
- Updated `setup.py` with new entry points
- Enhanced project structure with utils package
- Improved error handling and logging
- Better documentation and examples

### 📚 Documentation
- Updated README with Phase 2 features
- Added comprehensive CLI documentation
- Included configuration examples
- Added testing instructions

---

## [2.1.0] - 2025-06-19

### 🎯 Added - Enhanced Tools Directory

#### New Features
- **Clean Tools Directory**: Generated `ai-tools-directory.md` with categorized markdown table
- **Smart Filtering**: Filters out Reddit posts, news articles, and non-tool content
- **Category Organization**: Tools organized by type (Text/Chat, Code, Design, etc.)
- **Pricing Information**: Includes free/paid status for each tool
- **Readable Format**: Clean, professional markdown table format

#### New Script
- `src/scripts/generate_tools_directory.py`: Generates categorized tools directory
- Integrated into daily GitHub Actions workflow
- Automatically filters and categorizes tools from CSV

#### Improvements
- Better content filtering to exclude non-tool content
- Enhanced categorization logic
- Improved CSV cleaning and deduplication
- More professional output formatting

### 🔧 Technical Changes
- Updated GitHub Actions to generate tools directory daily
- Enhanced CSV processing with better filtering
- Improved markdown table generation
- Better error handling and logging

---

## [2.0.0] - 2025-06-18

### 🚀 Major Restructure

#### Project Reorganization
- **New Structure**: Moved from `tools/` to `src/` organization
- **Scripts**: All Python scripts now in `src/scripts/`
- **Data**: Organized data files in `data/` directory
- **Documentation**: Moved to `docs/` directory
- **Package Setup**: Added `setup.py` for proper package installation

#### Enhanced Discovery System
- **Multiple Sources**: GitHub trending, Reddit, news articles
- **Trending Score Algorithm**: Advanced scoring based on engagement
- **Smart Deduplication**: Prevents duplicates across all sources
- **Category Detection**: Automatic tool categorization
- **Enrichment**: Web scraping for better descriptions

#### New Features
- **Daily Digest**: Generates `ai-tools-daily.md` with 3-5 trending tools
- **Master CSV**: Maintains `data/master_resources.csv` with all tools
- **Cache System**: Prevents re-processing same items
- **GitHub Actions**: Automated daily workflows

#### Scripts
- `daily_tools_digest.py`: Main discovery and digest generator
- `news_aggregator.py`: News aggregation from RSS feeds
- Enhanced error handling and logging

---

## [1.0.0] - 2025-06-17

### 🎉 Initial Release

#### Core Features
- **News Aggregation**: RSS feed processing for AI news
- **Basic Tools Discovery**: Simple AI tools discovery
- **Markdown Output**: Basic markdown generation
- **GitHub Actions**: Initial automation setup

#### Components
- Basic news aggregation script
- Simple tools discovery
- Manual keyword management
- Basic output formatting

---

## Version History Summary

| Version | Date | Major Features |
|---------|------|----------------|
| 2.2.0 | 2025-06-20 | 🧠 Dynamic Keyword Learning System |
| 2.1.0 | 2025-06-19 | 🎯 Enhanced Tools Directory |
| 2.0.0 | 2025-06-18 | 🚀 Major Restructure & Enhanced Discovery |
| 1.0.0 | 2025-06-17 | 🎉 Initial Release |

---

## Future Roadmap

### Phase 3: AI-Powered Classification (Planned)
- **Machine Learning Models**: Train models on successful discoveries
- **Semantic Analysis**: Use embeddings for better categorization
- **Confidence Scoring**: ML-based confidence for discoveries
- **Adaptive Learning**: Continuous model improvement

### Phase 4: Advanced Analytics (Planned)
- **Trend Analysis**: Identify emerging AI trends
- **Market Intelligence**: Track tool popularity and adoption
- **Predictive Discovery**: Predict trending tools before they become popular
- **Competitive Analysis**: Compare tools across categories

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format. 
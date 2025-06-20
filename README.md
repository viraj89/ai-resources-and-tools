# Auto News AI Tools Discovery

An intelligent, automated system that discovers, aggregates, and maintains a comprehensive collection of trending AI tools, apps, and news using **dynamic keyword learning**.

## 🚀 Features

### Core Functionality
- **Daily AI Tools Discovery**: Automatically finds 3-5 trending AI tools daily
- **News Aggregation**: Collects and summarizes AI-related news and blog posts
- **Smart Deduplication**: Prevents duplicate entries across all sources
- **Trending Score Algorithm**: Ranks tools based on engagement and relevance
- **Clean Output**: Generates readable markdown and CSV formats

### 🧠 Phase 2: Dynamic Keyword Learning System
- **JSON-based Configuration**: All keywords stored in `data/config/keywords.json`
- **Auto-learning**: System learns from successful discoveries and updates keywords
- **Smart Categorization**: Automatically categorizes tools based on learned patterns
- **Keyword Extraction**: Extracts new keywords from tool names, descriptions, and URLs
- **Learning Statistics**: Tracks discovery success and keyword evolution
- **CLI Management**: Command-line interface for keyword management

## 📁 Project Structure

```
auto-news/
├── src/
│   ├── scripts/
│   │   ├── daily_tools_digest.py      # Daily AI tools discovery
│   │   ├── news_aggregator.py         # News aggregation
│   │   ├── generate_tools_directory.py # Generate tools directory
│   │   ├── manage_keywords.py         # Keyword management CLI
│   │   └── test_keyword_learning.py   # Test keyword system
│   └── utils/
│       ├── keyword_manager.py         # Keyword management utilities
│       └── keyword_learner.py         # Keyword learning system
├── data/
│   ├── config/
│   │   └── keywords.json              # Dynamic keyword configuration
│   ├── cache/
│   │   └── tools_cache.json           # Discovery cache
│   └── master_resources.csv           # Master tools database
├── docs/
│   └── CHANGELOG.md                   # Version history
├── ai-tools-daily.md                  # Daily digest output
├── blogs-and-news.md                  # News aggregation output
├── ai-tools-directory.md              # Tools directory
└── setup.py                          # Package installation
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd auto-news
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Verify installation**:
   ```bash
   keyword-manager stats
   ```

## 🚀 Quick Start

### Daily AI Tools Discovery
```bash
# Run daily discovery (finds 3-5 trending tools)
daily-tools

# Or use the Python script directly
python src/scripts/daily_tools_digest.py
```

### News Aggregation
```bash
# Aggregate news and blog posts
news-aggregator

# Or use the Python script directly
python src/scripts/news_aggregator.py
```

### Generate Tools Directory
```bash
# Generate categorized tools directory
tools-directory

# Or use the Python script directly
python src/scripts/generate_tools_directory.py
```

## 🧠 Keyword Learning System

### Overview
The system now uses a **dynamic keyword learning approach** that automatically improves over time:

1. **JSON Configuration**: All keywords stored in `data/config/keywords.json`
2. **Auto-learning**: System learns from successful discoveries
3. **Smart Extraction**: Extracts new keywords from tool names, descriptions, URLs
4. **Category Learning**: Learns category-specific keywords
5. **Confidence Scoring**: Uses frequency analysis for keyword confidence

### Managing Keywords

#### View Keywords
```bash
# List all keywords
keyword-manager list

# Verbose listing
keyword-manager list --verbose
```

#### Add Keywords
```bash
# Add to category
keyword-manager add --keyword "quantum_ai" --category "Business / Analytics"

# Add to keyword type
keyword-manager add --keyword "automation" --type "technologies"
```

#### Remove Keywords
```bash
# Remove from category
keyword-manager remove --keyword "old_keyword" --category "Code / Developer Tools"

# Remove from keyword type
keyword-manager remove --keyword "deprecated" --type "models"
```

#### View Statistics
```bash
# Show learning statistics
keyword-manager stats
```

#### Export/Import
```bash
# Export keywords
keyword-manager export --file my_keywords.json

# Import keywords
keyword-manager import --file my_keywords.json
```

#### Test System
```bash
# Test keyword functionality
keyword-manager test

# Run comprehensive tests
test-keywords
```

### Keyword Configuration Structure

The `data/config/keywords.json` file contains:

```json
{
  "ai_keywords": {
    "companies": ["openai", "anthropic", "google ai", ...],
    "models": ["gpt", "claude", "llama", ...],
    "technologies": ["ai", "machine learning", "deep learning", ...],
    "applications": ["ai tool", "ai platform", "text generation", ...],
    "tool_indicators": ["ai", "gpt", "assistant", "tool", ...]
  },
  "non_tool_indicators": ["reddit", "twitter", "article", ...],
  "categories": {
    "Text / Chat Assistants": ["chat", "assistant", "writing", ...],
    "Code / Developer Tools": ["code", "programming", "developer", ...],
    "Design / Image Generation": ["image", "photo", "art", ...],
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

## 🔄 GitHub Actions

The system includes automated workflows:

- **Daily Discovery**: Runs every day at 6 AM UTC
- **News Aggregation**: Runs every 6 hours
- **Tools Directory**: Generated daily with the discovery
- **Keyword Learning**: Integrated into daily discovery process

## 📊 Output Files

### Generated Files
- `ai-tools-daily.md`: Daily digest of 3-5 trending AI tools
- `blogs-and-news.md`: Aggregated news and blog posts
- `ai-tools-directory.md`: Categorized directory of all discovered tools
- `data/master_resources.csv`: Master database of all tools

### Configuration Files
- `data/config/keywords.json`: Dynamic keyword configuration
- `data/cache/tools_cache.json`: Discovery cache to prevent duplicates

## 🧪 Testing

### Test Keyword Learning System
```bash
# Run comprehensive tests
python src/scripts/test_keyword_learning.py

# Or use the installed command
test-keywords
```

### Test Individual Components
```bash
# Test keyword management
keyword-manager test

# Test daily discovery
python src/scripts/daily_tools_digest.py
```

## 📈 Learning Statistics

The system tracks learning progress:

- **Total Discoveries**: Number of successful tool discoveries
- **Auto-learned Keywords**: Keywords automatically added by the system
- **Last Updated**: When keywords were last updated
- **Config Version**: Current configuration version

## 🔧 Configuration

### Learning Configuration
```json
{
  "learning_config": {
    "enabled": true,
    "min_confidence_score": 0.7,
    "max_keywords_per_category": 50,
    "auto_update_frequency": "daily",
    "successful_discovery_threshold": 3,
    "keyword_extraction_methods": [
      "title_analysis",
      "description_analysis", 
      "url_analysis",
      "category_patterns"
    ]
  }
}
```

### Customization
- Adjust confidence thresholds
- Modify keyword extraction methods
- Set maximum keywords per category
- Configure update frequency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `test-keywords`
5. Submit a pull request

## 📝 Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for version history.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [CHANGELOG.md](docs/CHANGELOG.md)
2. Run `keyword-manager test` to verify system health
3. Check the generated output files for issues
4. Open an issue on GitHub

---

**Version**: 2.2.0  
**Last Updated**: June 2025  
**Status**: Active Development with Dynamic Learning

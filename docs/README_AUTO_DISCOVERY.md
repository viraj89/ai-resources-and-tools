# 🤖 AI Tools Auto-Discovery System

This innovative system automatically discovers and adds new AI tools to your `master_resources.csv` file, eliminating the need for manual entry. It works similarly to your news aggregation system but focuses on finding AI tools from multiple sources.

## 🚀 Features

### **Multi-Source Discovery**
- **GitHub Trending**: Scrapes trending repositories for AI tools
- **Reddit Communities**: Monitors r/MachineLearning and r/artificial for new tools
- **News Articles**: Extracts tool mentions from your existing news feed
- **Future Sources**: Product Hunt, Hugging Face, AI tool directories

### **Smart Filtering & Categorization**
- **AI Relevance Detection**: Uses comprehensive keyword matching to identify AI tools
- **Automatic Categorization**: Intelligently categorizes tools into appropriate categories
- **Duplicate Prevention**: Avoids adding tools that already exist in your CSV
- **Pricing Detection**: Automatically detects free/paid/freemium models

### **Data Enrichment**
- **Website Scraping**: Extracts better descriptions from tool websites
- **Meta Tag Analysis**: Uses meta descriptions and Open Graph data
- **Enhanced Descriptions**: Improves and formats tool descriptions

### **Quality Control**
- **Confidence Scoring**: Rates the quality of discovered tools
- **Cache Management**: Prevents re-processing the same items
- **Error Handling**: Graceful handling of network issues and parsing errors

## 📁 Files Overview

```
tools/script/
├── auto_discover_ai_tools.py          # Basic discovery script
├── enhanced_ai_discovery.py           # Enhanced version with better categorization
└── README_AUTO_DISCOVERY.md          # This file

tools/resources/
├── master_resources.csv               # Your main tools database
├── tools_cache.json                   # Cache to avoid duplicates
└── enhanced_tools_cache.json          # Enhanced version cache

.github/workflows/
└── auto-discover-tools.yml           # GitHub Actions automation
```

## 🛠️ Usage

### **Manual Execution**

1. **Basic Discovery**:
   ```bash
   python tools/script/auto_discover_ai_tools.py
   ```

2. **Enhanced Discovery** (recommended):
   ```bash
   python tools/script/enhanced_ai_discovery.py
   ```

### **Automated Execution**

The system runs automatically every 3 days via GitHub Actions. You can also trigger it manually from the GitHub Actions tab.

## 🔧 Configuration

### **Sources Configuration**

Edit the `SOURCES` dictionary in the script to add/remove discovery sources:

```python
SOURCES = {
    "github_trending": "https://github.com/trending?since=daily&spoken_language_code=en",
    "reddit_ml": "https://www.reddit.com/r/MachineLearning/new.json",
    "reddit_ai": "https://www.reddit.com/r/artificial/new.json",
    # Add more sources here
}
```

### **AI Keywords**

Customize the `AI_KEYWORDS` list to improve AI tool detection:

```python
AI_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "ML",
    "ChatGPT", "Claude", "GPT-4", "DALL-E", "Stable Diffusion",
    # Add more keywords
]
```

### **Categories**

Modify the `CATEGORIES` dictionary to adjust categorization rules:

```python
CATEGORIES = {
    "Text / Chat Assistants": ["chat", "assistant", "writing", "text"],
    "Code / Developer Tools": ["code", "programming", "developer"],
    # Add more categories
}
```

## 📊 How It Works

### **1. Discovery Phase**
- Scrapes multiple sources for potential AI tools
- Filters content based on AI-related keywords
- Extracts tool names, descriptions, and URLs

### **2. Processing Phase**
- Removes duplicates and existing tools
- Categorizes tools using keyword matching
- Determines pricing models
- Enhances descriptions

### **3. Enrichment Phase**
- Scrapes tool websites for better descriptions
- Extracts meta tags and Open Graph data
- Validates URLs and pricing information

### **4. Addition Phase**
- Adds new tools to the CSV file
- Updates cache to prevent re-processing
- Provides detailed logging

## 🎯 Example Output

```
🔍 Starting Enhanced AI Tools Discovery...
📊 Discovered 15 potential new AI tools
✅ Added: AutoGPT (Code / Developer Tools)
✅ Added: Midjourney V6 (Design / Image Generation)
✅ Added: Claude Sonnet (Text / Chat Assistants)
✅ Successfully added 3 new tools to master_resources.csv
🎉 Enhanced discovery complete! Added 3 new AI tools.
```

## 🔄 Automation Schedule

- **Frequency**: Every 3 days at 8 AM IST
- **Trigger**: GitHub Actions workflow
- **Manual Trigger**: Available via GitHub Actions UI
- **Commit**: Automatically commits changes to the repository

## 🛡️ Safety Features

### **Rate Limiting**
- Respects server rate limits with delays between requests
- Uses proper User-Agent headers
- Implements timeout handling

### **Error Handling**
- Graceful handling of network failures
- Continues processing even if some sources fail
- Detailed error logging

### **Data Validation**
- Validates URLs before processing
- Checks for duplicate entries
- Ensures data quality before adding to CSV

## 🚀 Advanced Features

### **AI-Powered Categorization** (Optional)

For even better categorization, you can enable AI API integration:

1. Set up API keys:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export ANTHROPIC_API_KEY="your-key-here"
   ```

2. Enable AI categorization in the script:
   ```python
   AI_API_CONFIG = {
       "use_ai_categorization": True
   }
   ```

### **Custom Sources**

Add your own discovery sources by implementing new methods:

```python
def discover_from_custom_source(self):
    """Discover AI tools from your custom source"""
    # Your implementation here
    pass
```

## 📈 Monitoring & Analytics

The system provides detailed logging and analytics:

- **Discovery Statistics**: Number of tools found per source
- **Success Rates**: Percentage of tools successfully added
- **Category Distribution**: Breakdown of tool categories
- **Cache Performance**: Duplicate prevention metrics

## 🔧 Troubleshooting

### **Common Issues**

1. **No tools discovered**:
   - Check internet connectivity
   - Verify source URLs are accessible
   - Review AI keywords configuration

2. **Duplicate entries**:
   - Clear cache files: `tools/resources/tools_cache.json`
   - Check existing CSV for duplicates

3. **Rate limiting**:
   - Increase delays between requests
   - Use different User-Agent headers
   - Implement proxy rotation

### **Debug Mode**

Enable debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

To improve the discovery system:

1. **Add New Sources**: Implement new discovery methods
2. **Improve Categorization**: Enhance keyword matching rules
3. **Better Filtering**: Add more sophisticated AI detection
4. **Performance**: Optimize scraping and processing speed

## 📝 Future Enhancements

- **Machine Learning**: Train models for better tool classification
- **Community Feedback**: Allow users to suggest corrections
- **API Integration**: Connect with more AI tool directories
- **Real-time Monitoring**: WebSocket-based real-time discovery
- **Quality Scoring**: Implement confidence scores for discovered tools

## 🎉 Benefits

1. **Time Saving**: No more manual tool entry
2. **Comprehensive Coverage**: Discovers tools from multiple sources
3. **Consistent Quality**: Standardized categorization and descriptions
4. **Always Updated**: Automated discovery keeps your database current
5. **Scalable**: Easy to add new sources and improve algorithms

---

**This system transforms your manual CSV maintenance into an intelligent, automated AI tools discovery engine! 🚀** 
# Release Notes

## v2.0.0 - Enhanced AI Tools Discovery & Daily Digest (2025-06-20)

### 🚀 Major New Features

#### Daily AI Tools Digest
- **Automated Daily Digest**: Generates `ai-tools-daily.md` with 3-5 top trending AI tools/apps daily
- **Master CSV Integration**: Each digest includes a link to the complete master resources list
- **Clean Markdown Format**: Perfect for newsletters, social media, or daily updates

#### Advanced Trending Detection
- **Sophisticated Scoring Algorithm**: Identifies the most trending tools using:
  - AI relevance keywords (ChatGPT, Claude, DALL-E, etc.)
  - Trending keywords (launch, release, new, viral, etc.)
  - Reddit engagement metrics (upvotes, comments)
  - GitHub trending bonus
  - Source diversity scoring

#### Enhanced Discovery Sources
- **Multi-Subreddit Reddit Integration**: 
  - r/artificial, r/MachineLearning, r/AINews, r/OpenAI, r/StableDiffusion
  - r/LocalLLaMA, r/ChatGPT, r/AI, r/artificialintelligence, r/deeplearning
- **Multiple Reddit Endpoints**: hot, new, and top posts for comprehensive coverage
- **GitHub Trending**: Enhanced repository discovery with better filtering
- **News Article Extraction**: Improved pattern matching for tool mentions

### 🔧 Technical Improvements

#### Automation & Scheduling
- **Daily Schedule**: Both workflows now run daily
  - News aggregation: 7:00 AM IST
  - Tools discovery: 7:15 AM IST
- **Deduplication System**: Prevents duplicates across all outputs
- **Enhanced Error Handling**: Better logging and graceful failure handling

#### Data Quality
- **Website Scraping**: Extracts better descriptions from tool websites
- **Pricing Detection**: Automatic detection of free/paid/freemium models
- **Enhanced Categorization**: Improved tool categorization with better keywords

### 📁 New Files Added
- `tools/script/daily_tools_digest.py` - Main daily digest generator
- `tools/script/auto_discover_ai_tools.py` - Enhanced tools discovery
- `tools/script/enhanced_ai_discovery.py` - Advanced discovery with AI categorization
- `tools/script/README_AUTO_DISCOVERY.md` - Comprehensive documentation
- `.github/workflows/auto-discover-tools.yml` - Daily tools discovery workflow
- `ai-tools-daily.md` - Daily digest output file
- `VERSION` - Version tracking file
- `CHANGELOG.md` - Detailed changelog

### 🔄 Migration from v1.0.0
- **No Breaking Changes**: All existing functionality preserved
- **Additive Features**: New capabilities build on existing system
- **Updated Dependencies**: Add `beautifulsoup4` to requirements
- **Enhanced Documentation**: Comprehensive README updates

---

## v1.0.0 - Initial AI News Aggregation System (2025-06-19)

### 🎯 Core Features

#### Automated News Aggregation
- **Google News RSS Integration**: Fetches AI-related news from multiple RSS feeds
- **Smart Filtering**: Comprehensive AI keyword matching for relevant content
- **Daily Updates**: Automatic daily news aggregation at 7:00 AM IST
- **Clean Output**: Well-formatted markdown with daily sections

#### News Processing Pipeline
- **Deduplication**: Prevents duplicate news items
- **Priority Sorting**: Severity-based scoring for important news
- **URL Shortening**: Clean citations using TinyURL API
- **Cache Management**: Prevents re-processing of recent news

#### Manual Tools Database
- **CSV-based System**: Curated collection of AI tools and resources
- **Categorization**: Organized by tool type and functionality
- **Pricing Information**: Free/paid/freemium tracking

### 📁 Files Created
- `tools/script/update_blogs_and_news.py` - Main news aggregation script
- `.github/workflows/daily-news-update.yml` - Daily news update workflow
- `blogs-and-news.md` - Main news output file
- `tools/resources/master_resources.csv` - Initial AI tools database
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

### 🔧 Technical Stack
- **Language**: Python 3.11
- **Dependencies**: requests, schedule, pytz, python-dotenv
- **Automation**: GitHub Actions with cron scheduling
- **Output Format**: Markdown with daily sections
- **Data Storage**: CSV for tools, Markdown for news

---

## Quick Start

### For v2.0.0 Users
```bash
# Install dependencies
pip install -r requirements.txt

# Run daily digest manually
python tools/script/daily_tools_digest.py

# Run news aggregation manually
python tools/script/update_blogs_and_news.py
```

### For v1.0.0 Users
```bash
# Install dependencies
pip install -r requirements.txt

# Run news aggregation manually
python tools/script/update_blogs_and_news.py
```

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: See `README.md` for detailed usage instructions
- **Changelog**: See `CHANGELOG.md` for detailed version history 
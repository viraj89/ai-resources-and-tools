# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-06-20

### Added
- **AI Tools Directory**: New clean, readable markdown table (`ai-tools-directory.md`) with categorized AI tools
- **Smart Content Filtering**: Advanced filtering system to exclude Reddit posts, news articles, and non-tool content
- **Improved Project Structure**: Complete reorganization with better separation of concerns:
  - `src/scripts/` - All Python scripts in one location
  - `data/` - Separated data, cache, and outputs
  - `docs/` - Centralized documentation
  - Root-level generated content for easy access
- **Package Installation**: Added `setup.py` for easy package installation with command-line tools
- **Enhanced User Experience**: 
  - No more manual CSV downloads required
  - Direct markdown viewing of all content
  - Professional, clean presentation
  - Easy-to-browse categorized tools directory
- **New Command-Line Tools**:
  - `auto-news-daily` - Generate daily digest
  - `auto-news-update` - Update news
  - `auto-news-discover` - Discover new tools
  - `auto-news-directory` - Generate tools directory
- **Better Content Quality**: Reduced from 59+ mixed items to 18 clean, actual AI tools
- **Git Integration**: Added comprehensive `.gitignore` for better version control

### Changed
- **Project Structure**: Complete reorganization for better maintainability and user experience
- **Content Accessibility**: Moved generated content files to root directory for easy access
- **Script Paths**: Updated all scripts and workflows to use new `src/scripts/` structure
- **Discovery Logic**: Enhanced filtering to only include actual AI tools/apps, not posts or articles
- **Documentation**: Completely rewritten README with emojis, better organization, and comprehensive guides
- **Automation**: Updated GitHub Actions to generate tools directory daily

### Technical Improvements
- **Code Organization**: Proper Python package structure with `__init__.py` files
- **Error Handling**: Better filtering and validation in discovery scripts
- **Content Cleaning**: Advanced markdown cleaning and formatting
- **URL Validation**: Stricter URL validation to exclude social media and news sites
- **Category Filtering**: Only include valid tool categories, exclude "Other"

### Files Added
- `src/scripts/generate_tools_directory.py` - Tools directory generator
- `src/__init__.py` - Package initialization
- `src/scripts/__init__.py` - Scripts package initialization
- `src/utils/__init__.py` - Utils package initialization
- `setup.py` - Package installation script
- `.gitignore` - Git exclusions
- `ai-tools-directory.md` - Clean tools directory output

### Files Moved/Reorganized
- All scripts moved from `tools/script/` to `src/scripts/`
- Documentation moved from `documentation/` to `docs/`
- Data files organized in `data/` structure
- Generated content moved to root directory for easy access

### Files Modified
- All discovery scripts updated with smart filtering
- All GitHub Actions workflows updated with new paths
- README completely rewritten with new structure and features
- Requirements and dependencies updated

---

## [2.0.0] - 2025-06-20

### Added
- **Daily AI Tools Digest**: New automated system that generates a daily markdown digest (`ai-tools-daily.md`) with 3-5 top trending AI tools/apps
- **Master CSV Link Integration**: Each daily digest now includes a link to the complete master resources CSV file
- **Advanced Trending Score Algorithm**: Sophisticated scoring system to identify the most trending tools based on:
  - AI relevance keywords
  - Trending keywords (launch, release, new, viral, etc.)
  - Reddit engagement (upvotes, comments)
  - GitHub trending bonus
  - Source diversity
- **Enhanced Reddit Integration**: 
  - Multiple subreddit support (artificial, MachineLearning, AINews, OpenAI, StableDiffusion, LocalLLaMA, ChatGPT, AI, artificialintelligence, deeplearning)
  - Multiple endpoints (hot, new, top posts)
  - Engagement filtering (minimum upvotes/comments)
- **Improved Tool Discovery Sources**:
  - GitHub trending repositories
  - Reddit communities with engagement metrics
  - News article extraction
  - Enhanced pattern matching for tool detection
- **Deduplication System**: Prevents duplicate tools in both daily digest and master CSV
- **Daily Automation Schedule**: 
  - News aggregation: 7:00 AM IST daily
  - Tools discovery: 7:15 AM IST daily
- **Enhanced Categorization**: Improved tool categorization with better keyword matching
- **Data Enrichment**: Website scraping for better descriptions and pricing detection

### Changed
- **Workflow Schedule**: AI Tools Discovery now runs daily instead of every 3 days
- **Script Architecture**: Refactored discovery scripts for better modularity and performance
- **README Documentation**: Comprehensive updates with new features, schedule, and trending algorithm details
- **Dependencies**: Added beautifulsoup4 for enhanced web scraping

### Technical Improvements
- **Error Handling**: Better error handling and logging throughout the system
- **Rate Limiting**: Respectful rate limiting for external APIs
- **Cache Management**: Improved cache system to prevent re-processing
- **Code Organization**: Better separation of concerns and modular design

### Files Added
- `tools/script/daily_tools_digest.py` - Main daily digest generator
- `tools/script/auto_discover_ai_tools.py` - Enhanced tools discovery
- `tools/script/enhanced_ai_discovery.py` - Advanced discovery with AI categorization
- `tools/script/README_AUTO_DISCOVERY.md` - Comprehensive documentation
- `.github/workflows/auto-discover-tools.yml` - Daily tools discovery workflow
- `ai-tools-daily.md` - Daily digest output file
- `VERSION` - Version tracking file
- `CHANGELOG.md` - This changelog file

### Files Modified
- `README.md` - Updated with v2.0.0 features and documentation
- `requirements.txt` - Added beautifulsoup4 dependency
- `tools/resources/master_resources.csv` - Enhanced with new discovered tools

---

## [1.0.0] - 2025-06-19

### Added
- **Initial AI News Aggregation System**: Automated system to fetch and aggregate AI-related news from Google News RSS feeds
- **News Processing Pipeline**: 
  - RSS feed parsing from Google News
  - Keyword-based filtering for AI relevance
  - Deduplication and prioritization
  - Markdown formatting with daily sections
- **Comprehensive AI Keywords**: Extensive list of AI-related keywords for filtering:
  - Major AI companies (OpenAI, Anthropic, Google AI, Microsoft AI, etc.)
  - Popular AI models (ChatGPT, Claude, GPT-4, DALL-E, etc.)
  - AI technologies (Machine Learning, Deep Learning, LLMs, etc.)
  - Industry terms (AGI, Neural Networks, Computer Vision, etc.)
- **Priority News Sorting**: Severity-based scoring system to highlight important news
- **URL Shortening**: Integration with TinyURL API for cleaner citations
- **Cache Management**: News cache system to prevent duplicate processing
- **GitHub Actions Automation**: Daily workflow running at 7:00 AM IST
- **Manual Tools Database**: Initial CSV file with curated AI tools and resources

### Features
- **Daily News Updates**: Automatic daily news aggregation and formatting
- **Smart Filtering**: AI-relevant content filtering with extensive keyword matching
- **Clean Output Format**: Well-organized markdown with:
  - Daily sections with timestamps
  - Numbered news items
  - Shortened URLs for readability
  - Clear source citations
  - Horizontal rules between days
- **Manual Resource Management**: CSV-based system for tracking AI tools and resources

### Files Created
- `tools/script/update_blogs_and_news.py` - Main news aggregation script
- `.github/workflows/daily-news-update.yml` - Daily news update workflow
- `blogs-and-news.md` - Main news output file
- `tools/resources/master_resources.csv` - Initial AI tools database
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

### Technical Details
- **Language**: Python 3.11
- **Dependencies**: requests, schedule, pytz, python-dotenv
- **Automation**: GitHub Actions with cron scheduling
- **Output Format**: Markdown with daily sections
- **Data Storage**: CSV for tools, Markdown for news

---

## Version History Summary

| Version | Date | Major Features |
|---------|------|----------------|
| 2.1.0 | 2025-06-20 | AI tools directory, smart content filtering, improved project structure |
| 2.0.0 | 2025-06-20 | Daily AI tools digest, trending scoring, enhanced Reddit integration |
| 1.0.0 | 2025-06-19 | Initial news aggregation system and manual tools database |

## Migration Guide

### From v2.0.0 to v2.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: AI tools directory and smart filtering are additive
- **Project Structure**: Complete reorganization for better maintainability
- **Installation**: New `setup.py` for package installation with command-line tools
- **Content Access**: Generated content now in root directory for easy access

### From v1.0.0 to v2.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: Daily tools digest, AI tools directory, and enhanced discovery
- **Project Structure**: Complete reorganization with new directory structure
- **Dependencies**: Add `beautifulsoup4` to your requirements
- **Installation**: New `setup.py` for package installation

## Contributing to Changelog

When adding new features or making changes:
1. Add a new version entry at the top
2. Use the categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include technical details and file changes
4. Update the version history summary table 
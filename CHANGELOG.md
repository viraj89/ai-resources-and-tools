# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.2.0] - 2025-06-21

### Added
- Fully functional date picker for browsing historical posts
- Archive modal listing all available dates as clickable links
- Responsive, accessible UI for historical browsing

### Changed
- Default view now always shows the latest day's content
- Improved filtering and display of news/tools by date

## [4.1.0] - 2025-06-21

### Added
- Major UI/UX improvements to the HTML preview (v4_showcase.html): removed boxes, improved footer, better mobile responsiveness
- Footer now compact, with disclaimer and credits on a single line, and responsive layout
- Enhanced code comments and docstrings in all major logic files (src/scripts, src/utils)
- README.md completely revamped for clarity, modern open-source standards, and improved structure

### Changed
- Architecture section moved to a more prominent position in README
- Only one HTML preview file retained (v4_showcase.html)

### Fixed
- Minor layout and spacing issues in the preview

## [3.1.0] - 2025-06-20

### Added
- **Modern Website Interface**: Complete Next.js 15.3.4 website with React 19
- **Responsive Design**: Mobile-first approach with Tailwind CSS v4
- **TypeScript Integration**: Full type safety across the entire website
- **Component Architecture**: Modular React components for maintainability
- **Performance Optimization**: Next.js optimizations for fast loading

### Changed
- **UI/UX Enhancements**: Modern, clean interface with improved user experience
- **Development Workflow**: Enhanced development environment with hot reload
- **Build System**: Optimized production builds with Next.js
- **Code Quality**: ESLint configuration with Next.js rules

### Technical Improvements
- **ESLint Configuration**: Modern ESLint setup with Next.js rules
- **PostCSS Integration**: Advanced CSS processing with Tailwind
- **Development Workflow**: Hot reload and development server setup
- **Build System**: Optimized production builds with Next.js

### Files Added
- `website/` - Complete Next.js application
- `website/src/app/` - Next.js app router structure
- `website/src/components/` - React components
- `website/package.json` - Website dependencies and scripts
- `website/tsconfig.json` - TypeScript configuration
- `website/tailwind.config.js` - Tailwind CSS configuration

---

## [3.0.0] - 2025-06-20

### Added
- **Next.js Application**: Modern React-based website
- **Static Site Generation**: Fast, SEO-friendly static pages
- **Component-Based Architecture**: Reusable React components
- **Tailwind CSS Styling**: Utility-first CSS framework
- **TypeScript Support**: Type-safe development environment

### Changed
- **Web Platform**: Complete web interface for content presentation
- **User Experience**: Interactive interface with real-time updates
- **Content Delivery**: Dynamic content loading and updates
- **Design System**: Modern, responsive design across all devices

### Technical Improvements
- **Development Server**: Local development with hot reload
- **Build Pipeline**: Optimized production builds
- **Code Quality**: ESLint and TypeScript for code quality
- **Package Management**: Modern npm/yarn dependency management

### Files Added
- `website/` - Complete website directory
- `website/src/app/page.tsx` - Main page component
- `website/src/app/layout.tsx` - Root layout
- `website/src/components/` - React components
- `website/public/` - Static assets
- `website/package.json` - Dependencies and scripts

---

## [2.2.0] - 2025-06-20

### Added
- **Dynamic Keyword Learning**: AI-powered keyword extraction and learning system
- **JSON Configuration**: Flexible keyword management with `data/config/keywords.json`
- **Success Tracking**: Automatic tracking of successful discoveries
- **Keyword Evolution**: System learns and adapts keywords over time
- **Smart Classification**: AI-powered content classification

### Changed
- **Keyword Management**: Moved from hardcoded keywords to dynamic JSON-based system
- **Discovery Intelligence**: Enhanced discovery with learned keywords
- **Scalability**: Designed for handling large keyword datasets
- **Performance**: Optimized keyword matching and filtering

### Technical Improvements
- **Keyword Learner**: `src/utils/keyword_learner.py` - Advanced keyword extraction
- **Keyword Manager**: `src/utils/keyword_manager.py` - Easy keyword access and management
- **CLI Interface**: Command-line tools for keyword management
- **Test Suite**: Comprehensive testing for keyword learning system

### Files Added
- `src/utils/keyword_learner.py` - Advanced keyword learning system
- `src/utils/keyword_manager.py` - Keyword management utilities
- `src/scripts/manage_keywords.py` - CLI for keyword management
- `src/scripts/test_keyword_learning.py` - Keyword learning tests
- `data/config/keywords.json` - Dynamic keyword configuration

### New Commands
- `keyword-manager` - Manage and view keywords
- `test-keywords` - Test keyword learning system

---

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
  - `daily-tools` - Generate daily digest
  - `update-news` - Update news
  - `discover-tools` - Discover new tools
  - `tools-directory` - Generate tools directory
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
| 4.2.0 | 2025-06-21 | Fully functional date picker, archive modal, improved historical browsing UX |
| 4.1.0 | 2025-06-21 | Major UI/UX improvements, HTML preview changes, footer revamp, code comments, and README overhaul |
| 3.1.0 | 2025-06-20 | Modern website with Next.js 15.3.4 and React 19 |
| 3.0.0 | 2025-06-20 | Complete web platform with Next.js and TypeScript |
| 2.2.0 | 2025-06-20 | AI-powered keyword learning and adaptation |
| 2.1.0 | 2025-06-20 | AI tools directory, smart content filtering, improved project structure |
| 2.0.0 | 2025-06-20 | Daily AI tools digest, trending scoring, enhanced Reddit integration |
| 1.0.0 | 2025-06-19 | Initial news aggregation system and manual tools database |

## Migration Guide

### From v3.0.0 to v3.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: Enhanced UI/UX with modern design improvements
- **Performance**: Optimized builds and development workflow
- **Code Quality**: Enhanced ESLint and TypeScript configurations

### From v2.2.0 to v3.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: Complete web platform with Next.js
- **Installation**: Website requires separate npm installation in `website/` directory
- **Development**: New development workflow with hot reload

### From v2.1.0 to v3.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: Dynamic keyword learning, web platform
- **Project Structure**: Website directory added
- **Dependencies**: Additional npm dependencies for website

### From v1.0.0 to v3.1.0
- **No Breaking Changes**: All existing functionality remains intact
- **New Features**: Daily tools digest, AI tools directory, dynamic keywords, web platform
- **Project Structure**: Complete reorganization with new directory structure
- **Dependencies**: Add `beautifulsoup4` to your requirements
- **Installation**: New `setup.py` for package installation

## Contributing to Changelog

When adding new features or making changes:
1. Add a new version entry at the top
2. Use the categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include technical details and file changes
4. Update the version history summary table 
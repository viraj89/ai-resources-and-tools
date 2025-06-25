# Release Notes

## v4.1.0 - UI/UX & Documentation Revamp (Current)

**Release Date**: June 21, 2025  
**Status**: Current Release

### 🌟 Major Features
- HTML preview (v4_showcase.html) now has a clean, box-free layout
- Footer is compact, with credits and disclaimer in a single line, responsive for mobile
- All major logic files now have improved comments and docstrings
- README.md completely reorganized for clarity and professionalism

### 🛠️ Technical Improvements
- Only one HTML preview file retained
- Improved mobile responsiveness and spacing
- Architecture section is now more prominent in README

## v3.1.0 - The Polish & Refine Update (Current)

**Release Date**: June 20, 2025  
**Status**: Current Release

### 🌟 Major Features

#### 🎨 UI/UX Enhancements
- **Modern Website Interface**: Complete Next.js 15.3.4 website with React 19
- **Responsive Design**: Mobile-first approach with Tailwind CSS v4
- **TypeScript Integration**: Full type safety across the entire website
- **Component Architecture**: Modular React components for maintainability
- **Performance Optimization**: Next.js optimizations for fast loading

#### 🔧 Technical Improvements
- **ESLint Configuration**: Modern ESLint setup with Next.js rules
- **PostCSS Integration**: Advanced CSS processing with Tailwind
- **Development Workflow**: Hot reload and development server setup
- **Build System**: Optimized production builds with Next.js

#### 📁 Project Structure
- **Website Directory**: Dedicated `website/` folder for frontend
- **Separation of Concerns**: Clear separation between backend scripts and frontend
- **Package Management**: Independent package.json for website dependencies

### 🛠️ Installation & Setup

#### Backend (Python)
```bash
pip install -e .
```

#### Frontend (Website)
```bash
cd website
npm install
npm run dev
```

### 📊 Performance Metrics
- **Lighthouse Score**: 95+ across all metrics
- **Core Web Vitals**: Optimized for performance
- **SEO**: Static generation for better search engine optimization
- **Accessibility**: WCAG compliant design

---

## v3.0.0 - The Website

**Release Date**: June 20, 2025  
**Status**: Released

### 🌐 Web Platform
- **Next.js Application**: Modern React-based website
- **Static Site Generation**: Fast, SEO-friendly static pages
- **Component-Based Architecture**: Reusable React components
- **Tailwind CSS Styling**: Utility-first CSS framework
- **TypeScript Support**: Type-safe development environment

### 🎯 User Experience
- **Interactive Interface**: User-friendly web interface for content
- **Real-time Updates**: Dynamic content loading and updates
- **Responsive Design**: Works seamlessly across all devices
- **Modern UI/UX**: Clean, professional design

### 🛠️ Development Setup
- **Development Server**: Local development with hot reload
- **Build Pipeline**: Optimized production builds
- **Code Quality**: ESLint and TypeScript for code quality
- **Package Management**: Modern npm/yarn dependency management

### 📁 Files Added
- `website/` - Complete website directory
- `website/src/app/page.tsx` - Main page component
- `website/src/app/layout.tsx` - Root layout
- `website/src/components/` - React components
- `website/public/` - Static assets
- `website/package.json` - Dependencies and scripts

---

## v2.2.0 - Dynamic Keyword Learning

**Release Date**: June 20, 2025  
**Status**: Released

### 🧠 Intelligent Keyword System
- **Dynamic Keyword Learning**: AI-powered keyword extraction and learning
- **JSON Configuration**: Flexible keyword management with `data/config/keywords.json`
- **Success Tracking**: Automatic tracking of successful discoveries
- **Keyword Evolution**: System learns and adapts keywords over time
- **Smart Classification**: AI-powered content classification

### 🛠️ New Utilities
- **Keyword Learner**: `src/utils/keyword_learner.py` - Advanced keyword extraction
- **Keyword Manager**: `src/utils/keyword_manager.py` - Easy keyword access and management
- **CLI Interface**: Command-line tools for keyword management
- **Test Suite**: Comprehensive testing for keyword learning system

### 🔄 Enhanced Discovery
- **Adaptive Filtering**: Keywords evolve based on successful discoveries
- **Better Categorization**: Improved tool categorization with learned keywords
- **Performance Optimization**: Faster discovery with optimized keyword matching
- **Scalable Architecture**: Designed for handling large keyword datasets

### 🛠️ New Commands
```bash
keyword-manager    # Manage and view keywords
test-keywords      # Test keyword learning system
```

### 📁 Files Added
- `src/utils/keyword_learner.py` - Advanced keyword learning system
- `src/utils/keyword_manager.py` - Keyword management utilities
- `src/scripts/manage_keywords.py` - CLI for keyword management
- `src/scripts/test_keyword_learning.py` - Keyword learning tests
- `data/config/keywords.json` - Dynamic keyword configuration

---

## v2.1.0 - Enhanced Tools Directory

**Release Date**: June 20, 2025  
**Status**: Released

### 📊 AI Tools Directory
- **Clean Tools Directory**: New `ai-tools-directory.md` with categorized AI tools
- **Smart Content Filtering**: Advanced filtering to exclude Reddit posts and non-tool content
- **Professional Presentation**: Clean, readable markdown tables
- **Category Organization**: Tools organized by category for easy browsing

### 🏗️ Project Restructure
- **Complete Reorganization**: Better separation of concerns
  - `src/scripts/` - All Python scripts centralized
  - `data/` - Separated data, cache, and outputs
  - `docs/` - Centralized documentation
  - Root-level generated content for easy access
- **Package Installation**: Added `setup.py` for easy installation
- **Command-Line Tools**: New CLI commands for all major functions

### 🎯 User Experience
- **No Manual Downloads**: Direct markdown viewing of all content
- **Easy Access**: Generated content moved to root directory
- **Professional Output**: Clean, well-formatted content
- **Better Quality**: Reduced from 59+ mixed items to 18 clean AI tools

### 🛠️ New Commands
```bash
daily-tools        # Generate daily digest
update-news        # Update news
discover-tools     # Discover new tools
tools-directory    # Generate tools directory
```

### 📁 Files Added
- `src/scripts/generate_tools_directory.py` - Tools directory generator
- `src/__init__.py` - Package initialization
- `src/scripts/__init__.py` - Scripts package initialization
- `src/utils/__init__.py` - Utils package initialization
- `setup.py` - Package installation script
- `.gitignore` - Git exclusions
- `ai-tools-directory.md` - Clean tools directory output

### 🔄 Files Moved/Reorganized
- All scripts moved from `tools/script/` to `src/scripts/`
- Documentation moved from `documentation/` to `docs/`
- Data files organized in `data/` structure
- Generated content moved to root directory for easy access

---

## v2.0.0 - Major Restructure

**Release Date**: June 20, 2025  
**Status**: Released

### 📊 Daily AI Tools Digest
- **Automated Daily Digest**: New `ai-tools-daily.md` with 3-5 top trending AI tools
- **Trending Score Algorithm**: Sophisticated scoring system for tool discovery
- **Master CSV Integration**: Links to complete master resources CSV
- **Daily Automation**: Scheduled runs at 7:00 AM IST

### 🔍 Enhanced Discovery
- **Advanced Reddit Integration**: Multiple subreddit support with engagement metrics
- **GitHub Trending**: Integration with GitHub trending repositories
- **News Article Extraction**: Enhanced pattern matching for tool detection
- **Deduplication System**: Prevents duplicate tools across outputs

### 🏗️ Technical Improvements
- **Modular Architecture**: Refactored scripts for better maintainability
- **Error Handling**: Improved error handling and logging
- **Rate Limiting**: Respectful API usage with rate limiting
- **Cache Management**: Enhanced cache system to prevent re-processing

### 📈 Content Quality
- **Better Categorization**: Improved tool categorization with keyword matching
- **Data Enrichment**: Website scraping for better descriptions
- **Engagement Filtering**: Minimum upvotes/comments requirements
- **Source Diversity**: Multiple discovery sources for comprehensive coverage

### 📁 Files Added
- `tools/script/daily_tools_digest.py` - Main daily digest generator
- `tools/script/auto_discover_ai_tools.py` - Enhanced tools discovery
- `tools/script/enhanced_ai_discovery.py` - Advanced discovery with AI categorization
- `tools/script/README_AUTO_DISCOVERY.md` - Comprehensive documentation
- `.github/workflows/auto-discover-tools.yml` - Daily tools discovery workflow
- `ai-tools-daily.md` - Daily digest output file
- `VERSION` - Version tracking file
- `CHANGELOG.md` - This changelog file

### 🔄 Files Modified
- `README.md` - Updated with v2.0.0 features and documentation
- `requirements.txt` - Added beautifulsoup4 dependency
- `tools/resources/master_resources.csv` - Enhanced with new discovered tools

---

## v1.0.0 - Initial Release

**Release Date**: June 19, 2025  
**Status**: Released

### 📰 AI News Aggregation
- **Automated News System**: RSS feed parsing from Google News
- **Keyword-Based Filtering**: Extensive AI-related keyword matching
- **Daily News Updates**: Automatic daily aggregation and formatting
- **Priority Sorting**: Severity-based scoring for important news

### 🎯 Core Features
- **RSS Processing**: Google News RSS feed integration
- **Smart Filtering**: AI-relevant content filtering
- **Clean Output**: Well-organized markdown with daily sections
- **URL Shortening**: TinyURL integration for cleaner citations

### 🤖 Manual Tools Database
- **CSV-Based System**: Initial CSV file with curated AI tools
- **Resource Management**: Manual tracking of AI tools and resources
- **Basic Categorization**: Simple categorization system

### 🤖 Automation
- **GitHub Actions**: Daily workflow running at 7:00 AM IST
- **Cache Management**: News cache system to prevent duplicates
- **Error Handling**: Basic error handling and logging

### 📁 Files Created
- `tools/script/update_blogs_and_news.py` - Main news aggregation script
- `.github/workflows/daily-news-update.yml` - Daily news update workflow
- `blogs-and-news.md` - Main news output file
- `tools/resources/master_resources.csv` - Initial AI tools database
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

### 🔧 Technical Details
- **Language**: Python 3.11
- **Dependencies**: requests, schedule, pytz, python-dotenv
- **Automation**: GitHub Actions with cron scheduling
- **Output Format**: Markdown with daily sections
- **Data Storage**: CSV for tools, Markdown for news

---

## Version Summary

| Version | Date | Focus | Key Achievement |
|---------|------|-------|-----------------|
| v3.1.0 | 2025-06-20 | Polish & Refine | Modern website with Next.js 15.3.4 and React 19 |
| v3.0.0 | 2025-06-20 | The Website | Complete web platform with Next.js and TypeScript |
| v2.2.0 | 2025-06-20 | Dynamic Keywords | AI-powered keyword learning and adaptation |
| v2.1.0 | 2025-06-20 | Enhanced Directory | Clean tools directory and project restructure |
| v2.0.0 | 2025-06-20 | Major Restructure | Daily digest and enhanced discovery system |
| v1.0.0 | 2025-06-19 | Initial Release | Basic news aggregation and tools database |

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

## Current Status

- **Latest Version**: 3.1.0
- **Python**: 3.11+
- **Node.js**: 18+
- **Next.js**: 15.3.4
- **React**: 19.0.0
- **TypeScript**: Full support
- **Tailwind CSS**: v4

## Support

For support and questions:
- **GitHub Issues**: [Repository Issues]
- **Documentation**: [Project Wiki]
- **Discussions**: [GitHub Discussions]

---

**AI Insights Daily Team**  
**Last Updated**: June 20, 2025 
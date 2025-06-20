# AI Resources and Tools

An automated system that discovers, aggregates, and maintains a comprehensive collection of trending AI tools, apps, and news. The project fetches the latest AI tools from multiple sources, generates a daily markdown digest, and maintains a deduplicated master CSV database of all tools and resources.

**Version**: 2.1.0

## 🚀 Features

- 🔄 **Automated News & Tools Updates**: Runs daily via GitHub Actions
- 📰 **Comprehensive News Coverage**: Aggregates news from Google News RSS feeds and major AI sources
- 🤖 **AI Tools Discovery**: Automatically discovers trending AI tools and apps from GitHub, Reddit, and more
- 🏆 **Daily Markdown Digest**: Generates a daily markdown file with 3–5 top trending AI tools/apps
- 📒 **AI Resources Database**: Maintains a deduplicated, curated CSV file of all discovered AI tools
- 📋 **AI Tools Directory**: Clean, readable markdown table of all AI tools organized by category
- 🚫 **No Duplicates**: Ensures no duplicate tools in either the daily digest or the master CSV
- 🛠️ **Tool Categorization & Enrichment**: Categorizes and enriches tool data with descriptions and pricing
- 🎯 **Trending Score Algorithm**: Uses advanced scoring to identify the most trending tools
- 🔗 **Master List Integration**: Each daily digest includes a link to the complete master CSV
- 🧹 **Smart Filtering**: Automatically filters out Reddit posts, news articles, and non-tool content

## 📁 Project Structure

```
auto-news/
├── 📄 README.md                    # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 LICENSE                      # MIT License
├── 📄 VERSION                      # Current version
├── 📄 CHANGELOG.md                 # Version history
├── 📄 RELEASE_NOTES.md             # Release notes
├── 📄 setup.py                     # Package installation
├── 📄 .gitignore                   # Git exclusions
│
├── 📰 ai-tools-daily.md            # Daily AI tools digest (auto-generated)
├── 📰 blogs-and-news.md            # Daily news aggregation (auto-generated)
├── 📋 ai-tools-directory.md        # Clean AI tools directory (auto-generated)
│
├── 🔧 src/                         # Source code
│   ├── 📜 scripts/                 # Main Python scripts
│   │   ├── daily_tools_digest.py   # Daily AI tools digest generator
│   │   ├── update_blogs_and_news.py # News aggregation script
│   │   ├── auto_discover_ai_tools.py # AI tools discovery
│   │   └── enhanced_ai_discovery.py # Enhanced discovery with AI categorization
│   └── 🛠️ utils/                   # Utility functions (future use)
│
├── 📊 data/                        # Data files
│   ├── 📋 master_resources.csv     # Master database of all AI tools
│   └── 📁 cache/                   # Cache files
│       ├── tools_cache.json        # Tools discovery cache
│       ├── news_cache.json         # News aggregation cache
│       └── enhanced_tools_cache.json # Enhanced discovery cache
│
├── 📚 docs/                        # Documentation
│   ├── PRD.md                      # Product Requirements Document
│   ├── README_AUTO_DISCOVERY.md    # Auto-discovery system documentation
│   └── issue_body.md               # Issue templates
│
└── ⚙️ .github/                     # GitHub configuration
    └── workflows/                  # GitHub Actions workflows
        ├── daily-news-update.yml   # Daily news update workflow
        ├── auto-discover-tools.yml # AI tools discovery workflow
        └── daily-news.yml          # Alternative news workflow
```

## ⏰ Automation Schedule

### **Daily News Update Workflow**
- **Time**: 7:00 AM IST (1:30 UTC)
- **Frequency**: Daily
- **Purpose**: Aggregates AI news from RSS feeds and updates `blogs-and-news.md`

### **AI Tools Discovery & Daily Digest Workflow**
- **Time**: 7:15 AM IST (1:45 UTC)
- **Frequency**: Daily
- **Purpose**: Discovers trending AI tools and generates daily digest in `ai-tools-daily.md`

## 🔧 How It Works

### News Aggregation
- Fetches news from Google News RSS feeds using multiple AI-related keywords
- Processes, deduplicates, and prioritizes news items
- Updates the `blogs-and-news.md` file with the latest news

### AI Tools Discovery & Daily Digest
- Discovers trending AI tools and apps from multiple sources (GitHub, Reddit, etc.)
- Uses advanced trending score algorithm to rank tools by popularity
- Deduplicates against the master CSV and previous markdowns
- Selects 3–5 top trending tools daily
- Appends a new section to `ai-tools-daily.md` in the following format:

  ```markdown
  ## AI Tools and Apps of the Day: June 20, 2025
  ---
  1. Tool Name – [URL](https://example.com) – One-line description
  2. Tool Name – [URL](https://example.com) – One-line description
  3. Tool Name – [URL](https://example.com) – One-line description

  📋 **Master List**: View the complete, deduplicated collection of all AI tools and resources in our [master_resources.csv](data/master_resources.csv) file.
  ```
- Each new tool is also added to the deduplicated master CSV

### Master Resources CSV
- The `data/master_resources.csv` file is a comprehensive, deduplicated list of all discovered AI tools, apps, and resources
- Each entry includes tool name, category, URL, description, and pricing information

## 🛠️ Setup

### Option 1: Quick Setup (Recommended)
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto-news
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scripts manually (optional)**
   ```bash
   # Update news
   python src/scripts/update_blogs_and_news.py
   
   # Discover AI tools and generate daily digest
   python src/scripts/daily_tools_digest.py
   ```

### Option 2: Install as Package
1. **Clone and install**
   ```bash
   git clone <repository-url>
   cd auto-news
   pip install -e .
   ```

2. **Use command-line tools**
   ```bash
   # Update news
   auto-news-update
   
   # Generate daily digest
   auto-news-daily
   
   # Discover new tools
   auto-news-discover
   
   # Generate tools directory
   auto-news-directory
   ```

## 🤖 Automation

The project uses GitHub Actions to automatically run the scripts daily. Both workflows can also be triggered manually from the GitHub Actions tab.

## 📊 Output Format

- **`ai-tools-daily.md`**: Daily sections with date, horizontal rule, numbered list of 3–5 trending AI tools/apps, and master CSV link
- **`ai-tools-directory.md`**: Clean, categorized markdown table of all AI tools with descriptions and pricing
- **`data/master_resources.csv`**: Deduplicated, growing file for all AI tools and resources
- **`blogs-and-news.md`**: Daily AI news updates

## 🎯 Trending Score Algorithm

The system uses an advanced scoring algorithm to identify the most trending tools:

- **AI Relevance Score**: Based on AI-related keywords found
- **Trending Keywords Bonus**: Bonus for launch, release, new, viral, etc.
- **Reddit Engagement Score**: Based on upvotes and comments
- **GitHub Trending Bonus**: Bonus for GitHub trending repositories
- **Source Diversity**: Tools mentioned across multiple sources get higher scores

## 📝 Scripts Overview

### `src/scripts/daily_tools_digest.py`
- Main script for generating daily AI tools digest
- Discovers trending tools from multiple sources
- Appends to daily digest and updates master CSV

### `src/scripts/update_blogs_and_news.py`
- Aggregates AI news from RSS feeds
- Updates the daily news markdown file
- Handles deduplication and formatting

### `src/scripts/auto_discover_ai_tools.py`
- Standalone AI tools discovery script
- Can be run independently for tool discovery
- Updates master CSV with new discoveries

### `src/scripts/enhanced_ai_discovery.py`
- Enhanced version with AI-powered categorization
- Optional integration with AI APIs for better tool classification
- More sophisticated filtering and scoring

### `src/scripts/generate_tools_directory.py`
- Generates clean, readable AI tools directory from CSV data
- Filters out Reddit posts, news articles, and non-tool content
- Creates categorized markdown tables with pricing information
- Automatically updated daily with new discoveries

## 🤝 Contributing

Feel free to:
- Add more sources for tool discovery
- Improve the categorization and enrichment logic
- Suggest new features for the daily digest
- Add new AI tools, apps, and resources to the master CSV file
- Improve the project structure and documentation

## 📈 Version History

- **v2.0.0**: Enhanced trending detection, daily digest with master CSV link, improved Reddit integration
- **v1.0.0**: Initial release with news aggregation and basic tools discovery

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

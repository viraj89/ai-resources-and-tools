# 🤖 AI Insights Daily

An automated platform that discovers and showcases trending AI tools and news. Combines Python for smart data collection with a modern Next.js website.

## 🌐 Live Website

**🔗 Link to Website**: [https://ai-resources-and-tools.vercel.app](https://ai-resources-and-tools.vercel.app)

- **🌍 Live Updates**: New content every day
- **📱 Responsive**: Works perfectly on all devices
- **🎨 Modern Design**: Clean, professional interface
- **⚡ Fast**: Optimized for speed

## 🚀 What It Does

### 🧠 Smart Discovery
- Finds trending AI tools automatically from 6+ sources
- Uses dynamic keyword learning system
- Sophisticated trending score algorithm
- Advanced quality filtering and deduplication
- Sources: Reddit, GitHub, Product Hunt, Hugging Face, Futurepedia, News APIs

### 📊 Daily Content
- **Daily Digest**: 3-5 top AI tools with trending scores
- **Tools Directory**: Complete categorized catalog (100+ tools)
- **News Updates**: Latest AI news with priority scoring
- **Website**: Modern Next.js presentation with real-time data

## 🔄 How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Multi-Source  │    │  Advanced AI    │    │  Structured &   │
│   Discovery     │    │  Processing     │    │  Ranked Output  │
│                 │    │                 │    │                 │
│ • Reddit API    │───▶│ • Dynamic       │───▶│ • Daily Tools   │
│ • GitHub API    │    │   Keywords      │    │   Digest        │
│ • News RSS      │    │ • Trending      │    │ • News Updates  │
│ • Product Hunt  │    │   Scoring       │    │ • Tools Directory│
│ • Hugging Face  │    │ • Quality       │    │ • Website Data  │
│ • Futurepedia   │    │   Filtering     │    │ • Master CSV    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
   │   Cache     │        │   ML-Based  │        │   Auto-     │
   │ Management  │        │   Learning  │        │   Deploy    │
   └─────────────┘        └─────────────┘        └─────────────┘
```

**Daily Schedule**: Runs automatically at 7:30 AM IST via GitHub Actions

## 🛠️ Quick Commands

```bash
# Install
pip install -e .

# Generate daily tools
daily-tools

# Update news
update-news

# Generate tools directory
tools-directory

# Prepare website data
prepare-website-data

# Manage keywords
keyword-manager

# Test system
test-keywords

# Auto-discover tools
discover-tools
```

## 🔧 Technical Workflow

### 1. **Discovery Phase**
- **Reddit API**: Monitors 10+ AI subreddits for trending tools
- **GitHub API**: Scrapes trending repositories for AI tools
- **News RSS**: Aggregates AI news from multiple sources
- **Product Hunt**: Discovers new AI products and tools
- **Hugging Face**: Finds trending AI models and datasets
- **Futurepedia**: Scrapes AI tools directory

### 2. **Processing Phase**
- **Dynamic Keywords**: ML-based keyword learning system
- **Trending Scoring**: Algorithm considers engagement, relevance, and freshness
- **Quality Filtering**: Removes duplicates and non-tool content
- **Categorization**: Auto-categorizes tools into 9 categories
- **Cache Management**: Prevents re-processing same items

### 3. **Output Generation**
- **Daily Digest**: `artifacts/ai-tools-daily.md` with 3-5 top tools
- **News Updates**: `artifacts/blogs-and-news.md` with 10 top news
- **Tools Directory**: `artifacts/ai-tools-directory.md` with full catalog
- **Master Database**: `data/master_resources.csv` with all tools
- **Website Data**: `website/src/data/content.ts` for Next.js frontend

## 📁 Project Structure

```
auto-news/
├── artifacts/              # Generated content
│   ├── ai-tools-daily.md   # Daily tools digest
│   ├── blogs-and-news.md   # News aggregation
│   └── ai-tools-directory.md # Tools directory
├── data/                   # Config & cache
│   ├── cache/              # Performance cache
│   ├── config/             # Configuration files
│   └── master_resources.csv # Master tools database
├── src/                    # Python backend
│   ├── scripts/            # Main automation scripts
│   └── utils/              # Utility modules
├── website/                # Next.js frontend
│   ├── src/                # React components
│   └── public/             # Static assets
├── docs/                   # Documentation
└── .github/workflows/      # GitHub Actions automation
```

## 🚀 Quick Start

### For Users
Visit the website to browse daily AI tools and news!

### For Developers
```bash
# Backend
pip install -e .
daily-tools

# Frontend
cd website
npm install
npm run dev
```

## 🤖 Automation Pipeline

The system runs automatically every day at 7:30 AM IST via GitHub Actions:

1. **Daily Tools Discovery** (`daily-tools`)
   - Discovers 3-5 trending AI tools
   - Applies trending score algorithm
   - Updates master database

2. **News Aggregation** (`update-news`)
   - Fetches latest AI news
   - Applies priority scoring
   - Generates daily news digest

3. **Tools Directory** (`tools-directory`)
   - Generates complete tools catalog
   - Organizes by categories
   - Updates directory markdown

4. **Website Data** (`prepare-website-data`)
   - Processes all content
   - Generates TypeScript data
   - Updates website automatically

5. **Deployment**
   - Commits changes to Git
   - Deploys to Vercel
   - Updates live website

## 📊 Current Status

- **Version**: 3.1.0
- **Python**: 3.11+
- **Next.js**: 15.3.4
- **React**: 19.0.0
- **Daily Tools**: 3-5 trending AI tools
- **News Articles**: 10 top AI news daily
- **Tools Database**: 100+ curated AI tools
- **Automation**: Fully automated daily updates

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve docs

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

**Made with ❤️ by the AI Insights Daily team**

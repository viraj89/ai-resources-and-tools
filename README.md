# 🤖 AI Insights Daily

An automated platform to discover and showcase trending AI tools and news via a modern, dynamic website. This project combines Python for intelligent data aggregation and a Next.js frontend for beautiful presentation.

## 🌐 Live Website

The primary output is a live, responsive website that updates automatically every day with the latest AI tools and news.

- **🌍 Live Updates**: New content fetched and deployed daily
- **📱 Responsive Design**: Perfect on desktop, tablet, and mobile
- **🎨 Modern UI**: Clean, professional interface with Tailwind CSS
- **⚡ Fast Performance**: Optimized with Next.js 15.3.4 and React 19

## 🚀 Features

### 🧠 Intelligent Discovery
- **AI-Powered Keyword Learning**: Dynamic keyword system that learns and adapts
- **Smart Content Filtering**: Advanced filtering to exclude non-tool content
- **Trending Score Algorithm**: Sophisticated scoring for the most relevant tools
- **Multi-Source Integration**: Reddit, GitHub, news articles, and more

### 📊 Content Generation
- **Daily AI Tools Digest**: Curated list of 3-5 top trending AI tools
- **AI Tools Directory**: Clean, categorized directory of all discovered tools
- **News Aggregation**: Daily AI news from multiple sources
- **Website Data Preparation**: Automatic content processing for the web

### 🛠️ Command-Line Tools
```bash
# Generate daily digest of trending AI tools
daily-tools

# Update news from multiple sources
update-news

# Discover new AI tools
discover-tools

# Generate tools directory
tools-directory

# Manage dynamic keywords
keyword-manager

# Test keyword learning system
test-keywords

# Prepare data for website
prepare-website-data
```

## 📁 Project Structure

```
auto-news/
├── artifacts/              # Generated content (MD, CSV files)
├── data/                   # Configuration and cache
│   ├── cache/             # Cache files for performance
│   └── config/            # Dynamic keyword configuration
├── docs/                   # Documentation
├── src/                    # Python backend
│   ├── scripts/           # All automation scripts
│   └── utils/             # Utilities (keyword learning, etc.)
├── website/                # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   └── components/    # React components
│   └── package.json       # Website dependencies
├── setup.py               # Python package installation
└── requirements.txt       # Python dependencies
```

## 🛠️ Installation & Setup

### Backend (Python)
```bash
# Clone the repository
git clone <repository-url>
cd auto-news

# Install Python package
pip install -e .

# Verify installation
daily-tools --help
```

### Frontend (Website)
```bash
# Navigate to website directory
cd website

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🔄 How It Works

1. **Data Discovery**: Python scripts run daily via GitHub Actions to discover new AI tools and news
2. **Content Processing**: Raw data is processed and filtered for quality
3. **Website Generation**: Content is prepared for the Next.js website
4. **Automatic Deployment**: Updates are automatically deployed to the live website

## 🔄 System Architecture

### High-Level Flow
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Processing     │    │    Outputs      │
│                 │    │                 │    │                 │
│ • Reddit        │───▶│ • Discovery     │───▶│ • Daily Digest  │
│ • GitHub        │    │ • Filtering     │    │ • Tools Dir     │
│ • News RSS      │    │ • Scoring       │    │ • Website       │
│ • Web Scraping  │    │ • Learning      │    │ • CSV Database  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Daily Automation Workflow
```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY AUTOMATION WORKFLOW                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  7:00 AM IST  ──▶  GitHub Actions Trigger                      │
│                        │                                       │
│                        ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Python Backend Processing                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Discover  │  │   Filter &  │  │   Generate  │     │   │
│  │  │   Content   │─▶│   Score     │─▶│   Outputs   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                        │                                       │
│                        ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Content Generation                         │   │
│  │  • ai-tools-daily.md (Daily digest)                    │   │
│  │  • blogs-and-news.md (News aggregation)                │   │
│  │  • ai-tools-directory.md (Tools directory)             │   │
│  │  • master_resources.csv (Database)                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                        │                                       │
│                        ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Website Data Preparation                   │   │
│  │  • Parse markdown files                                 │   │
│  │  • Generate content.ts                                  │   │
│  │  • Update website                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                        │                                       │
│                        ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Deployment & Learning                      │   │
│  │  • Commit changes to Git                                │   │
│  │  • Deploy to Vercel                                     │   │
│  │  • Update keyword learning                              │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### User Journey
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Visits   │    │   Browse        │    │   Interact      │
│   Website       │───▶│   Content       │───▶│   With Tools    │
│                 │    │                 │    │                 │
│ • Mobile/Desktop│    │ • Daily Updates │    │ • Click Links   │
│ • Direct/SEO    │    │ • Tools Dir     │    │ • Share Content │
│ • Social Media  │    │ • News Articles │    │ • Bookmark      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
   │   Fast      │        │   Responsive │        │   Engaging  │
   │ Loading     │        │   Design     │        │   Experience│
   │ (Next.js)   │        │ (Tailwind)   │        │ (Animations)│
   └─────────────┘        └─────────────┘        └─────────────┘
```

## 📅 Automation Schedule

- **Daily Tools Discovery**: 7:00 AM IST
- **News Aggregation**: 7:15 AM IST  
- **Website Updates**: 7:30 AM IST
- **All processes run automatically via GitHub Actions**

## 🧠 Dynamic Keyword Learning

The system features an intelligent keyword learning system that:

- **Tracks Success**: Monitors which keywords lead to successful discoveries
- **Extracts New Keywords**: Automatically learns new relevant terms
- **Adapts Over Time**: Evolves keyword database based on performance
- **JSON Configuration**: Flexible keyword management via `data/config/keywords.json`

## 🎯 Content Quality

- **Smart Filtering**: Excludes Reddit posts, news articles, and non-tool content
- **Deduplication**: Prevents duplicate tools across outputs
- **Categorization**: Tools organized by category (Chatbots, Image Generation, etc.)
- **Quality Scoring**: Trending score algorithm for relevance

## 🚀 Quick Start

### For Users
1. Visit the live website to browse daily AI tools and news
2. Bookmark for daily updates
3. Share interesting discoveries with the community

### For Developers
1. Install the Python package: `pip install -e .`
2. Set up the website: `cd website && npm install`
3. Run daily tools: `daily-tools`
4. Start development: `cd website && npm run dev`

### For Contributors
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with: `test-keywords`
5. Submit a pull request

## 📊 Current Status

- **Version**: 3.1.0
- **Python**: 3.11+
- **Node.js**: 18+
- **Next.js**: 15.3.4
- **React**: 19.0.0
- **TypeScript**: Full support
- **Tailwind CSS**: v4

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to:

- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation
- Add new AI tools to the discovery

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Live Website**: [Your website URL]
- **GitHub Repository**: [Your repo URL]
- **Issues**: [GitHub Issues]
- **Discussions**: [GitHub Discussions]

---

**Made with ❤️ by the AI Insights Daily team**

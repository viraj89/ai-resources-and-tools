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
- Finds trending AI tools automatically
- Learns and improves over time
- Filters out irrelevant content
- Sources: Reddit, GitHub, news sites

### 📊 Daily Content
- **Daily Digest**: 3-5 top AI tools
- **Tools Directory**: Complete catalog
- **News Updates**: Latest AI news
- **Website**: Beautiful presentation

## 🔄 How It Works

```
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│    Sources    │          │    Process    │          │     Output    │
├───────────────┤          ├───────────────┤          ├───────────────┤
│   • Reddit    │          │  • Discover   │          │   • Website   │
│   • GitHub    │  ──────► │  • Filter     │  ──────► │   • Daily MD  │
│   • News      │          │  • Learn      │          │   • Directory │
└───────────────┘          └───────────────┘          └───────────────┘
```

**Daily Schedule**: Runs automatically at 7:00 AM IST via GitHub Actions

## 🛠️ Quick Commands

```bash
# Install
pip install -e .

# Generate daily tools
daily-tools

# Update news
update-news

# Manage keywords
keyword-manager

# Test system
test-keywords
```

## 📁 Project Structure

```
auto-news/
├── artifacts/          # Generated content
├── data/              # Config & cache
├── src/               # Python scripts
├── website/           # Next.js app
└── docs/              # Documentation
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

## 📊 Current Status

- **Version**: 3.1.0
- **Python**: 3.11+
- **Next.js**: 15.3.4
- **React**: 19.0.0

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

## Architecture Overview

This project uses a hybrid architecture that leverages the strengths of both Python for data processing and Next.js for a modern user interface. The two systems are decoupled, communicating via statically generated data files.

### Backend (Python)

- **Purpose**: To automate the discovery, processing, and scoring of AI-related content from various sources like news feeds, GitHub, and research paper repositories.
- **Technology**: The core logic is built with Python scripts located in the `src/scripts` directory.
- **Data Flow**: The scripts run on a schedule, fetch new content, and then generate static data files (primarily `website/src/data/content.ts`) that the frontend consumes.

### Frontend (Next.js)

- **Purpose**: To provide a fast, responsive, and interactive user interface for browsing the aggregated content.
- **Technology**: The frontend is a modern web application built with Next.js (a React framework), located in the `website/` directory.
- **Data Flow**: The web application is completely decoupled from the Python backend. It simply reads the data from the `website/src/data/content.ts` file to render the UI.

## Key Features

- **Automated News Discovery**: Scans and ranks the latest news and articles.
- **AI Tool Discovery**: Finds trending new AI tools and applications.
- **Research Paper Aggregation**: Gathers the latest research papers from sources like arXiv.
- **Advanced Scoring**: Uses freshness and relevance metrics to surface the best content.
- **Modern UI**: A clean, responsive, and user-friendly interface.

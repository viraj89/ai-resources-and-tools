# AI Insights Daily

## Project Overview
AI Insights Daily is an automated platform that discovers, curates, and presents trending AI tools, news, and research breakthroughs. It combines a Python-based backend for intelligent data aggregation with a modern Next.js frontend for beautiful, responsive presentation.

## Key Features
- Automated daily discovery of AI tools, news, and research
- Multi-source integration: Product Hunt, Hacker News, arXiv, GitHub, News APIs
- Quality ranking, freshness scoring, and advanced filtering
- Modern, mobile-friendly website (Next.js + Tailwind CSS)
- Clean, professional HTML preview for rapid prototyping

## Architecture Overview
AI Insights Daily is built with a modular, scalable architecture:

- **Backend (Python):**
  - `src/scripts/`: Main discovery and data processing scripts
  - `src/utils/`: Utilities for parsing, scoring, and keyword management
  - Automated jobs for daily discovery, filtering, and enrichment
- **Frontend (Next.js + React):**
  - `website/`: Modern, responsive web interface
  - Presents daily digests, tools directory, and research archive
- **Artifacts:**
  - Markdown and CSV outputs for daily digests, tools directory, and research
  - HTML preview (`docs/v4_showcase.html`) for rapid UI prototyping

**System Flow:**
```
[Data Sources] → [Python Discovery & Filtering] → [Markdown/CSV/JSON Artifacts] → [Next.js Website & HTML Preview]
```

## Quick Start
### Backend (Python)
```bash
pip install -e .
```
### Frontend (Website)
```bash
cd website
npm install
npm run dev
```

## Usage
- Run backend scripts to generate daily digests and update content
- Launch the website for a live, interactive experience
- Use the HTML preview for quick design iteration

## Contribution
Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Changelog & Release Notes
See [CHANGELOG.md](CHANGELOG.md) and [RELEASE_NOTES.md](RELEASE_NOTES.md) for a full history of updates.

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

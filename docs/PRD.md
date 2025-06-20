# Product Requirements Document (PRD)

## 1. Overview

**Project Name:** Auto-News Daily AI News Aggregator

**Description:**
Auto-News is an automated system that fetches, deduplicates, and publishes daily AI news and blog posts from various sources, updating a markdown file (`blogs-and-news.md`) in a GitHub repository. The system leverages Python scripts, RSS feeds, and GitHub Actions for workflow automation.

---

## 2. Goals & Objectives

- Provide a daily, curated list of the most relevant and recent AI news and blog posts.
- Eliminate manual effort in news aggregation and publishing.
- Ensure news freshness, variety, and minimal duplication across days.
- Enable transparency and traceability of news updates via version control.
- **New Goal**: Present the aggregated content on a beautiful, modern, and responsive public-facing website.
- **New Goal**: Increase user engagement by providing a web interface instead of just markdown files.

---

## 3. Features

- **Automated News Fetching:**
  - Fetches news from Google News RSS feeds and keyword-based feeds.
- **Deduplication:**
  - Deduplicates news within the same day and across recent days (7-day window).
- **Prioritization:**
  - Ranks news based on severity and relevance using keyword matching.
- **Markdown Publishing:**
  - Formats and updates `blogs-and-news.md` with daily news, sources, and historical log.
- **URL Shortening:**
  - Uses TinyURL API to shorten news links for readability.
- **Workflow Automation:**
  - Uses GitHub Actions to run the update script daily and on-demand.
- **Change Tracking:**
  - Commits and pushes updates to the repository with clear commit messages.

### 3.1 Website Features (New)

- **Single-Page Application (SPA)**: A modern, responsive website built with Next.js and Tailwind CSS.
- **Dynamic Content**: Displays daily AI tools and news updates chronologically.
- **Preserves History**: All previous updates remain accessible on the single page, similar to a blog feed.
- **Automatic Deployment**: Deploys automatically to Vercel daily at 7:30 AM IST (2:00 UTC).
- **Unique Visitor Counter**: A footer counter to track page visits, powered by Vercel KV and Serverless Functions.
- **Free Hosting**: Entirely hosted and deployed using Vercel's free tier.

---

## 4. User Stories

- **As a reader**, I want to see a daily list of the most important AI news, so I can stay updated efficiently.
- **As a maintainer**, I want the news aggregation to be automated, so I don't have to manually update the file.
- **As a contributor**, I want to ensure duplicate news does not appear on consecutive days, so the content remains fresh.
- **As a stakeholder**, I want to track changes and updates to the news file, so I have a historical record.

---

## 5. Technical Architecture

- **Languages & Tools:** Python 3.11+, GitHub Actions, Markdown, RSS, JSON
- **Key Components:**
  - `tools/script/update_blogs_and_news.py`: Main script for fetching, deduplication, formatting, and updating news.
  - `blogs-and-news.md`: Markdown file containing the news log.
  - `tools/resources/news_cache.json`: JSON cache for recent news URLs.
  - `.github/workflows/daily-news.yml` & `.github/workflows/daily-news-update.yml`: GitHub Actions workflows for automation.
- **Data Flow:**
  1. GitHub Action triggers (scheduled or manual).
  2. Script fetches news from RSS feeds.
  3. Deduplication against recent cache.
  4. News prioritized and formatted.
  5. Markdown file updated and committed.
  6. Cache updated.

### 5.1 Website Architecture (New)

- **Framework**: Next.js with TypeScript.
- **Styling**: Tailwind CSS for responsive and modern design.
- **Data Source**: A `content.json` file generated daily by a Python script (`src/scripts/prepare_website_data.py`), which parses the project's markdown files and CSV.
- **Visitor Counter**:
    - **Backend**: A Vercel Serverless Function (`/api/views`).
    - **Database**: Vercel KV for storing the visitor count.
- **Deployment**:
    - **Platform**: Vercel (Free Tier).
    - **Trigger**: Automatic deployments triggered by commits to the `main` branch via the Vercel for GitHub integration.

---

## 6. Data Sources

- **Primary:** Google News RSS feeds (general AI and keyword-based)
- **Keywords:** OpenAI, Anthropic, Google AI, Microsoft AI, Meta AI, DeepMind, Stability AI, Midjourney, Cohere, ChatGPT, Claude, GPT-4, DALL-E, Stable Diffusion, Gemini, Llama, Mistral, Falcon, and more.
- **URL Shortening:** TinyURL API

---

## 7. Workflow Automation

- **GitHub Actions:**
  - Scheduled daily at 7 AM IST (1:30 UTC)
  - Manual dispatch supported
  - Steps:
    1. Checkout code
    2. Set up Python
    3. Install dependencies
    4. Run update script
    5. Commit and push changes if any

---

## 8. Error Handling & Edge Cases

- **Network Failures:**
  - Graceful fallback if RSS or TinyURL API fails
- **Encoding Issues:**
  - Handles UnicodeDecodeError when reading/writing files
- **Cache Corruption:**
  - Handles JSON load errors and resets cache if needed
- **Duplicate News:**
  - Deduplication logic prevents repeats within a 7-day window
- **File Not Found:**
  - Initializes markdown file if missing

---

## 9. Future Enhancements

- Add support for more news/blog sources (e.g., Hacker News, Reddit, Medium)
- Implement fuzzy deduplication based on title similarity
- Add web UI for browsing and searching news history
- Enable user-configurable keywords and sources
- Add notification (email/Slack) for daily updates
- Analytics dashboard for news trends

---

## 10. Success Metrics

- Daily news file is updated without manual intervention
- No duplicate news within a 7-day window
- News is relevant and timely (within 24 hours of publication)
- System uptime and workflow success rate > 99%
- **New Metric**: The Vercel website is successfully updated daily.
- **New Metric**: Positive user feedback on the website's design and usability.
- **New Metric**: Growth in unique visitor counts.

---

## 11. Stakeholders

- Project Owner / Maintainer
- Contributors / Developers
- End Users / Readers
- Community Stakeholders

---

## 12. Appendix

- **Repository Structure:**
  - `/blogs-and-news.md`: Main news log
  - `/tools/script/update_blogs_and_news.py`: News update script
  - `/tools/resources/news_cache.json`: Recent news cache
  - `/requirements.txt`: Python dependencies
  - `/.github/workflows/`: Automation workflows
- **References:**
  - [Google News RSS](https://news.google.com/)
  - [TinyURL API](https://tinyurl.com/)
- **Contact:**
  - [GitHub Issues](https://github.com/viraj89/ai-resources-and-tools/issues) 
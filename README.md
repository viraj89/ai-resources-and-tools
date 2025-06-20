# Auto-News AI

**Version 3.0.0** | Your daily digest of trending AI tools and news, now on a modern web platform.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fviraj89%2Fai-resources-and-tools&root-directory=website&project-name=auto-news-ai&repository-name=auto-news-ai)

---

This project automatically discovers, aggregates, and displays the latest in AI tools and news. Originally a set of data scripts, it has evolved into a full-fledged application with a public-facing website built on Next.js and deployed with Vercel.

## 🚀 The Website

The primary interface for this project is now a live, single-page website that is updated automatically every day.

- **Live Updates**: New content is fetched and deployed daily at **7:30 AM IST (2:00 UTC)**.
- **Responsive Design**: Fully accessible on desktop and mobile devices.
- **Historical Content**: Scroll through a chronological feed of all past news and tool discoveries.

## 📁 Project Structure

To address the "noise", the project is now conceptually simpler. The Python backend's sole purpose is to feed data to the Next.js frontend.

```
/
├── website/              # The Next.js frontend application
│   └── src/data/
│       └── content.json  # (Auto-generated) The single source of truth for the website
│
├── src/                  # The Python backend scripts
│   ├── scripts/          # All data-fetching and processing scripts
│   └── utils/            # Shared utilities like the keyword learner
│
├── data/                 # Raw data and configuration for the backend
│   ├── config/
│   │   └── keywords.json # Dynamic keywords for the discovery engine
│   └── master_resources.csv # (Auto-generated) The master tool list
│
├── .github/workflows/    # GitHub Actions for automation
│   └── daily-update.yml  # A single, consolidated workflow
│
├── ai-tools-daily.md     # (Artifact) Raw markdown output for daily tools
├── blogs-and-news.md     # (Artifact) Raw markdown output for news
└── ai-tools-directory.md # (Artifact) Raw markdown of the complete tool directory
```

**Key Takeaway**: The Python scripts in `src/` run daily to produce the raw `.md` and `.csv` files. Then, `prepare_website_data.py` creates `website/src/data/content.json`, which the Next.js app in `website/` uses to build the web page.

## 🛠️ For Developers

While the main product is the website, the underlying Python scripts and data are still accessible.

### Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/viraj89/ai-resources-and-tools.git
    cd ai-resources-and-tools
    ```
2.  **Install Python dependencies**:
    ```bash
    pip install -e .
    ```
3.  **Run scripts manually**:
    You can use the command-line tools defined in `setup.py`:
    ```bash
    # Run the full daily pipeline
    daily-tools
    news-aggregator
    tools-directory
    prepare-website-data

    # Manage keywords
    keyword-manager stats
    ```

### Deploying Your Own Version

You can deploy your own instance of this project with a single click using the Vercel Deploy Button at the top of this README.

## 🔄 Automation Flow

The entire project is automated by a single GitHub Actions workflow defined in `.github/workflows/daily-update.yml`:

1.  **Scheduled Trigger**: The workflow runs automatically every day at 7:30 AM IST (2:00 UTC).
2.  **Run Python Scripts**: It executes all the necessary Python scripts in order to fetch the latest data and generate the `content.json` for the website.
3.  **Commit Changes**: It commits all the changed files (markdown, CSV, and the final JSON) back to the repository.
4.  **Trigger Vercel Deployment**: This commit automatically triggers a new deployment on Vercel, ensuring the website is always up-to-date.

## 📝 Changelog

Detailed changes for each version are documented in the `RELEASE_NOTES.md` and `docs/CHANGELOG.md`.

## 📄 License

This project is licensed under the MIT License.

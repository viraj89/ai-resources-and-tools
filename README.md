# Auto News Aggregator

An automated tool that aggregates and updates AI-related news and blog posts daily. The tool fetches news from various sources, prioritizes important updates, and maintains a clean, organized markdown file with the latest AI news.

## Features

- 🔄 **Automated Updates**: Runs daily at 7 AM IST via GitHub Actions
- 📰 **Comprehensive Coverage**: Aggregates news from multiple sources including:
  - Google News RSS feeds
  - Major AI companies and startups
  - Industry developments and breakthroughs
- 🎯 **Smart Filtering**: Uses an extensive keyword list to ensure relevant content
- ⚡ **Priority Sorting**: Highlights important news based on severity keywords
- 🔗 **Clean Formatting**: Maintains a well-organized markdown file with:
  - Daily news sections
  - Numbered entries
  - Shortened URLs for better readability
  - Clear source citations
- 📒 **Master Resources List**: Maintains a comprehensive, curated CSV file of AI tools, apps, and resources, including their categories, descriptions, and pricing.

## Project Structure

```
.
├── tools/
│   ├── blogs-and-news.md    # Main output file with aggregated news (updated daily)
│   ├── resources/
│   │   └── master_resources.csv  # Comprehensive list of AI tools, apps, and resources
│   └── script/
│       └── update_blogs_and_news.py  # Main script for news aggregation
└── .github/
    └── workflows/
        └── daily_update.yml  # GitHub Actions workflow for automation
```

## How It Works

1. The script runs daily at 7 AM IST
2. Fetches news from Google News RSS feeds using multiple AI-related keywords
3. Processes and deduplicates the news items
4. Prioritizes important updates using severity keywords
5. Formats the content with proper markdown structure
6. Updates the `blogs-and-news.md` file with the latest news
7. Maintains a growing, curated `master_resources.csv` file with AI tools and resources

## Master Resources CSV

The `tools/resources/master_resources.csv` file is a comprehensive, manually curated list of AI tools, apps, and resources. It contains the following columns:

| Sr. No. | Tool Name | Category | URL | What it does | Free/Paid |
|---------|-----------|----------|-----|--------------|-----------|

You can add new resources to this file to help the community discover and track the evolving AI ecosystem.

## Setup

1. Clone the repository
2. Install required Python packages:
   ```bash
   pip install requests
   ```
3. Run the script manually (optional):
   ```bash
   python tools/script/update_blogs_and_news.py
   ```

## Automation

The project uses GitHub Actions to automatically run the script daily at 7 AM IST. The workflow is configured in `.github/workflows/daily_update.yml`.

## Output Format

The script generates a markdown file with the following structure:
- Daily sections with timestamps
- Numbered news items
- Shortened URLs for better readability
- Clear source citations
- Horizontal rules between days for better organization

The resources CSV is a separate, growing file for AI tools and resources.

## Contributing

Feel free to:
- Add more keywords for better news coverage
- Improve the severity scoring system
- Add more news sources
- Enhance the formatting
- Add new AI tools, apps, and resources to the master CSV file

## License

MIT License

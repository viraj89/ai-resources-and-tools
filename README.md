# AI Insights Daily

An automated system to discover and display trending AI tools and news on a public-facing website. This project combines Python for data aggregation and a Next.js frontend for presentation.

## 🚀 The Website

The primary output of this project is a live, single-page website that is updated automatically every day with the latest content.

- **Live Updates**: New content is fetched and deployed daily.
- **Responsive Design**: Accessible on desktop and mobile devices.
- **Clean UI**: A clean, modern interface for browsing daily updates.

## 📁 Project Structure

The project is organized into a clean and maintainable structure.

```
/
├── artifacts/            # (Auto-generated) All raw data files (MD, CSV).
├── data/                 # Configuration and cache for the backend.
├── src/                  # The Python backend scripts.
│   ├── scripts/
│   └── utils/
└── website/              # The Next.js frontend application.
```

## 🛠️ How It Works

1.  **Data Fetching**: Python scripts in `src/scripts/` run on a daily schedule via GitHub Actions. They scan sources like Reddit and GitHub to discover new AI tools and news.
2.  **Artifact Generation**: The scripts generate raw data files (e.g., `ai-tools-daily.md`, `blogs-and-news.md`) and save them in the `artifacts/` directory.
3.  **Website Build**: The `prepare_website_data.py` script processes these artifacts into a single `content.ts` file. The Next.js website in the `website/` directory uses this file to build the final static site.
4.  **Deployment**: Committing the updated `content.ts` file to GitHub automatically triggers a new deployment on Vercel, ensuring the live website is always up-to-date.

## 📄 License

This project is licensed under the MIT License.

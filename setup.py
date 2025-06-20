#!/usr/bin/env python3
"""
Setup script for Auto News AI Tools Discovery
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-news-ai-tools",
    version="3.0.0",
    author="Auto-News AI",
    description="An automated system to discover and display trending AI tools and news on a public-facing website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.6.3",
        "feedparser>=6.0.8",
        "pandas>=1.3.0",
        "openpyxl>=3.0.7",
        "markdown>=3.3.4",
        "pyyaml>=5.4.1",
        "schedule>=1.1.0",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "daily-tools=src.scripts.daily_tools_digest:main",
            "news-aggregator=src.scripts.news_aggregator:main",
            "tools-directory=src.scripts.generate_tools_directory:main",
            "keyword-manager=src.scripts.manage_keywords:main",
            "test-keywords=src.scripts.test_keyword_learning:main",
            "prepare-website-data=src.scripts.prepare_website_data:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
    zip_safe=False,
) 
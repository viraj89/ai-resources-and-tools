#!/usr/bin/env python3
"""
Setup script for AI Resources and Tools
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Read version
def read_version():
    with open("VERSION", "r", encoding="utf-8") as fh:
        return fh.read().strip()

setup(
    name="auto-news",
    version=read_version(),
    author="Auto-News Team",
    description="An automated system that discovers, aggregates, and maintains a comprehensive collection of trending AI tools, apps, and news",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auto-news",
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
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "auto-news-daily=src.scripts.daily_tools_digest:main",
            "auto-news-update=src.scripts.update_blogs_and_news:main",
            "auto-news-discover=src.scripts.auto_discover_ai_tools:main",
            "auto-news-directory=src.scripts.generate_tools_directory:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 
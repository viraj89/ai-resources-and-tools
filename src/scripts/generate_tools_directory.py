#!/usr/bin/env python3
"""
Generate AI Tools Directory
- Cleans the master_resources.csv to only include actual AI tools/apps
- Converts to a readable markdown table format
- Filters out Reddit posts, news articles, and non-tool content
- Creates a clean, categorized tools directory
"""

import csv
import re
import os
from datetime import datetime

# File paths
ARTIFACTS_DIR = "artifacts"
CSV_PATH = "data/master_resources.csv"
OUTPUT_PATH = os.path.join(ARTIFACTS_DIR, "ai-tools-directory.md")

# Keywords that indicate actual tools/apps (not posts or articles)
TOOL_INDICATORS = [
    "ai", "gpt", "claude", "assistant", "tool", "platform", "app", "bot", "agent",
    "generator", "creator", "studio", "hub", "workspace", "lab", "kit", "suite",
    "api", "sdk", "framework", "library", "engine", "model", "service", "solution"
]

# Keywords that indicate non-tools (posts, articles, etc.)
NON_TOOL_INDICATORS = [
    "reddit", "redd.it", "twitter", "tweet", "post", "article", "news", "report",
    "discussion", "question", "how to", "tutorial", "guide", "analysis", "review",
    "announcement", "update", "release", "launch", "introducing", "new feature",
    "github.com", "arxiv.org", "research", "paper", "study", "analysis"
]

# Categories to keep (exclude "Other" category)
VALID_CATEGORIES = [
    "Text / Chat Assistants",
    "Code / Developer Tools", 
    "Design / Image Generation",
    "Video / Creative Tools",
    "Voice / Audio Tools",
    "Presentations",
    "Search / Research",
    "Business / Analytics",
    "Education / Learning",
    "Productivity / Writing"
]

def is_actual_tool(tool_name, description, url):
    """Check if this is an actual AI tool/app, not a post or article"""
    
    # Skip if no URL or invalid URL
    if not url or url == "N/A" or not url.startswith('http'):
        return False
    
    # Skip if it's clearly a Reddit post or social media
    if any(indicator in url.lower() for indicator in ["reddit.com", "redd.it", "twitter.com", "youtu.be"]):
        return False
    
    # Skip if it's a news article or research paper
    if any(indicator in url.lower() for indicator in ["arxiv.org", "news", "article", "blog"]):
        return False
    
    # Skip if name contains non-tool indicators
    name_lower = tool_name.lower()
    if any(indicator in name_lower for indicator in NON_TOOL_INDICATORS):
        return False
    
    # Skip if it's a GitHub repository without clear tool indicators
    if "github.com" in url.lower():
        # Only include GitHub repos that are clearly AI tools
        if not any(indicator in name_lower for indicator in TOOL_INDICATORS):
            return False
    
    # Skip if description is too short or contains non-tool content
    if not description or len(description) < 10:
        return False
    
    # Skip if description contains non-tool indicators
    desc_lower = description.lower()
    if any(indicator in desc_lower for indicator in NON_TOOL_INDICATORS):
        return False
    
    return True

def clean_description(description):
    """Clean and format the description"""
    if not description:
        return ""
    
    # Remove markdown formatting
    description = re.sub(r'\*\*.*?\*\*', '', description)  # Remove bold
    description = re.sub(r'\*.*?\*', '', description)      # Remove italic
    description = re.sub(r'\[.*?\]\(.*?\)', '', description)  # Remove links
    description = re.sub(r'`.*?`', '', description)        # Remove code blocks
    
    # Clean up whitespace
    description = re.sub(r'\s+', ' ', description)
    description = description.strip()
    
    # Limit length
    if len(description) > 150:
        description = description[:147] + "..."
    
    return description

def generate_markdown_table(tools_by_category):
    """Generate a markdown table for each category"""
    
    markdown_content = f"""# 🤖 AI Tools Directory

*Last updated: {datetime.now().strftime('%B %d, %Y')}*

This directory contains a curated collection of trending AI tools and applications, automatically discovered and categorized.

## 📊 Summary
"""
    
    # Add summary
    total_tools = sum(len(tools) for tools in tools_by_category.values())
    markdown_content += f"- **Total Tools**: {total_tools}\n"
    markdown_content += f"- **Categories**: {len(tools_by_category)}\n"
    markdown_content += f"- **Last Updated**: {datetime.now().strftime('%B %d, %Y')}\n\n"
    
    # Generate table for each category
    for category, tools in tools_by_category.items():
        if not tools:
            continue
            
        markdown_content += f"## {category}\n\n"
        markdown_content += "| Tool | Description | Pricing | URL |\n"
        markdown_content += "|------|-------------|---------|-----|\n"
        
        for tool in tools:
            name = tool['Tool Name']
            description = clean_description(tool['What it does'])
            pricing = tool['Free/Paid']
            url = tool['URL']
            
            # Format pricing with emoji
            pricing_emoji = "🆓" if pricing == "Freemium" else "💰" if pricing == "Paid" else "❓"
            pricing_display = f"{pricing_emoji} {pricing}"
            
            markdown_content += f"| **{name}** | {description} | {pricing_display} | [Visit]({url}) |\n"
        
        markdown_content += "\n---\n\n"
    
    # Add footer
    markdown_content += """
## 📋 About This Directory

This directory is automatically generated from our master database of AI tools. Tools are discovered from multiple sources including:
- GitHub trending repositories
- Reddit AI communities  
- News articles and announcements
- Product discovery platforms

### 🔄 Updates
This directory is updated daily via automated scripts. New tools are automatically discovered and added to the master database.

### 📊 Data Source
The complete, deduplicated database is available in [master_resources.csv](data/master_resources.csv).

---
*Generated by [Auto-News](https://github.com/yourusername/auto-news) - Automated AI Tools Discovery*
"""
    
    return markdown_content

def main():
    """Main function to generate the tools directory"""
    print("🔍 Generating AI Tools Directory...")
    
    # Ensure artifacts directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Read and clean CSV data
    tools_by_category = {category: [] for category in VALID_CATEGORIES}
    
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                tool_name = row['Tool Name'].strip()
                category = row['Category'].strip()
                url = row['URL'].strip()
                description = row['What it does'].strip()
                pricing = row['Free/Paid'].strip()
                
                # Skip if not a valid category
                if category not in VALID_CATEGORIES:
                    continue
                
                # Check if this is an actual tool
                if is_actual_tool(tool_name, description, url):
                    tool_data = {
                        'Tool Name': tool_name,
                        'Category': category,
                        'URL': url,
                        'What it does': description,
                        'Free/Paid': pricing
                    }
                    tools_by_category[category].append(tool_data)
    
    except FileNotFoundError:
        print(f"❌ CSV file not found: {CSV_PATH}")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Generate markdown content
    markdown_content = generate_markdown_table(tools_by_category)
    
    # Write to file
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Print summary
        total_tools = sum(len(tools) for tools in tools_by_category.values())
        print(f"✅ Generated AI Tools Directory with {total_tools} tools")
        
        for category, tools in tools_by_category.items():
            if tools:
                print(f"   📁 {category}: {len(tools)} tools")
        
        print(f"📄 Output saved to: {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")

if __name__ == "__main__":
    main() 
## Problem
The daily news update script is not properly deduplicating news articles across consecutive days. This results in the same news articles appearing on multiple days (e.g., June 19 and June 20 had duplicate news items).

## Current Behavior
- Script fetches news from RSS feeds daily
- Only deduplicates within the same day's fetch
- Does not check against previous days' news
- Same articles can appear on consecutive days

## Expected Behavior
- Script should check against recent previous days (e.g., last 3-7 days)
- Prevent duplicate news articles from appearing across consecutive days
- Maintain news freshness and variety

## Proposed Solution
1. Store a cache of recent news URLs (last 7 days)
2. Check new articles against this cache before adding
3. Update cache after each run
4. Optionally, implement a more sophisticated deduplication based on title similarity

## Files to Modify
- `tools/script/update_blogs_and_news.py`

## Priority
Medium - affects user experience and content quality 
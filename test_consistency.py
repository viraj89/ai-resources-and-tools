#!/usr/bin/env python3
"""
Test script to verify consistency between June 20 and June 21 data
"""

import json
import sys
import os

def test_consistency():
    """Test that both dates have consistent structure"""
    
    # Read the content file
    content_path = "website/src/data/content.ts"
    
    if not os.path.exists(content_path):
        print("❌ Content file not found")
        return False
    
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the JSON part (remove TypeScript export syntax)
        json_start = content.find('export const content = ') + len('export const content = ')
        json_end = content.rfind(';')
        json_content = content[json_start:json_end].strip()
        
        # Parse JSON
        data = json.loads(json_content)
        
        # Group updates by date
        updates_by_date = {}
        for update in data['daily_updates']:
            date = update['date'][:10]  # Extract YYYY-MM-DD
            if date not in updates_by_date:
                updates_by_date[date] = {'tools': [], 'news': []}
            
            if update['type'] == 'tools':
                updates_by_date[date]['tools'].extend(update['data'])
            elif update['type'] == 'news':
                updates_by_date[date]['news'].extend(update['data'])
        
        # Test consistency
        print("🔍 Testing data consistency...")
        print(f"📅 Dates found: {list(updates_by_date.keys())}")
        
        for date, content in updates_by_date.items():
            tools_count = len(content['tools'])
            news_count = len(content['news'])
            
            print(f"\n📅 {date}:")
            print(f"   🛠️  Tools: {tools_count}")
            print(f"   📰 News: {news_count}")
            
            # Check if both sections exist
            if tools_count > 0 and news_count > 0:
                print(f"   ✅ Both tools and news present")
            elif tools_count > 0:
                print(f"   ⚠️  Only tools present")
            elif news_count > 0:
                print(f"   ⚠️  Only news present")
            else:
                print(f"   ❌ No content")
        
        # Verify both dates have tools
        june_20 = updates_by_date.get('2025-06-20', {})
        june_21 = updates_by_date.get('2025-06-21', {})
        
        if len(june_20.get('tools', [])) > 0 and len(june_21.get('tools', [])) > 0:
            print(f"\n✅ SUCCESS: Both June 20 and June 21 have tools sections!")
            return True
        else:
            print(f"\n❌ FAILURE: Missing tools sections")
            return False
            
    except Exception as e:
        print(f"❌ Error testing consistency: {e}")
        return False

if __name__ == "__main__":
    success = test_consistency()
    sys.exit(0 if success else 1) 
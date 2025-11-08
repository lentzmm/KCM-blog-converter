#!/usr/bin/env python3
"""
Create Notion Conversion Tracking Database
One-time script to set up the database structure
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client as NotionClient

# Load environment variables
env_path = Path(__file__).parent / 'shared' / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Notion client
notion_api_key = os.getenv('NOTION_API_KEY')
if not notion_api_key:
    print("❌ ERROR: NOTION_API_KEY not found in shared/.env")
    print("Please make sure your Notion API key is set.")
    exit(1)

notion_client = NotionClient(auth=notion_api_key)

print("=" * 60)
print("Creating Notion Conversion Tracking Database...")
print("=" * 60)
print()

# First, let's search for an existing page to use as parent
# We'll look for the main context database or any page
print("Step 1: Finding a parent page in your Notion workspace...")

try:
    # Get the user's Notion pages
    search_results = notion_client.search(
        filter={
            "property": "object",
            "value": "page"
        }
    )

    pages = search_results.get('results', [])

    if not pages:
        print("❌ No pages found in your Notion workspace.")
        print("\nPlease do ONE of these:")
        print("1. Create any page in Notion first (can be blank)")
        print("2. Or share an existing page with your Notion integration")
        print("\nThen run this script again.")
        exit(1)

    # Use the first page as parent
    parent_page_id = pages[0]['id']
    parent_page_title = pages[0].get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'Untitled')

    print(f"✅ Found parent page: '{parent_page_title}'")
    print(f"   Database will be created as a child of this page")
    print()

except Exception as e:
    print(f"❌ Error searching for pages: {e}")
    print("\nMake sure:")
    print("1. Your NOTION_API_KEY is correct in shared/.env")
    print("2. Your integration has access to at least one page")
    exit(1)

# Create the database
print("Step 2: Creating database with all properties...")

try:
    new_database = notion_client.databases.create(
        parent={
            "type": "page_id",
            "page_id": parent_page_id
        },
        title=[
            {
                "type": "text",
                "text": {
                    "content": "Blog Post Conversions"
                }
            }
        ],
        properties={
            "Article Title": {
                "title": {}
            },
            "KCM URL": {
                "url": {}
            },
            "KCM Slug": {
                "rich_text": {}
            },
            "WordPress URL": {
                "url": {}
            },
            "WordPress Slug": {
                "rich_text": {}
            },
            "WordPress Post ID": {
                "number": {
                    "format": "number"
                }
            },
            "Focus Keyphrase": {
                "rich_text": {}
            },
            "Converted Date": {
                "date": {}
            },
            "Categories": {
                "multi_select": {
                    "options": []
                }
            },
            "Tags": {
                "multi_select": {
                    "options": []
                }
            },
            "SEO Title": {
                "rich_text": {}
            },
            "Meta Description": {
                "rich_text": {}
            },
            "Internal Links Count": {
                "number": {
                    "format": "number"
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {
                            "name": "Published",
                            "color": "green"
                        },
                        {
                            "name": "Draft",
                            "color": "yellow"
                        },
                        {
                            "name": "Failed",
                            "color": "red"
                        }
                    ]
                }
            }
        }
    )

    database_id = new_database['id']
    database_url = new_database['url']

    print("✅ Database created successfully!")
    print()
    print("=" * 60)
    print("DATABASE DETAILS")
    print("=" * 60)
    print(f"Database Name: Blog Post Conversions")
    print(f"Database URL:  {database_url}")
    print(f"Database ID:   {database_id}")
    print()
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("1. Open your shared/.env file")
    print()
    print("2. Add this line (or update if it exists):")
    print()
    print(f"   NOTION_CONVERSION_DB_ID={database_id}")
    print()
    print("3. Save the .env file")
    print()
    print("4. Restart your server:")
    print("   - Stop the server (Ctrl+C)")
    print("   - Run start-kcm-converter-CLEAN.bat")
    print()
    print("5. Test it:")
    print("   - Convert a blog post")
    print("   - Upload to WordPress")
    print("   - Check your Notion database for the new entry!")
    print()
    print("=" * 60)
    print()
    print(f"View your database here: {database_url}")
    print()

except Exception as e:
    print(f"❌ Error creating database: {e}")
    print("\nPlease check:")
    print("1. Your Notion integration has 'Insert content' permission")
    print("2. The integration is connected to your workspace")
    import traceback
    print("\nFull error:")
    print(traceback.format_exc())
    exit(1)

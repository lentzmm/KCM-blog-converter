"""
Notion Conversion Tracker
Tracks KCM to WordPress post conversions in a Notion database
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def get_url_mappings(notion_client) -> Dict[str, str]:
    """
    Query Notion conversion database and return KCM URL -> WordPress URL mapping

    Args:
        notion_client: Authenticated Notion client

    Returns:
        Dictionary mapping KCM URLs to WordPress URLs
    """
    conversion_db_id = os.getenv('NOTION_CONVERSION_DB_ID')

    if not conversion_db_id:
        logger.warning("NOTION_CONVERSION_DB_ID not set - link replacement disabled")
        return {}

    try:
        # Query all pages in conversion database
        response = notion_client.databases.query(
            database_id=conversion_db_id,
            filter={
                "and": [
                    {
                        "property": "Status",
                        "select": {
                            "equals": "Published"
                        }
                    }
                ]
            }
        )

        url_mapping = {}

        for page in response.get('results', []):
            props = page.get('properties', {})

            # Extract KCM URL
            kcm_url_prop = props.get('KCM URL', {})
            kcm_url = kcm_url_prop.get('url')

            # Extract WordPress URL
            wp_url_prop = props.get('WordPress URL', {})
            wp_url = wp_url_prop.get('url')

            if kcm_url and wp_url:
                url_mapping[kcm_url] = wp_url
                logger.info(f"Mapped: {kcm_url} -> {wp_url}")

        logger.info(f"Loaded {len(url_mapping)} URL mappings from Notion")
        return url_mapping

    except Exception as e:
        logger.error(f"Failed to load URL mappings from Notion: {e}")
        return {}


def add_conversion_record(
    notion_client,
    kcm_url: str,
    kcm_slug: str,
    wordpress_url: str,
    wordpress_slug: str,
    wordpress_post_id: int,
    article_title: str,
    focus_keyphrase: str,
    categories: List[str],
    tags: List[str],
    seo_title: str,
    meta_description: str,
    internal_links_count: int = 0,
    status: str = "Published"
) -> Optional[str]:
    """
    Add a new conversion record to the Notion database

    Args:
        notion_client: Authenticated Notion client
        kcm_url: Original KCM article URL
        kcm_slug: Original KCM slug
        wordpress_url: New WordPress URL
        wordpress_slug: New WordPress slug
        wordpress_post_id: WordPress post ID
        article_title: Article title
        focus_keyphrase: SEO focus keyphrase
        categories: List of category names
        tags: List of tag names
        seo_title: SEO title
        meta_description: Meta description
        internal_links_count: Number of internal links found
        status: Conversion status (Published, Draft, Failed)

    Returns:
        Notion page ID if successful, None otherwise
    """
    conversion_db_id = os.getenv('NOTION_CONVERSION_DB_ID')

    if not conversion_db_id:
        logger.warning("NOTION_CONVERSION_DB_ID not set - skipping conversion tracking")
        return None

    try:
        # Create new page in conversion database
        new_page = notion_client.pages.create(
            parent={"database_id": conversion_db_id},
            properties={
                "Article Title": {
                    "title": [
                        {
                            "text": {
                                "content": article_title[:2000]  # Notion title limit
                            }
                        }
                    ]
                },
                "KCM URL": {
                    "url": kcm_url
                },
                "KCM Slug": {
                    "rich_text": [
                        {
                            "text": {
                                "content": kcm_slug
                            }
                        }
                    ]
                },
                "WordPress URL": {
                    "url": wordpress_url
                },
                "WordPress Slug": {
                    "rich_text": [
                        {
                            "text": {
                                "content": wordpress_slug
                            }
                        }
                    ]
                },
                "WordPress Post ID": {
                    "number": wordpress_post_id
                },
                "Focus Keyphrase": {
                    "rich_text": [
                        {
                            "text": {
                                "content": focus_keyphrase
                            }
                        }
                    ]
                },
                "Converted Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                },
                "Categories": {
                    "multi_select": [{"name": cat} for cat in categories[:10]]  # Limit to 10
                },
                "Tags": {
                    "multi_select": [{"name": tag} for tag in tags[:20]]  # Limit to 20
                },
                "SEO Title": {
                    "rich_text": [
                        {
                            "text": {
                                "content": seo_title
                            }
                        }
                    ]
                },
                "Meta Description": {
                    "rich_text": [
                        {
                            "text": {
                                "content": meta_description[:2000]
                            }
                        }
                    ]
                },
                "Internal Links Count": {
                    "number": internal_links_count
                },
                "Status": {
                    "select": {
                        "name": status
                    }
                }
            }
        )

        page_id = new_page.get('id')
        logger.info(f"✅ Added conversion record to Notion: {article_title} (Page ID: {page_id})")
        return page_id

    except Exception as e:
        logger.error(f"Failed to add conversion record to Notion: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def create_conversion_database_schema():
    """
    Returns the schema for the Notion conversion tracking database
    This is for documentation - user needs to create the database manually
    """
    return {
        "Database Name": "Blog Post Conversions",
        "Properties": {
            "Article Title": "Title (text)",
            "KCM URL": "URL",
            "KCM Slug": "Text",
            "WordPress URL": "URL",
            "WordPress Slug": "Text",
            "WordPress Post ID": "Number",
            "Focus Keyphrase": "Text",
            "Converted Date": "Date",
            "Categories": "Multi-select",
            "Tags": "Multi-select",
            "SEO Title": "Text",
            "Meta Description": "Text",
            "Internal Links Count": "Number",
            "Status": "Select (options: Published, Draft, Failed)"
        }
    }

#!/usr/bin/env python3
"""
KCM Blog Converter Server
Flask server for converting KeepingCurrentMatters.com blogs to South Jersey localized content
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
import base64
import mimetypes
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from anthropic import Anthropic
from pathlib import Path
import sys

# Add shared folder to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'shared'))
from wordpress_taxonomy import get_categories_prompt, get_tags_prompt
from kcm_to_wordpress_mapping import parse_kcm_recommendations, merge_taxonomy
from wordpress_taxonomy_ids import build_webhook_payload
from notion_conversion_tracker import get_url_mappings, add_conversion_record
from link_replacer import replace_kcm_links, extract_kcm_links
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from shared folder
env_path = Path(__file__).parent.parent / 'shared' / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Initialize API clients
notion_client = NotionClient(auth=os.getenv('NOTION_API_KEY'))
claude_client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
database_id = os.getenv('NOTION_DATABASE_ID')

# WordPress configuration
WORDPRESS_SITE_URL = os.getenv('WORDPRESS_SITE_URL', 'https://mikesellsnj.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'admin')
WORDPRESS_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD', '')

# Master document name
MASTER_DOC_NAME = "South Jersey Real Estate Context Guide"

# Store last webhook payload for retry functionality
last_webhook_payload = None
# Store uploaded image data for the current conversion
uploaded_images = []


def migrate_kcm_links(html: str) -> str:
    """
    Migrate KCM links to MSNJ format
    From: https://www.simplifyingthemarket.com/en/2025/09/24/[slug]/?a=211199-eed154519afbfe4c41f1265fedb5efcd
    To: https://mikesellsnj.com/[slug]/
    """
    # Pattern to match KCM links
    kcm_pattern = r'https?://www\.simplifyingthemarket\.com/en/\d{4}/\d{2}/\d{2}/([^/?]+)/?(?:\?[^"]*)?'

    def replace_link(match):
        slug = match.group(1)
        return f'https://mikesellsnj.com/{slug}/'

    modified_html = re.sub(kcm_pattern, replace_link, html)

    # Count migrations
    count = len(re.findall(kcm_pattern, html))
    if count > 0:
        logger.info(f"Migrated {count} KCM links to MSNJ format")

    return modified_html


def convert_image_urls(html: str, uploaded_image_mapping: Dict[str, str] = None) -> str:
    """
    Convert image URLs to WordPress structure using uploaded image mapping
    Updates both <img src> and <a href> tags wrapping images
    Target format: Full WordPress URL from uploaded images

    Args:
        html: HTML content with image tags
        uploaded_image_mapping: Dict mapping original URLs to WordPress URLs (from uploaded images)
    """
    if not uploaded_image_mapping:
        # No images uploaded yet, return original HTML
        logger.warning("No uploaded image mapping provided - images will not be updated in HTML")
        return html

    # First, replace <img src> attributes
    img_pattern = r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>'

    def replace_img(match):
        before_src = match.group(1)
        original_url = match.group(2)
        after_src = match.group(3)

        # Check if we have a WordPress URL for this original URL
        if original_url in uploaded_image_mapping:
            # Use the WordPress URL from our uploaded images
            wordpress_url = uploaded_image_mapping[original_url]
            logger.info(f"Replacing img src: {original_url[:50]}... -> {wordpress_url}")
            return f'<img {before_src}src="{wordpress_url}"{after_src}>'
        else:
            # Keep original if not in mapping
            return match.group(0)

    modified_html = re.sub(img_pattern, replace_img, html)

    # Second, replace <a href> attributes that link to images
    # Pattern to match <a href="image-url">
    link_pattern = r'<a\s+([^>]*?)href="([^"]+)"([^>]*?)>'

    def replace_link(match):
        before_href = match.group(1)
        original_url = match.group(2)
        after_href = match.group(3)

        # Check if this link URL matches any original image URL
        if original_url in uploaded_image_mapping:
            # Replace the link to point to WordPress image
            wordpress_url = uploaded_image_mapping[original_url]
            logger.info(f"Replacing a href: {original_url[:50]}... -> {wordpress_url}")
            return f'<a {before_href}href="{wordpress_url}"{after_href}>'
        else:
            # Keep original if not in mapping
            return match.group(0)

    modified_html = re.sub(link_pattern, replace_link, modified_html)

    # Count conversions
    count = len([url for url in uploaded_image_mapping.keys() if url in html])
    if count > 0:
        logger.info(f"Converted {count} image URLs to WordPress structure")

    return modified_html


def remove_em_dashes(html: str) -> str:
    """Remove all em dashes (—) from the HTML"""
    # Remove em dash character
    html = html.replace('—', '-')
    # Remove HTML entity version
    html = html.replace('&mdash;', '-')
    html = html.replace('&#8212;', '-')
    return html


def extract_topics_from_blog(blog_html: str) -> List[str]:
    """Extract key topics from blog post HTML using Claude"""
    logger.info("Extracting topics from blog post...")

    # Remove HTML tags for analysis
    text_content = re.sub(r'<[^>]+>', ' ', blog_html)
    text_content = re.sub(r'\s+', ' ', text_content).strip()

    # Truncate if too long
    max_chars = 10000
    if len(text_content) > max_chars:
        text_content = text_content[:max_chars]

    prompt = f"""Analyze this real estate blog post and extract the key topics, themes, and concepts.
Focus on:
- Main real estate topics (e.g., "downsizing", "first-time buyers", "equity", "market trends")
- Target audience or demographics
- Seasonal or timing aspects
- Financial concepts or programs mentioned

Blog content:
{text_content}

Return a JSON array of 5-15 key topics/keywords that would be useful for finding relevant local context.
Return ONLY the JSON array, no additional text.
Example: ["downsizing", "equity", "senior homeowners", "spring selling season"]"""

    try:
        message = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Clean up response
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1])

        topics = json.loads(response_text)
        logger.info(f"Extracted {len(topics)} topics")

        return topics
    except Exception as e:
        logger.error(f"Failed to extract topics: {e}")
        return ["real estate", "South Jersey", "home buying", "selling"]


def search_notion_database(topics: List[str]) -> List[Dict]:
    """Search Notion database for relevant content based on topics"""
    logger.info("Searching Notion database...")

    try:
        # Get all pages
        all_pages = []
        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                response = notion_client.databases.query(
                    database_id=database_id,
                    start_cursor=start_cursor
                )
            else:
                response = notion_client.databases.query(database_id=database_id)

            all_pages.extend(response['results'])
            has_more = response['has_more']
            start_cursor = response.get('next_cursor')

        logger.info(f"Found {len(all_pages)} total pages")

        # Score and rank pages
        scored_pages = []
        master_doc = None

        for page in all_pages:
            title_prop = page['properties'].get('Title', {})
            if title_prop.get('title'):
                title = title_prop['title'][0]['text']['content']
            else:
                title = "Untitled"

            # Always capture master doc
            if MASTER_DOC_NAME.lower() in title.lower():
                master_doc = {
                    'id': page['id'],
                    'title': title,
                    'url': page['url'],
                    'is_master': True
                }
                logger.info(f"Found master document: {title}")
                continue

            # Score based on keyword matches
            score = 0
            page_text = title.lower()

            keywords_prop = page['properties'].get('Keywords / Tags', {})
            if keywords_prop.get('multi_select'):
                for tag in keywords_prop['multi_select']:
                    page_text += " " + tag['name'].lower()
            elif keywords_prop.get('rich_text') and keywords_prop['rich_text']:
                page_text += " " + keywords_prop['rich_text'][0]['text']['content'].lower()

            for topic in topics:
                topic_lower = topic.lower()
                if topic_lower in page_text:
                    score += page_text.count(topic_lower)

            if score > 0:
                scored_pages.append({
                    'id': page['id'],
                    'title': title,
                    'url': page['url'],
                    'score': score,
                    'is_master': False
                })

        # Sort by score
        scored_pages.sort(key=lambda x: x['score'], reverse=True)

        # Take top 5 relevant pages
        relevant_pages = scored_pages[:5]

        # Always include master doc first
        if master_doc:
            relevant_pages.insert(0, master_doc)

        logger.info(f"Selected {len(relevant_pages)} relevant documents")

        return relevant_pages

    except Exception as e:
        logger.error(f"Failed to search database: {e}")
        return []


def retrieve_page_content(page_id: str) -> str:
    """Retrieve full content of a Notion page"""
    try:
        blocks = []
        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                response = notion_client.blocks.children.list(
                    block_id=page_id,
                    start_cursor=start_cursor
                )
            else:
                response = notion_client.blocks.children.list(block_id=page_id)

            blocks.extend(response['results'])
            has_more = response['has_more']
            start_cursor = response.get('next_cursor')

        content_parts = []

        for block in blocks:
            block_type = block['type']

            if block_type == 'paragraph':
                text = extract_rich_text(block['paragraph']['rich_text'])
                if text:
                    content_parts.append(text)
            elif block_type == 'heading_1':
                text = extract_rich_text(block['heading_1']['rich_text'])
                if text:
                    content_parts.append(f"\n## {text}\n")
            elif block_type == 'heading_2':
                text = extract_rich_text(block['heading_2']['rich_text'])
                if text:
                    content_parts.append(f"\n### {text}\n")
            elif block_type == 'heading_3':
                text = extract_rich_text(block['heading_3']['rich_text'])
                if text:
                    content_parts.append(f"\n#### {text}\n")
            elif block_type == 'bulleted_list_item':
                text = extract_rich_text(block['bulleted_list_item']['rich_text'])
                if text:
                    content_parts.append(f"• {text}")
            elif block_type == 'numbered_list_item':
                text = extract_rich_text(block['numbered_list_item']['rich_text'])
                if text:
                    content_parts.append(f"- {text}")

        return '\n'.join(content_parts)

    except Exception as e:
        logger.error(f"Failed to retrieve page content: {e}")
        return ""


def extract_rich_text(rich_text_array: List) -> str:
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return ''.join([text['text']['content'] for text in rich_text_array])


def extract_article_slug(html: str) -> str:
    """Extract article slug from title, H1, H2, or H3"""
    title = None

    # Try to extract from H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
    if h1_match:
        title = h1_match.group(1)
        logger.info(f"Extracted title from H1: {title[:60]}...")
    else:
        # Try to extract from H2 (first one)
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE)
        if h2_match:
            title = h2_match.group(1)
            logger.info(f"Extracted title from H2: {title[:60]}...")
        else:
            # Try to extract from H3 (first one)
            h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', html, re.IGNORECASE)
            if h3_match:
                title = h3_match.group(1)
                logger.info(f"Extracted title from H3: {title[:60]}...")
            else:
                # Try to extract from title tag
                title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1)
                    logger.info(f"Extracted title from <title> tag: {title[:60]}...")
                else:
                    logger.warning("No H1, H2, H3, or title tag found - using 'article' as fallback")
                    title = "article"

    # Remove HTML tags from title
    title = re.sub(r'<[^>]+>', '', title)

    # Convert to slug
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars (including apostrophes, question marks, etc.)
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'-+', '-', slug)  # Remove multiple hyphens
    slug = slug.strip('-')  # Remove leading/trailing hyphens

    # Limit length
    slug = slug[:50]

    final_slug = slug if slug else "article"
    logger.info(f"Final slug: {final_slug}")

    return final_slug


def download_image(url: str) -> Optional[bytes]:
    """Download image from URL and return bytes"""
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.content
        else:
            logger.error(f"Failed to download image {url}: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading image {url}: {e}")
        return None


def upload_image_to_wordpress(image_data: bytes, filename: str, alt_text: str = "") -> Optional[Dict]:
    """
    Upload image to WordPress media library via REST API with proper SEO filename

    Args:
        image_data: Raw image bytes
        filename: Desired SEO-optimized filename
        alt_text: Alt text for the image

    Returns:
        Dict with id, url, and other WordPress media metadata, or None on failure
    """
    if not WORDPRESS_APP_PASSWORD:
        logger.error("WordPress app password not configured")
        return None

    try:
        # Create auth header
        auth_string = f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}"
        auth_bytes = auth_string.encode('utf-8')
        auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

        # Determine content type
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = 'image/png'

        # Upload to WordPress with SEO-optimized filename
        upload_url = f"{WORDPRESS_SITE_URL}/wp-json/wp/v2/media"

        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': content_type
        }

        response = requests.post(
            upload_url,
            headers=headers,
            data=image_data,
            timeout=30
        )

        if response.status_code == 201:
            media_data = response.json()
            media_id = media_data['id']

            # WordPress often ignores Content-Disposition, so we need to rename via post update
            # Extract the slug from our desired filename (without extension)
            slug_name = os.path.splitext(filename)[0]

            # Update the media post with correct slug, alt text, and title
            update_url = f"{WORDPRESS_SITE_URL}/wp-json/wp/v2/media/{media_id}"
            update_data = {
                'slug': slug_name,
                'alt_text': alt_text,
                'title': slug_name.replace('-', ' ').title()
            }

            update_response = requests.post(
                update_url,
                headers={'Authorization': f'Basic {auth_b64}'},
                json=update_data,
                timeout=10
            )

            if update_response.status_code == 200:
                updated_media = update_response.json()
                actual_url = updated_media['source_url']
                logger.info(f"✅ Uploaded and renamed image: {filename} (ID: {media_id})")
                logger.info(f"   WordPress URL: {actual_url}")
            else:
                # Use original URL if update failed
                actual_url = media_data['source_url']
                logger.warning(f"⚠️ Image uploaded but rename failed: {filename} (ID: {media_id})")
                logger.warning(f"   Using URL: {actual_url}")

            return {
                'id': media_id,
                'url': actual_url,
                'filename': filename,
                'alt_text': alt_text
            }
        else:
            logger.error(f"WordPress upload failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        logger.error(f"Error uploading image to WordPress: {e}")
        return None


def extract_images(original_html: str, converted_html: str, focus_keyphrase: str = "") -> List[Dict]:
    """
    Extract all images and generate SEO/GEO optimized filenames and alt text

    Args:
        original_html: Original blog HTML
        converted_html: Converted blog HTML
        focus_keyphrase: Primary SEO keyphrase (used in 50%+ of alt text per ACTIVE prompt guidelines)
    """
    logger.info("Extracting images from blog post...")
    if focus_keyphrase:
        logger.info(f"Focus keyphrase for alt text: {focus_keyphrase}")

    # Debug: Show first 500 chars of converted HTML to see what we're working with
    logger.info(f"Converted HTML preview (first 500 chars): {converted_html[:500]}")

    # Extract article slug
    slug = extract_article_slug(converted_html)
    logger.info(f"Extracted slug for images: {slug}")

    # Extract meaningful topic words from focus keyphrase (avoiding location words)
    # This creates unique filenames and avoids duplicates like "home-south-jersey-guide.png"
    location_words = ['south', 'jersey', 'nj', 'gloucester', 'camden', 'burlington',
                      'salem', 'cumberland', 'county', 'new', 'township', 'twp']

    if focus_keyphrase:
        # Split keyphrase into words and remove location words
        keyphrase_words = [w.strip().lower() for w in focus_keyphrase.split()]
        topic_words = [w for w in keyphrase_words if w not in location_words and len(w) > 2]

        # Take first 3 meaningful words for filename uniqueness
        if len(topic_words) >= 3:
            topic_term = '-'.join(topic_words[:3])
        elif len(topic_words) >= 2:
            topic_term = '-'.join(topic_words[:2])
        elif len(topic_words) >= 1:
            topic_term = topic_words[0]
        else:
            # Fallback to slug-based extraction
            slug_words = [w for w in slug.split('-') if w not in location_words and len(w) > 2]
            topic_term = '-'.join(slug_words[:3]) if len(slug_words) >= 3 else '-'.join(slug_words[:2]) if len(slug_words) >= 2 else 'real-estate'
    else:
        # No keyphrase - extract from slug
        slug_words = [w for w in slug.split('-') if w not in location_words and len(w) > 2]
        topic_term = '-'.join(slug_words[:3]) if len(slug_words) >= 3 else '-'.join(slug_words[:2]) if len(slug_words) >= 2 else 'real-estate'

    logger.info(f"Topic term for images (from keyphrase): {topic_term}")

    # Find all img tags
    img_pattern = r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>'
    matches = re.findall(img_pattern, original_html, re.IGNORECASE)

    if not matches:
        logger.info("No images found in blog post")
        return []

    images = []
    current_date = datetime.now()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')

    for index, match in enumerate(matches, 1):
        before_src = match[0]
        original_url = match[1]
        after_src = match[2]

        # Skip if already a WordPress URL or data URI
        if '/wp-content/' in original_url or original_url.startswith('data:'):
            continue

        # Extract extension from URL
        parsed = urlparse(original_url)
        filename = os.path.basename(parsed.path)
        ext = os.path.splitext(filename)[1] if '.' in filename else '.png'

        # Generate unique SEO-optimized filename
        # Uses 3 meaningful words from focus keyphrase (excluding location words)
        # Format: {topic-word-1}-{topic-word-2}-{topic-word-3}-{index}.ext
        # Example: first-time-buyer-guide.png, home-equity-tips-2.png
        # This avoids duplicates like "home-south-jersey-guide.png"
        if index == 1:
            suggested_filename = f"{topic_term}-guide{ext}"
        else:
            suggested_filename = f"{topic_term}-{index}{ext}"

        wordpress_path = f"/wp-content/uploads/{year}/{month}/{suggested_filename}"

        # Generate alt text following ACTIVE prompt guidelines:
        # - 50%+ must include exact focus keyphrase
        # - Remaining use variations or descriptive text
        # - Keep natural and descriptive

        # First try to extract existing alt text from original
        alt_match = re.search(r'alt=["\']([^"\']+)["\']', before_src + after_src, re.IGNORECASE)
        original_alt = alt_match.group(1) if alt_match else None

        # Determine if this image should include the exact keyphrase (50% rule)
        # Use modulo to ensure roughly 50% get keyphrase
        include_keyphrase = (index % 2 == 1)  # Odd-numbered images get exact keyphrase

        if include_keyphrase and focus_keyphrase:
            # Include exact focus keyphrase in alt text
            if original_alt:
                # Prepend keyphrase to existing alt text
                alt_text = f"{focus_keyphrase}: {original_alt}"
            else:
                # Create alt text with keyphrase
                alt_text = f"{focus_keyphrase} - infographic {index}"
            logger.info(f"  Image {index}: Using exact keyphrase in alt text")
        else:
            # Use variation or descriptive alt text
            if original_alt:
                # Enhance with geo if not present
                if 'south jersey' not in original_alt.lower() and 'nj' not in original_alt.lower():
                    alt_text = f"{original_alt} - South Jersey real estate"
                else:
                    alt_text = original_alt
            else:
                # Generate descriptive alt text without exact keyphrase
                clean_slug = slug.replace('-', ' ').title()
                alt_text = f"{clean_slug} guide - visual {index}"
            logger.info(f"  Image {index}: Using descriptive alt text (variation)")

        images.append({
            'position': index,
            'original_url': original_url,
            'suggested_filename': suggested_filename,
            'wordpress_path': wordpress_path,
            'alt_text': alt_text
        })

    logger.info(f"Extracted {len(images)} images with SEO/GEO optimized filenames")
    return images


def generate_seo_metadata(original_html: str, converted_html: str) -> Dict:
    """Generate SEO metadata for the converted blog post"""
    logger.info("Generating SEO metadata...")

    # Remove HTML tags for analysis
    text_content = re.sub(r'<[^>]+>', ' ', converted_html)
    text_content = re.sub(r'\s+', ' ', text_content).strip()

    # Extract title from H1 if present
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', converted_html, re.IGNORECASE)
    article_title = h1_match.group(1) if h1_match else "South Jersey Real Estate Article"

    # Get current year for context
    current_year = datetime.now().year

    prompt = f"""Analyze this South Jersey real estate blog post and generate SEO metadata.

IMPORTANT: This article is from {current_year}. Do NOT reference old years (2023, 2024, etc.) in titles or descriptions.

ARTICLE TITLE: {article_title}

ARTICLE CONTENT (first 2000 chars):
{text_content[:2000]}

Generate the following SEO metadata in JSON format:

1. **article_title**: The main article title (what appears as H1)

2. **categories**: Array of 1-3 WordPress categories from these EXACT options:
{get_categories_prompt()}

   Guidelines:
   - Use "For Buyers" for home buying, first-time buyers, move-up buyers
   - Use "For Sellers" for home selling, listing tips, pricing strategies
   - Use "Housing Market Updates" for market trends, statistics, forecasts
   - Add county categories if specific county/towns are heavily featured

3. **tags**: Array of 5-10 relevant tags from the following options:
{get_tags_prompt()}

   Guidelines:
   - MUST use tags from the list above - do NOT create new tags
   - Include topic tags that match the content (e.g., "Home Prices", "Interest Rates")
   - Include demographic tags if relevant (e.g., "First Time Home Buyers", "Move-up Buyers")
   - Do NOT include date tags - those will be auto-generated

   **TOWN TAG RULES (VERY STRICT):**
   - DEFAULT for general market articles: NO town tags at all
   - ONLY tag a town if the article is SPECIFICALLY ABOUT that town's market/trends
   - Town must appear 4+ times AND be central to the article's topic
   - Casual mentions or examples do NOT count - do not tag them
   - If the article mentions multiple towns casually (like examples), tag NONE of them
   - When in doubt: DO NOT tag it

4. **focus_keyphrase**: The primary SEO keyword phrase (3-6 words) - should include "South Jersey" or specific town

5. **seo_title**: Optimized title tag (50-60 characters) including location

6. **meta_description**: ONLY provide if different from default. Default is: %%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%
   If the default works, return the string "%%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%"
   Otherwise, provide a compelling 140-160 character custom meta description

Return ONLY valid JSON with these exact keys:
{{
  "article_title": "...",
  "categories": [...],
  "tags": [...],
  "focus_keyphrase": "...",
  "seo_title": "...",
  "meta_description": "..."
}}"""

    try:
        message = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()

        # Clean up response
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1])

        metadata = json.loads(response_text)
        logger.info("SEO metadata generated successfully")

        return metadata

    except Exception as e:
        logger.error(f"❌ FAILED TO GENERATE SEO METADATA - USING FALLBACK GENERIC TAGS ❌")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"This is why you're seeing generic categories and tags!")
        import traceback
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        return {
            "article_title": "South Jersey Real Estate Guide",
            "categories": ["Housing Market Updates"],
            "tags": ["Real Estate Market", "Home Prices", "Selling Tips", "Buying Tips"],  # Fixed to use exact tag names
            "focus_keyphrase": "South Jersey real estate",
            "seo_title": "South Jersey Real Estate Guide",
            "meta_description": "%%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%"
        }


def rewrite_blog_post(original_html: str, context_pages: List[Dict]) -> str:
    """Use Claude to rewrite the blog post with local South Jersey context"""
    logger.info("Retrieving content from selected pages...")

    # Retrieve full content from each page
    context_docs = []
    for page in context_pages:
        content = retrieve_page_content(page['id'])
        if content:
            context_docs.append({
                'title': page['title'],
                'content': content,
                'is_master': page.get('is_master', False)
            })
            logger.info(f"Retrieved content from: {page['title']}")

    if not context_docs:
        logger.error("No context retrieved")
        return ""

    # Build context section
    context_text = ""
    for doc in context_docs:
        marker = " [MASTER REFERENCE]" if doc['is_master'] else ""
        context_text += f"\n\n{'='*60}\n"
        context_text += f"Document: {doc['title']}{marker}\n"
        context_text += f"{'='*60}\n"
        context_text += doc['content']

    logger.info("Sending to Claude for rewriting...")

    # Load refined prompt template (ACTIVE version)
    prompt_path = Path(__file__).parent / 'kcm_prompt_ACTIVE.md'

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            refined_prompt_template = f.read()
        logger.info("Loaded refined prompt template: ACTIVE")
    except FileNotFoundError:
        logger.warning(f"Refined prompt template v4 not found at {prompt_path}, using fallback prompt")
        refined_prompt_template = """# KCM to South Jersey Blog Conversion

## MISSION
Convert national real estate content into South Jersey gold. Make readers stop scrolling. Drive action.

## CRITICAL REQUIREMENTS
- Preserve all existing internal links EXACTLY
- Replace ALL em dashes (—) with hyphens (-)
- Keep sentences 10-15 words (95% active voice)
- Maximum 4-5 town mentions total
- Use real data only from context documents
- Price range: $300K-$600K (adjust per town)

OUTPUT: Return ONLY the rewritten HTML. No preamble, no code fences."""

    prompt = f"""{refined_prompt_template}

---

## CONTENT TO CONVERT

### ORIGINAL BLOG POST (HTML):
{original_html}

### SOUTH JERSEY CONTEXT DOCUMENTS:
{context_text}

---

## CONVERSION INSTRUCTIONS

Apply ALL guidelines from the refined prompt above to convert this national content into localized South Jersey content.

**CRITICAL REMINDERS:**
- Preserve ALL existing internal links exactly as they appear
- DO NOT remove or modify ANY existing links
- Replace ALL em dashes (—, &mdash;, &#8212;) with regular hyphens (-)
- Use WordPress-compatible HTML formatting
- Draw statistics ONLY from the context documents provided
- Keep town mentions to 4-5 maximum total
- Maintain 75-85 Flesch Reading Ease score
- Use active voice 95%+ of the time

OUTPUT: Return ONLY the rewritten HTML. No preamble, no explanation, no code fences, just the complete localized blog post in HTML format ready for WordPress."""

    try:
        message = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )

        rewritten_html = message.content[0].text.strip()

        # Remove markdown code fences if present
        if rewritten_html.startswith('```html'):
            lines = rewritten_html.split('\n')
            rewritten_html = '\n'.join(lines[1:-1])
        elif rewritten_html.startswith('```'):
            lines = rewritten_html.split('\n')
            rewritten_html = '\n'.join(lines[1:-1])

        # Aggressively clean up any markdown sections Claude might have added
        # Remove any markdown headers at the beginning (# or ##)
        while rewritten_html.strip().startswith('#'):
            lines = rewritten_html.strip().split('\n')
            # Find first line that doesn't start with # (the actual HTML content)
            for i, line in enumerate(lines):
                if not line.strip().startswith('#'):
                    rewritten_html = '\n'.join(lines[i:])
                    break
            # Prevent infinite loop if all lines start with #
            if i == len(lines) - 1:
                break

        # Remove any markdown sections at the END
        # Look for patterns like "## OUTPUT", "### 1.", "### 2.", "## SEO", etc.
        # These typically appear after the HTML content ends
        end_section_patterns = [
            r'\n#+\s*(OUTPUT|SEO|IMAGE|KEYPHRASE|DELIVERABLE).*',
            r'\n###\s*\d+\..*',  # Numbered sections like "### 1. Rewritten HTML"
            r'\n##\s*\d+\..*'   # Numbered sections like "## 1. HTML"
        ]

        for pattern in end_section_patterns:
            match = re.search(pattern, rewritten_html, re.IGNORECASE | re.DOTALL)
            if match:
                rewritten_html = rewritten_html[:match.start()]
                logger.info(f"Removed markdown section from converted HTML (pattern: {pattern[:30]}...)")
                break  # Only need to find the first match since we're removing everything after it

        # Remove any remaining em dashes
        rewritten_html = remove_em_dashes(rewritten_html)

        # Migrate KCM links to MSNJ format
        rewritten_html = migrate_kcm_links(rewritten_html)

        # Note: Image URL conversion will happen after images are uploaded to WordPress
        # This ensures we use the actual WordPress URLs with SEO-optimized filenames

        logger.info(f"Blog post rewritten successfully ({len(rewritten_html)} chars)")

        return rewritten_html

    except Exception as e:
        logger.error(f"Failed to rewrite blog post: {e}")
        return ""


@app.route('/convert', methods=['POST'])
def convert():
    """Main endpoint for blog conversion"""
    try:
        data = request.json
        original_html = data.get('html', '')
        kcm_tags_text = data.get('kcm_tags', '')

        if not original_html:
            return jsonify({'error': 'No HTML provided'}), 400

        logger.info(f"Received conversion request ({len(original_html)} chars)")

        # Parse KCM recommended tags if provided
        kcm_taxonomy = {"categories": [], "tags": []}
        if kcm_tags_text and kcm_tags_text.strip():
            logger.info(f"Parsing KCM recommended tags: {kcm_tags_text[:100]}...")
            kcm_taxonomy = parse_kcm_recommendations(kcm_tags_text)
            logger.info(f"KCM taxonomy parsed: {kcm_taxonomy['categories']} categories, {len(kcm_taxonomy['tags'])} tags")

        # Extract topics
        topics = extract_topics_from_blog(original_html)

        # Search database
        relevant_pages = search_notion_database(topics)

        if not relevant_pages:
            return jsonify({'error': 'No relevant context found in Notion database'}), 500

        # Rewrite blog post
        converted_html = rewrite_blog_post(original_html, relevant_pages)

        if not converted_html:
            return jsonify({'error': 'Conversion failed'}), 500

        # Replace KCM internal links with WordPress links (if database is configured)
        logger.info("Checking for KCM internal links to replace...")
        url_mapping = get_url_mappings(notion_client)
        converted_html, link_stats = replace_kcm_links(converted_html, url_mapping)

        if link_stats['replaced'] > 0:
            logger.info(f"✅ Replaced {link_stats['replaced']} KCM links with WordPress URLs")
        if link_stats['not_found']:
            logger.warning(f"⚠️  {len(link_stats['not_found'])} KCM links not yet converted:")
            for url in link_stats['not_found']:
                logger.warning(f"   - {url}")

        # Generate SEO metadata (AI-generated)
        ai_seo_metadata = generate_seo_metadata(original_html, converted_html)

        # Merge KCM recommendations with AI suggestions
        # FIXED: Pass the actual category/tag lists, not the whole dictionaries
        seo_metadata = merge_taxonomy(
            kcm_taxonomy.get('categories', []),
            kcm_taxonomy.get('tags', []),
            ai_seo_metadata.get('categories', []),
            ai_seo_metadata.get('tags', [])
        )

        # Preserve other AI-generated fields
        seo_metadata['article_title'] = ai_seo_metadata.get('article_title', '')
        seo_metadata['focus_keyphrase'] = ai_seo_metadata.get('focus_keyphrase', '')
        seo_metadata['seo_title'] = ai_seo_metadata.get('seo_title', '')
        seo_metadata['meta_description'] = ai_seo_metadata.get('meta_description', '')

        # Extract images with focus keyphrase for SEO-optimized alt text
        focus_keyphrase = seo_metadata.get('focus_keyphrase', '')
        images = extract_images(original_html, converted_html, focus_keyphrase)

        # Calculate expansion ratio
        expansion = round(len(converted_html) / len(original_html), 2)

        return jsonify({
            'converted_html': converted_html,
            'original_length': len(original_html),
            'converted_length': len(converted_html),
            'expansion': expansion,
            'topics': topics,
            'documents_used': [p['title'] for p in relevant_pages],
            'seo': seo_metadata,
            'images': images,
            'link_replacement': link_stats
        })

    except Exception as e:
        logger.error(f"Conversion error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/send-to-wordpress', methods=['POST'])
def send_to_wordpress():
    """Send converted blog post to WordPress via n8n webhook"""
    global last_webhook_payload, uploaded_images

    try:
        data = request.json
        converted_html = data.get('converted_html', '')
        seo_metadata = data.get('seo_metadata', {})
        featured_image_id = data.get('featured_image_id', None)

        if not converted_html:
            return jsonify({'error': 'No HTML provided'}), 400

        if not seo_metadata:
            return jsonify({'error': 'No SEO metadata provided'}), 400

        logger.info("Building webhook payload for WordPress...")

        # Check if HTML contains images but none were uploaded
        if '<img' in converted_html and not uploaded_images:
            logger.warning("⚠️  HTML contains images but no images were uploaded to WordPress!")
            return jsonify({
                'error': 'Images not uploaded',
                'message': 'The converted HTML contains images, but you have not uploaded them to WordPress yet. Please upload images first using the "Upload Images to WordPress" button, then try sending to WordPress again.',
                'contains_images': True,
                'uploaded_count': 0
            }), 400

        # Use featured image from uploaded images if not provided and images were uploaded
        if not featured_image_id and uploaded_images:
            featured_image_id = uploaded_images[0]['wordpress_id']
            logger.info(f"Using first uploaded image as featured image: ID {featured_image_id}")

        # Update image URLs in HTML if images were uploaded
        if uploaded_images:
            # Create mapping of original URLs to WordPress URLs
            image_url_mapping = {img['original_url']: img['wordpress_url'] for img in uploaded_images}
            logger.info(f"Updating {len(image_url_mapping)} image URLs in HTML with WordPress URLs")
            converted_html = convert_image_urls(converted_html, image_url_mapping)

            # Remove first image from post content (it's the featured image)
            # Match first <img> tag (including any attributes before/after src)
            first_img_pattern = r'<img\s+[^>]*?src=["\'][^"\']+["\'][^>]*?>'
            match = re.search(first_img_pattern, converted_html, re.IGNORECASE)
            if match:
                # Also remove surrounding <br> tags if present
                img_with_breaks = re.sub(
                    r'<br\s*/?>\s*' + re.escape(match.group(0)) + r'\s*<br\s*/?>',
                    '',
                    converted_html,
                    count=1,
                    flags=re.IGNORECASE
                )
                if img_with_breaks != converted_html:
                    converted_html = img_with_breaks
                    logger.info("Removed first image (with surrounding breaks) from post content - it's the featured image")
                else:
                    # No breaks found, just remove the image
                    converted_html = converted_html.replace(match.group(0), '', 1)
                    logger.info("Removed first image from post content - it's the featured image")

        # Extract fields from seo_metadata for webhook payload
        title = seo_metadata.get('article_title', 'Untitled')
        categories = seo_metadata.get('categories', [])
        tags = seo_metadata.get('tags', [])

        # Build Yoast SEO meta (including focus keyphrase)
        yoast_meta = {
            'yoast_wpseo_focuskw': seo_metadata.get('focus_keyphrase', ''),
            'yoast_wpseo_title': seo_metadata.get('seo_title', ''),
            'yoast_wpseo_metadesc': seo_metadata.get('meta_description', '')
        }

        logger.info(f"Yoast SEO metadata: Focus Keyphrase = '{yoast_meta['yoast_wpseo_focuskw']}'")

        # Log what we're about to send
        logger.info(f"Categories to send: {categories}")
        logger.info(f"Tags to send: {tags}")

        # Build n8n webhook payload with properly structured parameters
        payload = build_webhook_payload(
            title=title,
            content=converted_html,
            excerpt='',  # Empty excerpt for now
            categories=categories,
            tags=tags,
            featured_media_id=featured_image_id,
            yoast_meta=yoast_meta
        )

        # CRITICAL: n8n workflow expects payload wrapped in 'body' key
        # n8n accesses data as: $('Webhook').item.json.body.body.tags
        # So we send: {'body': payload} which becomes body.body.tags in n8n
        wrapped_payload = {'body': payload}

        # Log the actual payload structure (without the huge content field)
        payload_debug = {k: v for k, v in payload.items() if k != 'content'}
        payload_debug['content'] = f"<{len(payload.get('content', ''))} chars>"
        logger.info(f"Webhook payload (inner): {payload_debug}")
        logger.info(f"Categories (IDs): {payload.get('categories', [])}")
        logger.info(f"Tags (IDs): {payload.get('tags', [])}")

        # Store payload for potential retry
        last_webhook_payload = wrapped_payload

        logger.info(f"Sending to n8n webhook: {len(converted_html)} chars")

        # Send to n8n webhook (production)
        webhook_url = "https://n8n.srv1007195.hstgr.cloud/webhook/wordpress-publish"

        response = requests.post(
            webhook_url,
            json=wrapped_payload,  # Send wrapped payload
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            logger.info("✅ Successfully sent to WordPress")

            # Get webhook response (needed regardless of Notion tracking)
            # n8n may return an array or object - handle both
            webhook_response_raw = response.json() if response.text else {}
            if isinstance(webhook_response_raw, list) and len(webhook_response_raw) > 0:
                webhook_response = webhook_response_raw[0]  # Extract first item from array
            elif isinstance(webhook_response_raw, dict):
                webhook_response = webhook_response_raw
            else:
                webhook_response = {}

            # Try to add conversion record to Notion (optional feature)
            try:
                kcm_url = data.get('kcm_url', '')  # Original KCM URL from frontend

                # WordPress REST API returns 'id' and 'link', not 'post_id' and 'post_url'
                wordpress_post_id = webhook_response.get('id', 0)
                wordpress_url = webhook_response.get('link', '')

                logger.info(f"Notion tracking data - KCM URL: {kcm_url}, WP Post ID: {wordpress_post_id}, WP URL: {wordpress_url}")

                if kcm_url and wordpress_post_id and wordpress_url:
                    # Extract slugs from URLs (full path for matching across different domains)
                    # Example: /en/2025/09/18/do-you-know-how-much-your-house-is-really-worth/
                    kcm_slug = urlparse(kcm_url).path.rstrip('/') if kcm_url else ''
                    wordpress_slug = urlparse(wordpress_url).path.rstrip('/') if wordpress_url else ''

                    # Count internal links
                    all_kcm_links = extract_kcm_links(converted_html)
                    internal_links_count = len(all_kcm_links)

                    # Ensure categories and tags are lists of strings (not IDs)
                    # They should already be lists of category/tag names from seo_metadata
                    category_list = categories if isinstance(categories, list) else []
                    tag_list = tags if isinstance(tags, list) else []

                    logger.info(f"Notion tracking - Categories: {category_list}, Tags: {tag_list}")

                    # Add to Notion conversion tracking database
                    notion_page_id = add_conversion_record(
                        notion_client=notion_client,
                        kcm_url=kcm_url,
                        kcm_slug=kcm_slug,
                        wordpress_url=wordpress_url,
                        wordpress_slug=wordpress_slug,
                        wordpress_post_id=wordpress_post_id,
                        article_title=title,
                        focus_keyphrase=seo_metadata.get('focus_keyphrase', ''),
                        categories=category_list,
                        tags=tag_list,
                        seo_title=seo_metadata.get('seo_title', ''),
                        meta_description=seo_metadata.get('meta_description', ''),
                        internal_links_count=internal_links_count,
                        status='Published'
                    )

                    if notion_page_id:
                        logger.info(f"✅ Conversion tracked in Notion (Page ID: {notion_page_id})")
                else:
                    logger.warning("⚠️  Missing KCM URL or WordPress details - skipping Notion tracking")

            except Exception as notion_error:
                # Don't fail the whole request if Notion tracking fails
                logger.error(f"Failed to add conversion record to Notion (non-critical): {notion_error}")

            return jsonify({
                'success': True,
                'message': 'Blog post sent to WordPress (draft created)',
                'webhook_response': webhook_response
            })
        else:
            logger.error(f"Webhook failed: {response.status_code} - {response.text}")
            return jsonify({
                'success': False,
                'error': f'Webhook returned status {response.status_code}',
                'details': response.text
            }), response.status_code

    except requests.exceptions.Timeout:
        logger.error("Webhook timeout")
        return jsonify({'error': 'Webhook request timed out'}), 504

    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook request error: {e}")
        return jsonify({'error': f'Failed to connect to webhook: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Error sending to WordPress: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/process-images', methods=['POST'])
def process_images():
    """Download images from KCM and upload to WordPress"""
    global uploaded_images

    try:
        data = request.json
        images = data.get('images', [])

        if not images:
            return jsonify({'error': 'No images provided'}), 400

        if not WORDPRESS_APP_PASSWORD or WORDPRESS_APP_PASSWORD == 'your_wordpress_app_password_here':
            return jsonify({
                'error': 'WordPress credentials not configured. Please set WORDPRESS_APP_PASSWORD in .env file.'
            }), 400

        logger.info(f"Processing {len(images)} images...")

        processed_images = []
        failed_images = []

        for img in images:
            original_url = img.get('original_url')
            suggested_filename = img.get('suggested_filename')
            alt_text = img.get('alt_text', '')

            logger.info(f"Processing image: {original_url}")

            # Download image
            image_data = download_image(original_url)
            if not image_data:
                failed_images.append({
                    'original_url': original_url,
                    'error': 'Failed to download'
                })
                continue

            # Upload to WordPress
            wp_result = upload_image_to_wordpress(image_data, suggested_filename, alt_text)
            if not wp_result:
                failed_images.append({
                    'original_url': original_url,
                    'error': 'Failed to upload to WordPress'
                })
                continue

            processed_images.append({
                'original_url': original_url,
                'wordpress_id': wp_result['id'],
                'wordpress_url': wp_result['url'],
                'filename': wp_result['filename'],
                'alt_text': wp_result['alt_text']
            })

        # Store for webhook use
        uploaded_images = processed_images

        logger.info(f"✅ Processed {len(processed_images)} images successfully, {len(failed_images)} failed")

        return jsonify({
            'success': True,
            'processed': len(processed_images),
            'failed': len(failed_images),
            'images': processed_images,
            'failures': failed_images,
            'featured_image_id': processed_images[0]['wordpress_id'] if processed_images else None
        })

    except Exception as e:
        logger.error(f"Error processing images: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/retry-webhook', methods=['POST'])
def retry_webhook():
    """Retry sending the last webhook payload to WordPress"""
    global last_webhook_payload

    try:
        if not last_webhook_payload:
            return jsonify({
                'success': False,
                'error': 'No webhook payload available. Please run "Convert to South Jersey" first.'
            }), 400

        logger.info("Retrying webhook with stored payload...")

        # Send to n8n webhook (production)
        webhook_url = "https://n8n.srv1007195.hstgr.cloud/webhook/wordpress-publish"

        response = requests.post(
            webhook_url,
            json=last_webhook_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            logger.info("✅ Successfully retried webhook to WordPress")
            return jsonify({
                'success': True,
                'message': 'Blog post sent to WordPress (draft created)',
                'webhook_response': response.json() if response.text else {}
            })
        else:
            logger.error(f"Webhook retry failed: {response.status_code} - {response.text}")
            return jsonify({
                'success': False,
                'error': f'Webhook returned status {response.status_code}',
                'details': response.text
            }), response.status_code

    except requests.exceptions.Timeout:
        logger.error("Webhook retry timeout")
        return jsonify({'error': 'Webhook request timed out'}), 504

    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook retry request error: {e}")
        return jsonify({'error': f'Failed to connect to webhook: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Error retrying webhook: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'notion_connected': bool(notion_client),
        'claude_connected': bool(claude_client),
        'wordpress_configured': bool(WORDPRESS_APP_PASSWORD and WORDPRESS_APP_PASSWORD != 'your_wordpress_app_password_here'),
        'wordpress_site': WORDPRESS_SITE_URL,
        'wordpress_username': WORDPRESS_USERNAME
    })


if __name__ == '__main__':
    logger.info("Starting KCM Blog Converter Server...")
    logger.info("Server will run on http://localhost:5000")
    logger.info("Open clipboard.html in your browser to use the converter")
    app.run(host='0.0.0.0', port=5000, debug=True)

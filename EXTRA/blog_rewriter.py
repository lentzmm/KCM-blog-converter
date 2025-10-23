#!/usr/bin/env python3
"""
Blog Rewriter Tool - Localizes national real estate content for South Jersey
Uses Notion Knowledge Base and Claude API to add local context and details
"""

import os
import sys
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from anthropic import Anthropic

# Add shared folder to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'shared'))
from wordpress_taxonomy import get_categories_prompt, get_tags_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blog_rewriter_log.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class BlogRewriter:
    """Main class to rewrite blog posts with South Jersey local context"""

    def __init__(self):
        """Initialize the blog rewriter with API credentials"""
        # Load .env from shared folder
        env_path = Path(__file__).parent.parent / 'shared' / '.env'
        load_dotenv(dotenv_path=env_path)

        # Load environment variables
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')

        # Validate required credentials
        self._validate_credentials()

        # Initialize API clients
        self.notion_client = None
        self.claude_client = None

        # Key document name to always retrieve
        self.master_doc_name = "South Jersey Real Estate Context Guide"

    def _validate_credentials(self):
        """Validate that all required credentials are present"""
        missing = []

        if not self.claude_api_key:
            missing.append('CLAUDE_API_KEY')
        if not self.notion_api_key:
            missing.append('NOTION_API_KEY')
        if not self.notion_database_id:
            missing.append('NOTION_DATABASE_ID')

        if missing:
            logger.error(f"Missing required environment variables: {', '.join(missing)}")
            logger.error("Please ensure your .env file is properly configured")
            sys.exit(1)

    def authenticate(self):
        """Authenticate with Notion and Claude APIs"""
        logger.info("Authenticating with APIs...")

        try:
            # Notion
            self.notion_client = NotionClient(auth=self.notion_api_key)
            db_info = self.notion_client.databases.retrieve(self.notion_database_id)
            logger.info(f"[OK] Connected to Notion database: {db_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")

            # Claude
            self.claude_client = Anthropic(api_key=self.claude_api_key)
            logger.info(f"[OK] Connected to Claude API")

            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def extract_topics_from_blog(self, blog_html: str) -> List[str]:
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
- Geographic references (states, regions, cities mentioned)
- Specific programs or financial concepts
- Target audience or demographics
- Seasonal or timing aspects

Blog content:
{text_content}

Return a JSON array of 5-15 key topics/keywords that would be useful for finding relevant local context.
Return ONLY the JSON array, no additional text.
Example: ["downsizing", "equity", "senior homeowners", "California market", "spring selling season"]"""

        try:
            message = self.claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text.strip()

            # Clean up response - remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])

            topics = json.loads(response_text)
            logger.info(f"[OK] Extracted {len(topics)} topics: {', '.join(topics[:5])}...")

            return topics
        except Exception as e:
            logger.error(f"Failed to extract topics: {e}")
            # Fallback to basic keyword extraction
            return ["real estate", "South Jersey", "home buying", "selling"]

    def search_notion_database(self, topics: List[str]) -> List[Dict]:
        """Search Notion database for relevant content based on topics"""
        logger.info("Searching Notion database for relevant content...")

        try:
            # Get all pages from database
            all_pages = []
            has_more = True
            start_cursor = None

            while has_more:
                if start_cursor:
                    response = self.notion_client.databases.query(
                        database_id=self.notion_database_id,
                        start_cursor=start_cursor
                    )
                else:
                    response = self.notion_client.databases.query(
                        database_id=self.notion_database_id
                    )

                all_pages.extend(response['results'])
                has_more = response['has_more']
                start_cursor = response.get('next_cursor')

            logger.info(f"[OK] Found {len(all_pages)} total pages in database")

            # Score and rank pages by relevance
            scored_pages = []
            master_doc = None

            for page in all_pages:
                # Extract title
                title_prop = page['properties'].get('Title', {})
                if title_prop.get('title'):
                    title = title_prop['title'][0]['text']['content']
                else:
                    title = "Untitled"

                # Always capture master doc
                if self.master_doc_name.lower() in title.lower():
                    master_doc = {
                        'id': page['id'],
                        'title': title,
                        'url': page['url'],
                        'is_master': True
                    }
                    logger.info(f"[OK] Found master document: {title}")
                    continue

                # Score based on keyword matches
                score = 0
                page_text = title.lower()

                # Add keywords/tags to search text
                keywords_prop = page['properties'].get('Keywords / Tags', {})
                if keywords_prop.get('multi_select'):
                    for tag in keywords_prop['multi_select']:
                        page_text += " " + tag['name'].lower()
                elif keywords_prop.get('rich_text') and keywords_prop['rich_text']:
                    page_text += " " + keywords_prop['rich_text'][0]['text']['content'].lower()

                # Calculate relevance score
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

            logger.info(f"[OK] Selected {len(relevant_pages)} relevant documents")
            for page in relevant_pages:
                marker = " [MASTER]" if page.get('is_master') else f" (score: {page.get('score', 0)})"
                logger.info(f"  - {page['title']}{marker}")

            return relevant_pages

        except Exception as e:
            logger.error(f"Failed to search Notion database: {e}")
            return []

    def retrieve_page_content(self, page_id: str) -> str:
        """Retrieve the full content of a Notion page"""
        try:
            # Get all blocks from the page
            blocks = []
            has_more = True
            start_cursor = None

            while has_more:
                if start_cursor:
                    response = self.notion_client.blocks.children.list(
                        block_id=page_id,
                        start_cursor=start_cursor
                    )
                else:
                    response = self.notion_client.blocks.children.list(block_id=page_id)

                blocks.extend(response['results'])
                has_more = response['has_more']
                start_cursor = response.get('next_cursor')

            # Extract text from blocks
            content_parts = []

            for block in blocks:
                block_type = block['type']

                if block_type == 'paragraph':
                    text = self._extract_rich_text(block['paragraph']['rich_text'])
                    if text:
                        content_parts.append(text)

                elif block_type == 'heading_1':
                    text = self._extract_rich_text(block['heading_1']['rich_text'])
                    if text:
                        content_parts.append(f"\n## {text}\n")

                elif block_type == 'heading_2':
                    text = self._extract_rich_text(block['heading_2']['rich_text'])
                    if text:
                        content_parts.append(f"\n### {text}\n")

                elif block_type == 'heading_3':
                    text = self._extract_rich_text(block['heading_3']['rich_text'])
                    if text:
                        content_parts.append(f"\n#### {text}\n")

                elif block_type == 'bulleted_list_item':
                    text = self._extract_rich_text(block['bulleted_list_item']['rich_text'])
                    if text:
                        content_parts.append(f"• {text}")

                elif block_type == 'numbered_list_item':
                    text = self._extract_rich_text(block['numbered_list_item']['rich_text'])
                    if text:
                        content_parts.append(f"- {text}")

            return '\n'.join(content_parts)

        except Exception as e:
            logger.error(f"Failed to retrieve page content: {e}")
            return ""

    def _extract_rich_text(self, rich_text_array: List) -> str:
        """Extract plain text from Notion rich text array"""
        if not rich_text_array:
            return ""
        return ''.join([text['text']['content'] for text in rich_text_array])

    def rewrite_blog_post(self, original_html: str, context_pages: List[Dict]) -> str:
        """Use Claude to rewrite the blog post with local South Jersey context"""
        logger.info("Retrieving content from selected pages...")

        # Retrieve full content from each page
        context_docs = []
        for page in context_pages:
            content = self.retrieve_page_content(page['id'])
            if content:
                context_docs.append({
                    'title': page['title'],
                    'content': content,
                    'is_master': page.get('is_master', False)
                })
                logger.info(f"[OK] Retrieved content from: {page['title']} ({len(content)} chars)")

        if not context_docs:
            logger.error("No context retrieved from Notion pages")
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

        prompt = f"""You are an expert real estate content writer specializing in South Jersey markets. Your task is to completely rewrite this generic national real estate blog post to be hyper-localized for South Jersey (Gloucester, Camden, Burlington, Salem, and Cumberland counties).

ORIGINAL BLOG POST (HTML):
{original_html}

SOUTH JERSEY CONTEXT DOCUMENTS:
{context_text}

REWRITING INSTRUCTIONS:

1. GEOGRAPHIC LOCALIZATION (CRITICAL):
   - Replace ALL generic references with specific South Jersey towns
   - Use actual municipalities: Haddonfield, Cherry Hill, Voorhees, Moorestown, Mount Laurel, Mullica Hill, Washington Township, Deptford, Woodbury, Woolwich, Pitman, Sewell, etc.
   - Reference appropriate counties: Gloucester, Camden, Burlington, Salem, Cumberland
   - Add proximity advantages: "20 minutes to Philadelphia", "45 minutes to Jersey Shore", "near major highways (295, 42, 55, AC Expressway)"
   - Use concrete local examples throughout

2. FINANCIAL DETAILS:
   - Use South Jersey price points: $300K-$600K typical range (adjust based on town)
   - Reference specific NJ programs: Senior Freeze, NJHMFA, attorney review period (3 business days)
   - Include property tax context where relevant
   - Mention closing costs specific to NJ

3. MARKET CONTEXT:
   - Emphasize market stability and steady appreciation
   - Reference housing diversity (colonials, ranches, new construction, historic homes)
   - Mention both suburbs (quiet family neighborhoods) and more active areas
   - Include local market dynamics from the context documents

4. EXPANSION REQUIREMENTS:
   - Significantly expand the content length with local details
   - Add specific examples, scenarios, and case studies using South Jersey locations
   - Include relevant local programs, resources, and considerations
   - Expand each main point with 2-3x more local detail

5. TONE & STYLE:
   - Maintain analytical, no-nonsense, informative tone
   - Be specific and concrete, not generic or vague
   - Sound like a local expert who knows these markets intimately
   - Keep the helpful, educational approach of the original

6. HTML FORMATTING:
   - Preserve the HTML structure (headings, paragraphs, lists, etc.)
   - Keep WordPress-compatible formatting
   - Maintain readability and proper tag closure

7. AUTHENTICITY:
   - Every geographic reference should be real and accurate
   - Every example should feel locally authentic
   - Use the provided context documents extensively
   - Don't make up statistics - use general ranges or omit

OUTPUT: Return ONLY the rewritten HTML. No preamble, no explanation, just the complete localized blog post in HTML format ready for WordPress."""

        try:
            message = self.claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=16000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            rewritten_html = message.content[0].text.strip()

            # Remove markdown code fences if present
            if rewritten_html.startswith('```html'):
                lines = rewritten_html.split('\n')
                rewritten_html = '\n'.join(lines[1:-1])
            elif rewritten_html.startswith('```'):
                lines = rewritten_html.split('\n')
                rewritten_html = '\n'.join(lines[1:-1])

            logger.info(f"[OK] Blog post rewritten successfully ({len(rewritten_html)} chars)")

            return rewritten_html

        except Exception as e:
            logger.error(f"Failed to rewrite blog post: {e}")
            return ""

    def generate_seo_metadata(self, rewritten_html: str) -> Dict[str, Any]:
        """Generate SEO metadata (categories, tags, etc.) for the rewritten blog"""
        logger.info("Generating SEO metadata...")

        # Remove HTML tags for analysis
        text_content = re.sub(r'<[^>]+>', ' ', rewritten_html)
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        # Extract title from H3 or first heading
        h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', rewritten_html, re.IGNORECASE)
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', rewritten_html, re.IGNORECASE)
        article_title = h3_match.group(1) if h3_match else (h1_match.group(1) if h1_match else "South Jersey Real Estate Article")

        # Get current year for context
        current_year = datetime.now().year

        prompt = f"""Analyze this South Jersey real estate blog post and generate SEO metadata.

IMPORTANT: This article is from {current_year}. Do NOT reference old years (2023, 2024, etc.) in titles or descriptions.

ARTICLE TITLE: {article_title}

ARTICLE CONTENT (first 2000 chars):
{text_content[:2000]}

Generate the following SEO metadata in JSON format:

1. **article_title**: The main article title (what appears as H1/H3)

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
   - Include specific town tags ONLY if that town is explicitly mentioned
   - Do NOT include date tags - those will be auto-generated

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
            message = self.claude_client.messages.create(
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
            logger.info("[OK] SEO metadata generated successfully")

            return metadata

        except Exception as e:
            logger.error(f"Failed to generate SEO metadata: {e}")
            return {
                "article_title": "South Jersey Real Estate Guide",
                "categories": ["Housing Market Updates"],
                "tags": ["New Jersey real estate", "real estate market", "Home Buying Advice", "Selling Tips"],
                "focus_keyphrase": "South Jersey real estate",
                "seo_title": "South Jersey Real Estate Guide",
                "meta_description": "%%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%"
            }

    def run_review_mode(self, blog_html: str):
        """Run in review mode - show context before rewriting"""
        logger.info("\n" + "="*60)
        logger.info("RUNNING IN REVIEW MODE")
        logger.info("="*60 + "\n")

        # Extract topics
        topics = self.extract_topics_from_blog(blog_html)

        print("\n" + "="*60)
        print("EXTRACTED TOPICS:")
        print("="*60)
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")

        # Search database
        relevant_pages = self.search_notion_database(topics)

        print("\n" + "="*60)
        print("RELEVANT DOCUMENTS FOUND:")
        print("="*60)
        for page in relevant_pages:
            marker = " [MASTER DOCUMENT]" if page.get('is_master') else f" (relevance score: {page.get('score', 0)})"
            print(f"• {page['title']}{marker}")
            print(f"  URL: {page['url']}")

        # Ask if user wants to proceed
        print("\n" + "="*60)
        response = input("\nProceed with rewriting using these documents? (yes/no): ").strip().lower()

        if response in ['yes', 'y']:
            print("\nProceeding with rewrite...\n")
            rewritten = self.rewrite_blog_post(blog_html, relevant_pages)

            if rewritten:
                # Generate SEO metadata
                print("\n" + "="*60)
                print("GENERATING SEO METADATA...")
                print("="*60)
                metadata = self.generate_seo_metadata(rewritten)

                # Display metadata
                print("\n📊 SEO METADATA:")
                print(f"  Title: {metadata.get('article_title')}")
                print(f"  Categories: {', '.join(metadata.get('categories', []))}")
                print(f"  Tags: {', '.join(metadata.get('tags', []))}")
                print(f"  Focus Keyphrase: {metadata.get('focus_keyphrase')}")
                print(f"  SEO Title: {metadata.get('seo_title')}")
                if metadata.get('meta_description') != "%%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%":
                    print(f"  Meta Description: {metadata.get('meta_description')}")

                # Save output
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"rewritten_blog_{timestamp}.html"
                metadata_file = f"rewritten_blog_{timestamp}_metadata.json"

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(rewritten)

                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)

                print("\n" + "="*60)
                print("SUCCESS!")
                print("="*60)
                print(f"Rewritten blog saved to: {output_file}")
                print(f"SEO metadata saved to: {metadata_file}")
                print(f"Original length: {len(blog_html)} chars")
                print(f"Rewritten length: {len(rewritten)} chars")
                print(f"Expansion: {len(rewritten) / len(blog_html):.1f}x")
            else:
                print("\n❌ Rewriting failed. Check the log for details.")
        else:
            print("\nRewrite cancelled.")

    def run_auto_mode(self, blog_html: str):
        """Run in auto mode - just do the rewrite"""
        logger.info("\n" + "="*60)
        logger.info("RUNNING IN AUTO MODE")
        logger.info("="*60 + "\n")

        # Extract topics
        topics = self.extract_topics_from_blog(blog_html)

        # Search database
        relevant_pages = self.search_notion_database(topics)

        if not relevant_pages:
            logger.error("No relevant documents found")
            return

        # Rewrite
        rewritten = self.rewrite_blog_post(blog_html, relevant_pages)

        if rewritten:
            # Generate SEO metadata
            metadata = self.generate_seo_metadata(rewritten)

            # Save output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"rewritten_blog_{timestamp}.html"
            metadata_file = f"rewritten_blog_{timestamp}_metadata.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rewritten)

            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

            print("\n" + "="*60)
            print("SUCCESS!")
            print("="*60)
            print(f"Rewritten blog saved to: {output_file}")
            print(f"SEO metadata saved to: {metadata_file}")
            print(f"Original length: {len(blog_html)} chars")
            print(f"Rewritten length: {len(rewritten)} chars")
            print(f"Expansion: {len(rewritten) / len(blog_html):.1f}x")
            print("\n📊 SEO METADATA:")
            print(f"  Categories: {', '.join(metadata.get('categories', []))}")
            print(f"  Tags: {', '.join(metadata.get('tags', []))}")
            print(f"  Focus Keyphrase: {metadata.get('focus_keyphrase')}")
            print("\nDocuments used:")
            for page in relevant_pages:
                marker = " [MASTER]" if page.get('is_master') else ""
                print(f"  • {page['title']}{marker}")
        else:
            print("\n❌ Rewriting failed. Check the log for details.")


def main():
    """Main entry point"""
    print("""
================================================================
         SOUTH JERSEY BLOG REWRITER
         Localizes national real estate content
================================================================
    """)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python blog_rewriter.py <input_file.html> [--auto]")
        print("")
        print("Options:")
        print("  --auto    Run in auto mode (no review step)")
        print("")
        print("Examples:")
        print("  python blog_rewriter.py blog.html")
        print("  python blog_rewriter.py blog.html --auto")
        print("")
        sys.exit(1)

    input_file = sys.argv[1]
    auto_mode = '--auto' in sys.argv

    # Read input file
    if not os.path.exists(input_file):
        print(f"[ERROR] File not found: {input_file}")
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            blog_html = f.read()

        if not blog_html.strip():
            print("[ERROR] Input file is empty")
            sys.exit(1)

        print(f"[OK] Loaded blog post from: {input_file} ({len(blog_html)} chars)")

    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        sys.exit(1)

    # Initialize rewriter
    try:
        rewriter = BlogRewriter()

        if not rewriter.authenticate():
            print("[ERROR] Authentication failed")
            sys.exit(1)

        print("")

        # Run in selected mode
        if auto_mode:
            rewriter.run_auto_mode(blog_html)
        else:
            rewriter.run_review_mode(blog_html)

    except KeyboardInterrupt:
        print("\n\n[WARNING] Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n[ERROR] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

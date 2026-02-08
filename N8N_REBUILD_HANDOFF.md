# KCM Blog Converter - Complete System Handoff for N8N Rebuild

**Project:** KCM-to-WordPress Blog Converter
**Purpose:** Convert national real estate content from KeepingCurrentMatters.com into localized South Jersey blog posts
**Current Stack:** Python Flask + Claude API + Notion + WordPress REST API
**Target:** Rebuild in N8N workflow automation
**Date:** 2025-02-08

---

## Executive Summary

This system converts generic real estate blog posts from KeepingCurrentMatters.com into hyper-localized South Jersey content using AI (Claude), publishes to WordPress with full SEO optimization, and tracks all conversions in Notion.

**Current Flow:**
```
HTML Input → Topic Extraction (Claude) → Context Retrieval (Notion) →
Rewriting (Claude + Guides) → Image Processing → Link Replacement →
WordPress Publishing → Notion Tracking
```

**Key Metrics:**
- Conversion time: ~60-90 seconds per post
- Content expansion: 1.5-2x original length
- SEO compliance: 100% Yoast-ready
- Image processing: Automatic download, rename, upload
- Link tracking: Full internal link replacement

---

## System Architecture

### Current Python Components

```
┌─────────────────────────────────────────────────────────┐
│           clipboard.html (Web UI)                       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP POST
┌────────────────────▼────────────────────────────────────┐
│    kcm_converter_server.py (Flask - 1,670 lines)        │
├──────────────────────────────────────────────────────────┤
│  Endpoints:                                              │
│  • /convert          - Main conversion                   │
│  • /process-images   - Upload images                     │
│  • /send-to-wordpress - Create post + n8n webhook        │
│  • /upload-all       - One-click combined                │
│  • /retry-webhook    - Retry failed webhook              │
│  • /health           - Status check                      │
└────┬───────────┬──────────────┬──────────────┬───────────┘
     │           │              │              │
     ▼           ▼              ▼              ▼
  Claude API   Notion API    WordPress      N8N Webhook
              (Context +      REST API      (Yoast SEO)
              Tracking)
```

### Data Sources & Integrations

| System | Purpose | Authentication | Data Flow |
|--------|---------|---------------|-----------|
| **Claude API** | Content rewriting, topic extraction, SEO generation | API Key | HTTP POST with prompt |
| **Notion** | Knowledge base + conversion tracking | Integration token | Query databases, create pages |
| **WordPress** | Target publishing platform | App Password (Basic Auth) | REST API: create posts, upload media |
| **N8N** | Yoast SEO metadata injection | Webhook | Receives payload, updates WP |

---

## Core Business Logic

### 1. Topic Extraction

**Input:** Original KCM HTML
**Process:** Claude analyzes content and extracts 5-15 key topics
**Output:** JSON array of keywords (e.g., ["downsizing", "equity", "market trends"])

**Current Implementation:**
```python
# Extract topics using Claude
prompt = """Analyze this real estate blog post and extract key topics.
Focus on: main topics, target audience, seasonal aspects, financial concepts.
Return JSON array of 5-15 keywords."""

response = claude_client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)
topics = json.loads(response.content[0].text)
```

**N8N Implementation:**
- HTTP Request node to Claude API
- JSON parser to extract topics array
- Pass to next node

---

### 2. Context Retrieval from Notion

**Input:** Topics array
**Process:**
1. Query Notion knowledge base (NOTION_DATABASE_ID)
2. Score pages based on topic matches in title and keywords
3. Retrieve top 5 + always include master doc ("South Jersey Real Estate Context Guide")

**Notion Database Structure (Knowledge Base):**
- **Title** (title): Page name
- **Keywords / Tags** (multi-select or rich text): For matching topics
- **Content**: Full page blocks (paragraphs, headings, lists)

**Scoring Algorithm:**
```python
for page in all_pages:
    score = 0
    page_text = title.lower() + keywords.lower()
    for topic in topics:
        if topic.lower() in page_text:
            score += page_text.count(topic.lower())

    if score > 0:
        scored_pages.append({'id': page_id, 'score': score})

# Return: master_doc + top_5_by_score
```

**N8N Implementation:**
- Notion "Search" node with database query
- Loop through results with scoring logic
- Sort and filter top 5
- Retrieve full page content for each

---

### 3. AI Rewriting Engine

**The Heart of the System** - This is where the magic happens.

**Inputs:**
1. Original KCM HTML
2. Master context doc from Notion
3. Top 5 relevant context docs
4. 5 guide documents (prompts):
   - `kcm_prompt_ACTIVE.md` - Main orchestration prompt
   - `town_naming_guide.md` - South Jersey towns database
   - `writing_mechanics_guide.md` - Human voice patterns, AI detection avoidance
   - `seo_optimization_guide.md` - Yoast requirements, keyphrase density
   - `technical_requirements_guide.md` - HTML preservation rules

**Claude Prompt Structure:**
```
[kcm_prompt_ACTIVE.md content]

---

CONTENT TO CONVERT:
[Original HTML]

SOUTH JERSEY CONTEXT DOCUMENTS:
[Master doc content]
[Top 5 docs content]

---

CRITICAL REQUIREMENTS:
- Localize to South Jersey towns (limit: 4-5 mentions total)
- Expand 1.5-2x with meaningful local details
- Remove ALL em dashes (— → -)
- Preserve all existing links EXACTLY
- Optimize for Yoast SEO
- Maintain 75-85 Flesch Reading Ease
- Use active voice 95%+ of time
- Keep sentences 10-15 words
- Avoid AI detection patterns

OUTPUT: Return ONLY the rewritten HTML
```

**Outputs:**
- Rewritten HTML (localized, expanded, optimized)
- Automatically cleaned (em dashes removed, markdown stripped)

**Critical Files to Port:**

1. **kcm_prompt_ACTIVE.md** (11KB) - Main prompt
2. **town_naming_guide.md** (12KB) - 50+ South Jersey towns with demographics
3. **writing_mechanics_guide.md** (12KB) - Sentence patterns, voice rules
4. **seo_optimization_guide.md** (18KB) - Yoast compliance checklist
5. **technical_requirements_guide.md** (12KB) - HTML handling rules

**N8N Implementation:**
- Read all 5 guide files (store as variables or static data)
- Concatenate into mega-prompt
- HTTP Request to Claude API
- Regex cleanup for markdown/em-dashes
- Pass HTML to next step

---

### 4. SEO Metadata Generation

**Input:** Converted HTML
**Process:** Claude analyzes content and generates SEO fields
**Output:** JSON with metadata

**SEO Fields Generated:**
```json
{
  "article_title": "Why South Jersey Home Prices Are Rising in 2025",
  "categories": ["For Buyers", "Housing Market Updates"],
  "tags": ["Home Prices", "Cherry Hill", "First Time Home Buyers"],
  "focus_keyphrase": "South Jersey home prices 2025",
  "seo_title": "South Jersey Home Prices 2025 | Market Trends",
  "meta_description": "Discover why South Jersey home prices are rising in 2025..."
}
```

**Categories (9 total):**
- Burlington County Real Estate
- Camden County Real Estate
- Cumberland County Real Estate
- For Buyers
- For Sellers
- Gloucester County Real Estate
- Housing Market Updates
- Salem County Real Estate
- Uncategorized

**Tags (50+ total):** See `shared/wordpress_taxonomy_ids.py` for complete list with WordPress IDs

**Category/Tag Selection Rules:**
1. Use "For Buyers" for home buying content
2. Use "For Sellers" for selling tips
3. Use "Housing Market Updates" for trends/data
4. Add county tags ONLY if heavily featured (4+ mentions)
5. Add town tags ONLY if article is specifically about that town
6. Default: NO town tags for general market articles

**N8N Implementation:**
- Second Claude API call with SEO generation prompt
- JSON parser
- Map category/tag names to WordPress IDs (see mapping table below)

---

### 5. WordPress Taxonomy Mapping

**Category Name → WordPress ID:**
```javascript
{
  "Burlington County Real Estate": 1042,
  "Camden County Real Estate": 1031,
  "Cumberland County Real Estate": 1036,
  "For Buyers": 881,
  "For Sellers": 882,
  "Gloucester County Real Estate": 1038,
  "Housing Market Updates": 884,
  "Salem County Real Estate": 1039,
  "Uncategorized": 1
}
```

**Tag Name → WordPress ID (Top 25):**
```javascript
{
  "Affordability": 1134,
  "Agent Value": 1135,
  "Baby Boomers": 1136,
  "Buying Tips": 1138,
  "Cherry Hill": 1054,
  "Clayton": 1053,
  "Collingswood": 1057,
  "Deptford": 1045,
  "Down Payments": 1141,
  "Downsize": 1142,
  "Economy": 1143,
  "Equity": 1144,
  "First Time Home Buyers": 1145,
  "For Sale by Owner": 1162,
  "Forecasts": 1146,
  "Home Prices": 1147,
  "Home Staging": 1148,
  "Home Value": 1149,
  "Inflation": 1150,
  "Interest Rates": 1152,
  "Millennials": 1154,
  "Moorestown": 1059,
  "Mortgage": 1155,
  "Pricing Strategy": 1157,
  "Real Estate Market": 1158
}
```

**Full List:** 50+ tags in `shared/wordpress_taxonomy_ids.py:21-84`

**N8N Implementation:**
- Create lookup table (dictionary/object)
- Map names to IDs before WordPress API call

---

### 6. Image Processing Pipeline

**Steps:**

1. **Extract Images from HTML**
   ```python
   pattern = r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>'
   matches = re.findall(pattern, original_html)
   ```

2. **Generate SEO Filenames**
   - Extract 3 meaningful words from focus keyphrase (exclude location words)
   - Format: `{topic-word-1}-{topic-word-2}-{topic-word-3}-{index}.ext`
   - Example: `home-equity-tips-2.png`

3. **Generate Alt Text (Yoast 50% Rule)**
   - 50% of images: Include exact focus keyphrase
   - 50% of images: Use variations or descriptive text
   - Format: `"{focus_keyphrase}: {original_alt}"` or `"{focus_keyphrase} - infographic {index}"`

4. **Download from Source**
   ```python
   response = requests.get(original_url, timeout=15)
   image_bytes = response.content
   ```

5. **Upload to WordPress**
   ```python
   POST /wp-json/wp/v2/media
   Headers:
     Authorization: Basic {base64(username:app_password)}
     Content-Disposition: attachment; filename="{seo_filename}"
     Content-Type: image/png
   Body: {image_bytes}

   Response: {"id": 12345, "source_url": "https://..."}
   ```

6. **Update HTML**
   - Replace original URLs with WordPress URLs
   - Remove first image from content (it becomes featured image)

**N8N Implementation:**
- HTTP Request to download images
- Loop through each image
- Binary data handling for upload
- WordPress REST API media endpoint
- String replacement in HTML

---

### 7. Link Replacement System

**Two Types of Links:**

**A. keepingcurrentmatters.com Links**
- Extract all KCM links from HTML
- Query Notion conversion database
- Replace with WordPress URLs if found
- Warn if not found

**B. simplifyingthemarket.com Links**
- Extract slug from URL pattern: `https://www.simplifyingthemarket.com/en/YYYY/MM/DD/{slug}/?a=...`
- Look up slug in Notion conversion database (KCM Slug field)
- Replace with final WordPress URL
- Fallback: `https://mikesellsnj.com/{slug}/` if not in database

**Notion Conversion Database Structure:**

| Property | Type | Purpose |
|----------|------|---------|
| Article Title | Title | Post title |
| KCM URL | URL | Original KCM link |
| KCM Slug | Text | Article slug (for simplifyingthemarket.com) |
| WordPress URL | URL | Final published URL |
| WordPress Slug | Text | WordPress permalink slug |
| WordPress Post ID | Number | WordPress post ID |
| Focus Keyphrase | Text | SEO keyphrase |
| Converted Date | Date | Conversion timestamp |
| Categories | Multi-select | WordPress categories |
| Tags | Multi-select | WordPress tags |
| SEO Title | Text | Yoast SEO title |
| Meta Description | Text | Meta description |
| Internal Links Count | Number | # of internal links found |
| Status | Select | Published / Draft / Failed |

**Link Replacement Logic:**
```python
# Query Notion for all Published posts
url_mapping = {}  # Full URL mapping
slug_mapping = {}  # Slug-only mapping

for page in notion_results:
    kcm_url = page.properties['KCM URL'].url
    kcm_slug = page.properties['KCM Slug'].rich_text[0].text
    wp_url = page.properties['WordPress URL'].url

    url_mapping[kcm_url] = wp_url
    slug_mapping[kcm_slug] = wp_url

# Replace links
html = replace_kcm_links(html, url_mapping, slug_mapping)
```

**N8N Implementation:**
- Notion query for conversion database
- Build lookup dictionaries
- Regex replacements in HTML
- Log warnings for missing links

---

### 8. WordPress Publishing

**Endpoint:** `POST /wp-json/wp/v2/posts`

**Authentication:** Basic Auth
```
Username: {WORDPRESS_USERNAME}
Password: {WORDPRESS_APP_PASSWORD}
```

**Payload Structure:**
```json
{
  "title": "Article Title",
  "content": "<p>Full HTML content...</p>",
  "excerpt": "",
  "slug": "article-slug",
  "status": "draft",
  "categories": [881, 884],
  "tags": [1054, 1138, 1145],
  "featured_media": 12345
}
```

**Response:**
```json
{
  "id": 42475,
  "link": "https://mikesellsnj.com/?p=42475",
  "title": {"rendered": "Article Title"},
  "featured_media": 12345,
  "categories": [881, 884],
  "tags": [1054, 1138, 1145]
}
```

**N8N Implementation:**
- HTTP Request node (POST)
- Basic Auth credentials
- Parse response for post ID and URL

---

### 9. Yoast SEO Injection (N8N Workflow)

**Current n8n Workflow:**

```
Webhook Trigger (from Python /send-to-wordpress)
    ↓
HTTP Request to WordPress REST API
    - Endpoint: POST /wp-json/wp/v2/posts
    - Body Parameters:
        * title: {{$('Webhook').item.json.body.body.title}}
        * content: {{$('Webhook').item.json.body.body.content}}
        * slug: {{$('Webhook').item.json.body.body.slug}}
        * categories: {{$('Webhook').item.json.body.body.categories}}
        * tags: {{$('Webhook').item.json.body.body.tags}}
        * featured_media: {{$('Webhook').item.json.body.body.featured_media}}
        * meta[_yoast_wpseo_focuskw]: {{$('Webhook').item.json.body.body.yoast_focus_keyword}}
        * meta[_yoast_wpseo_metadesc]: {{$('Webhook').item.json.body.body.yoast_meta_description}}
        * meta[_yoast_wpseo_title]: {{$('Webhook').item.json.body.body.yoast_seo_title}}
```

**Payload Sent to n8n:**
```json
{
  "body": {
    "title": "Article Title",
    "slug": "article-slug",
    "content": "...",
    "categories": [881],
    "tags": [1054, 1138],
    "featured_media": 12345,
    "yoast_focus_keyword": "south jersey homes",
    "yoast_meta_description": "Learn about...",
    "yoast_seo_title": "South Jersey Homes | Guide"
  }
}
```

**WordPress Plugin Required:** `wordpress-yoast-rest-api.php` (v2.1)
- Intercepts REST API requests
- Extracts `meta[_yoast_wpseo_*]` parameters
- Updates Yoast post meta fields

**N8N Rebuild Note:** You can skip the webhook entirely and send Yoast fields directly in the WordPress REST API call from N8N.

---

### 10. Notion Conversion Tracking

**After WordPress publish, create tracking record:**

```python
notion_client.pages.create(
    parent={"database_id": NOTION_CONVERSION_DB_ID},
    properties={
        "Article Title": {"title": [{"text": {"content": title}}]},
        "KCM URL": {"url": kcm_url},
        "KCM Slug": {"rich_text": [{"text": {"content": kcm_slug}}]},
        "WordPress URL": {"url": wordpress_url},
        "WordPress Slug": {"rich_text": [{"text": {"content": wp_slug}}]},
        "WordPress Post ID": {"number": post_id},
        "Focus Keyphrase": {"rich_text": [{"text": {"content": keyphrase}}]},
        "Converted Date": {"date": {"start": datetime.now().isoformat()}},
        "Categories": {"multi_select": [{"name": cat} for cat in categories]},
        "Tags": {"multi_select": [{"name": tag} for tag in tags]},
        "SEO Title": {"rich_text": [{"text": {"content": seo_title}}]},
        "Meta Description": {"rich_text": [{"text": {"content": meta_desc}}]},
        "Internal Links Count": {"number": links_count},
        "Status": {"select": {"name": "Published"}}
    }
)
```

**N8N Implementation:**
- Notion "Create Page" node
- Map all fields from previous steps
- Only create if post was successfully published

---

## Environment Variables Required

```env
# Claude API
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Notion
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # Knowledge base
NOTION_CONVERSION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx  # Conversion tracking

# WordPress
WORDPRESS_SITE_URL=https://mikesellsnj.com
WORDPRESS_USERNAME=lentzmm
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# N8N Webhook (if using separate webhook)
N8N_WEBHOOK_URL=https://n8n.srv1007195.hstgr.cloud/webhook/wordpress-publish
```

---

## N8N Workflow Design

### Recommended Node Structure

```
1. TRIGGER: Manual / Webhook / Schedule
   Input: Original KCM HTML

2. EXTRACT TOPICS (HTTP Request - Claude API)
   Prompt: Topic extraction
   Output: topics[]

3. QUERY NOTION KNOWLEDGE BASE (Notion - Database Query)
   Query by topics
   Output: relevant_pages[]

4. SCORE & FILTER PAGES (Code Node - JavaScript)
   Score pages by topic matches
   Output: top_5_pages[]

5. RETRIEVE PAGE CONTENT (Loop - Notion Get Page)
   For each page, get full content
   Output: context_text

6. LOAD GUIDE FILES (HTTP Request / File Read)
   Load 5 guide markdown files
   Output: guide_prompts

7. BUILD MEGA PROMPT (Code Node - JavaScript)
   Concatenate guides + context + original HTML
   Output: full_prompt

8. AI REWRITING (HTTP Request - Claude API)
   Send mega prompt
   Output: converted_html

9. CLEAN HTML (Code Node - JavaScript)
   Remove em dashes, strip markdown
   Output: cleaned_html

10. GENERATE SEO (HTTP Request - Claude API)
    Analyze HTML for SEO metadata
    Output: seo_metadata{}

11. MAP TAXONOMY (Code Node - JavaScript)
    Convert category/tag names to WP IDs
    Output: category_ids[], tag_ids[]

12. EXTRACT IMAGES (Code Node - Regex)
    Find all <img> tags
    Output: images[]

13. DOWNLOAD IMAGES (Loop - HTTP Request)
    Download each image
    Output: image_bytes[]

14. UPLOAD TO WORDPRESS (Loop - HTTP Request)
    POST /wp-json/wp/v2/media
    Output: wp_image_ids[], wp_image_urls[]

15. UPDATE IMAGE URLS (Code Node - String Replace)
    Replace KCM URLs with WP URLs
    Output: final_html

16. QUERY NOTION CONVERSIONS (Notion - Database Query)
    Get all converted posts
    Output: url_mapping{}, slug_mapping{}

17. REPLACE LINKS (Code Node - Regex Replace)
    Replace KCM links with WP links
    Output: linked_html

18. CREATE WORDPRESS POST (HTTP Request)
    POST /wp-json/wp/v2/posts
    Output: post_id, post_url

19. LOG TO NOTION (Notion - Create Page)
    Create conversion record
    Output: notion_page_id

20. RETURN SUCCESS
    Output: {post_id, post_url, success: true}
```

### Node Details

**Node 2: Extract Topics (Claude API)**
```javascript
// HTTP Request Node
Method: POST
URL: https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {{$env.CLAUDE_API_KEY}}
  anthropic-version: 2023-06-01
  content-type: application/json
Body:
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Analyze this real estate blog post and extract 5-15 key topics. Return ONLY a JSON array. Content: {{$node["Trigger"].json["html"]}}"
  }]
}
Output: Parse response.content[0].text as JSON
```

**Node 8: AI Rewriting (Claude API)**
```javascript
// HTTP Request Node
Method: POST
URL: https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {{$env.CLAUDE_API_KEY}}
  anthropic-version: 2023-06-01
  content-type: application/json
Body:
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 16000,
  "messages": [{
    "role": "user",
    "content": "{{$node["Build Mega Prompt"].json["prompt"]}}"
  }]
}
```

**Node 11: Map Taxonomy (Code Node)**
```javascript
// JavaScript code
const CATEGORY_IDS = {
  "For Buyers": 881,
  "For Sellers": 882,
  "Housing Market Updates": 884,
  "Burlington County Real Estate": 1042,
  // ... rest of mappings
};

const TAG_IDS = {
  "Affordability": 1134,
  "Cherry Hill": 1054,
  "First Time Home Buyers": 1145,
  // ... rest of mappings
};

const categories = $input.item.json.categories || [];
const tags = $input.item.json.tags || [];

const category_ids = categories.map(name => CATEGORY_IDS[name]).filter(id => id);
const tag_ids = tags.map(name => TAG_IDS[name]).filter(id => id);

return [{json: {category_ids, tag_ids}}];
```

**Node 18: Create WordPress Post**
```javascript
// HTTP Request Node
Method: POST
URL: {{$env.WORDPRESS_SITE_URL}}/wp-json/wp/v2/posts
Authentication: Basic Auth
  Username: {{$env.WORDPRESS_USERNAME}}
  Password: {{$env.WORDPRESS_APP_PASSWORD}}
Body Parameters:
  title: {{$node["SEO"].json["seo_title"]}}
  content: {{$node["Replace Links"].json["html"]}}
  slug: auto-generated from title
  status: draft
  categories: {{$node["Map Taxonomy"].json["category_ids"]}}
  tags: {{$node["Map Taxonomy"].json["tag_ids"]}}
  featured_media: {{$node["Upload Images"].first().json["id"]}}
  meta[_yoast_wpseo_focuskw]: {{$node["SEO"].json["focus_keyphrase"]}}
  meta[_yoast_wpseo_metadesc]: {{$node["SEO"].json["meta_description"]}}
  meta[_yoast_wpseo_title]: {{$node["SEO"].json["seo_title"]}}
```

---

## Critical Files to Port

### 1. Guide Files (Must be loaded into N8N)

**Location:** `/kcm-converter/`

| File | Size | Purpose | How to Use in N8N |
|------|------|---------|-------------------|
| `kcm_prompt_ACTIVE.md` | 11KB | Main orchestration prompt | Load as static text variable |
| `town_naming_guide.md` | 12KB | South Jersey towns database | Concatenate into prompt |
| `writing_mechanics_guide.md` | 12KB | Human voice, AI avoidance | Concatenate into prompt |
| `seo_optimization_guide.md` | 18KB | Yoast requirements | Concatenate into prompt |
| `technical_requirements_guide.md` | 12KB | HTML preservation | Concatenate into prompt |

**N8N Strategy:**
- Option A: Store files in N8N as workflow variables
- Option B: Host files on accessible URL and HTTP Request them
- Option C: Copy content into Code node as multi-line strings

### 2. Taxonomy Mapping

**Location:** `/shared/wordpress_taxonomy_ids.py`

**Full Category Mapping:**
```javascript
{
  "Burlington County Real Estate": 1042,
  "Camden County Real Estate": 1031,
  "Cumberland County Real Estate": 1036,
  "For Buyers": 881,
  "For Sellers": 882,
  "Gloucester County Real Estate": 1038,
  "Housing Market Updates": 884,
  "Salem County Real Estate": 1039,
  "Uncategorized": 1
}
```

**Full Tag Mapping (50 tags):**
```javascript
{
  "Affordability": 1134,
  "Agent Value": 1135,
  "Alloway": 1092,
  "Audubon": 1061,
  "Baby Boomers": 1136,
  "Barrington": 1114,
  "Bellmawr": 1115,
  "Berlin": 1116,
  "Bridgeton": 1077,
  "Brooklawn": 1118,
  "Burlington Twp": 1068,
  "Buying Myths": 1137,
  "Buying Tips": 1138,
  "Carneys Point": 1086,
  "Cherry Hill": 1054,
  "Cinnaminson": 1069,
  "Clayton": 1053,
  "Clementon": 1119,
  "Collingswood": 1057,
  "Commercial Twp": 1078,
  "Deerfield": 1076,
  "Delran": 1070,
  "Demographics": 1139,
  "Deptford": 1045,
  "Distressed Properties": 1140,
  "Down Payments": 1141,
  "Downsize": 1142,
  "East Greenwich": 1049,
  "Eastampton": 1101,
  "Economy": 1143,
  "Elk Twp": 1124,
  "Elmer": 1091,
  "Equity": 1144,
  "First Time Home Buyers": 1145,
  "For Sale by Owner": 1162,
  "Forecasts": 1146,
  "Home Prices": 1147,
  "Home Staging": 1148,
  "Home Value": 1149,
  "Haddonfield": 1055,
  "Haddon Heights": 1056,
  "Inflation": 1150,
  "Inspection": 1151,
  "Interest Rates": 1152,
  "Investment Properties": 1153,
  "Millennials": 1154,
  "Moorestown": 1059,
  "Mortgage": 1155,
  "Mount Laurel": 1060,
  "Move Up Buyers": 1156,
  "Pricing Strategy": 1157,
  "Real Estate Market": 1158,
  "Selling Tips": 1159,
  "Spring Market": 1160,
  "Summer Market": 1161,
  "Voorhees": 1051,
  "Washington Twp": 1052,
  "Wenonah": 1125,
  "West Deptford": 1046,
  "Westville": 1126,
  "Woodbury": 1127,
  "Woodbury Heights": 1128
}
```

**Copy this directly into N8N Code node.**

### 3. Regex Patterns

**Extract Images:**
```javascript
const imgPattern = /<img\s+([^>]*?)src="([^"]+)"([^>]*?)>/gi;
const matches = [];
let match;
while ((match = imgPattern.exec(html)) !== null) {
  matches.push({
    beforeSrc: match[1],
    url: match[2],
    afterSrc: match[3]
  });
}
```

**Extract simplifyingthemarket.com Links:**
```javascript
const kcmPattern = /https?:\/\/www\.simplifyingthemarket\.com\/en\/\d{4}\/\d{2}\/\d{2}\/([^/?]+)\/?(?:\?[^"]*)?/g;
const slugs = [];
let match;
while ((match = kcmPattern.exec(html)) !== null) {
  slugs.push(match[1]);  // Captured slug
}
```

**Remove Em Dashes:**
```javascript
html = html.replace(/—/g, '-');
html = html.replace(/&mdash;/g, '-');
html = html.replace(/&#8212;/g, '-');
```

**Clean Markdown Fences:**
```javascript
// Remove ```html and ``` wrappers
if (html.startsWith('```html')) {
  const lines = html.split('\n');
  html = lines.slice(1, -1).join('\n');
}
```

---

## Testing & Validation

### Test Data

**Sample KCM HTML Input:**
```html
<h3>Why Home Prices Are Rising This Year</h3>
<p>According to the latest data, home prices are on the rise. Here's what you need to know.</p>
<img src="https://kcmblog.com/wp-content/uploads/chart.png" alt="Price chart">
<p>As a buyer, you should consider these factors...</p>
```

**Expected Output:**
```html
<h3>Why South Jersey Home Prices Are Rising in 2025</h3>
<p>Cherry Hill and Moorestown are seeing home prices climb. Local data shows median prices in Camden County hit $385,000 this quarter. Here's what South Jersey buyers need to know.</p>
<img src="https://mikesellsnj.com/wp-content/uploads/2025/02/south-jersey-home-prices-guide.png" alt="South Jersey home prices 2025: price chart">
<p>As a first-time buyer in South Jersey, you should consider these local market factors...</p>
```

### Validation Checklist

- [ ] HTML structure preserved (all tags closed)
- [ ] All original links intact
- [ ] Em dashes removed
- [ ] Images uploaded to WordPress
- [ ] Image URLs updated in HTML
- [ ] Featured image set correctly
- [ ] Categories and tags applied (as IDs)
- [ ] Yoast SEO fields populated
- [ ] Post created as draft in WordPress
- [ ] Notion conversion record created
- [ ] Internal KCM links replaced
- [ ] Flesch Reading Ease: 75-85
- [ ] Town mentions: 4-5 max
- [ ] Content expanded 1.5-2x

---

## Error Handling & Edge Cases

### Common Failures

1. **Claude API timeout** (16,000 token response)
   - Solution: Retry once, if fails again use shorter prompt

2. **Image download fails** (404, timeout)
   - Solution: Skip image, log warning, continue

3. **WordPress auth fails** (401)
   - Solution: Verify app password, check Basic Auth header

4. **Notion query returns no results**
   - Solution: Use default master doc only, continue

5. **No images in article**
   - Solution: Skip image processing, no featured image

6. **Yoast fields not set**
   - Solution: Verify WordPress plugin active, check meta[] syntax

7. **Link replacement fails**
   - Solution: Use fallback URLs, log warnings

### Retry Logic

**Claude API:** Retry once with exponential backoff (2s)
**WordPress API:** Retry once with exponential backoff (2s)
**Notion API:** Retry once with exponential backoff (2s)
**Image downloads:** No retry (skip failed images)

---

## Performance Benchmarks

**Current Python System:**
- Topic extraction: ~5 seconds
- Context retrieval: ~3 seconds
- AI rewriting: ~30-45 seconds
- Image processing: ~5-10 seconds (per image)
- WordPress publishing: ~2 seconds
- Notion tracking: ~1 second
- **Total:** 60-90 seconds per post

**Expected N8N Performance:**
- Similar timing (limited by Claude API)
- Possible parallel processing for images
- Estimated: 60-90 seconds per post

---

## Migration Checklist

### Phase 1: Setup (Week 1)
- [ ] Install N8N (if not already)
- [ ] Configure Claude API credentials
- [ ] Configure Notion API credentials
- [ ] Configure WordPress API credentials
- [ ] Set up environment variables
- [ ] Create test workflow

### Phase 2: Core Logic (Week 2)
- [ ] Implement topic extraction node
- [ ] Implement Notion query + scoring
- [ ] Load all 5 guide files
- [ ] Build mega-prompt concatenation
- [ ] Implement AI rewriting call
- [ ] Add HTML cleanup logic

### Phase 3: SEO & Taxonomy (Week 3)
- [ ] Implement SEO generation
- [ ] Create category/tag mapping
- [ ] Test taxonomy assignment
- [ ] Validate Yoast field format

### Phase 4: Images (Week 4)
- [ ] Image extraction regex
- [ ] Image download loop
- [ ] WordPress media upload
- [ ] HTML URL replacement
- [ ] Featured image assignment

### Phase 5: Links (Week 5)
- [ ] Notion conversion database query
- [ ] Build URL mapping
- [ ] Build slug mapping
- [ ] Implement link replacement
- [ ] Test fallback logic

### Phase 6: Publishing (Week 6)
- [ ] WordPress post creation
- [ ] Yoast SEO injection
- [ ] Notion tracking record
- [ ] Error handling
- [ ] Success logging

### Phase 7: Testing (Week 7)
- [ ] End-to-end test with sample post
- [ ] Verify all SEO fields
- [ ] Check image quality
- [ ] Validate links
- [ ] Review HTML output

### Phase 8: Production (Week 8)
- [ ] Deploy to production N8N
- [ ] Create user documentation
- [ ] Train users
- [ ] Monitor first 10 conversions
- [ ] Decommission Python system

---

## Support & Troubleshooting

### Python System Reference

**Flask Server Logs:**
```bash
# Run server
cd /home/user/KCM-blog-converter
python kcm-converter/kcm_converter_server.py

# Server URL
http://localhost:5000

# Endpoints
GET  /health
POST /convert
POST /process-images
POST /send-to-wordpress
POST /upload-all
POST /retry-webhook
```

**Key Log Messages:**
```
✅ Replaced 3 KCM links with WordPress URLs
⚠️  2 KCM links not yet converted
✅ Uploaded 3 images, using first as featured image
✅ Conversion tracked in Notion (Page ID: xyz)
Yoast SEO metadata: Focus Keyphrase = 'south jersey homes'
```

### Debugging Tips

1. **Check Claude API response:**
   - Look for `response.content[0].text`
   - Validate JSON parsing
   - Check for markdown fences

2. **Verify Notion database structure:**
   - All property names match exactly
   - Status has "Published" option (case-sensitive)
   - Database shared with integration

3. **WordPress authentication:**
   - Test with curl first
   - Verify app password (no spaces in env file)
   - Check Basic Auth header format

4. **Image issues:**
   - Check image URL accessibility
   - Verify WordPress media permissions
   - Test manual upload via WordPress UI

---

## Contact & Handoff

**Current System Maintainer:** Claude (AI Assistant)
**System Documentation:** This file + Python codebase
**Code Repository:** `/home/user/KCM-blog-converter/`
**WordPress Site:** https://mikesellsnj.com
**N8N Instance:** https://n8n.srv1007195.hstgr.cloud

**Critical Files for Reference:**
- `kcm-converter/kcm_converter_server.py` - Main server logic
- `shared/wordpress_taxonomy_ids.py` - Complete taxonomy mapping
- `shared/notion_conversion_tracker.py` - Notion integration
- `kcm-converter/kcm_prompt_ACTIVE.md` - Current AI prompt

**Questions?**
- Review existing Python code for implementation details
- Check WORK_LOG_2025-11-10.md for historical context
- Refer to N8N_YOAST_SETUP.md for current n8n configuration

---

## Appendix A: Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: KCM HTML                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: TOPIC EXTRACTION                                       │
│  • Claude API call                                              │
│  • Extract 5-15 keywords                                        │
│  • Output: ["downsizing", "equity", "market trends"]            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: NOTION CONTEXT RETRIEVAL                               │
│  • Query knowledge base database                                │
│  • Score pages by topic matches                                 │
│  • Retrieve top 5 + master doc                                  │
│  • Get full page content                                        │
│  • Output: context_text (6 docs concatenated)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: BUILD MEGA-PROMPT                                      │
│  • Load 5 guide files                                           │
│  • Concatenate: guides + context + original HTML                │
│  • Output: 50KB+ prompt                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: AI REWRITING                                           │
│  • Claude API (16,000 tokens)                                   │
│  • Localize to South Jersey                                     │
│  • Expand 1.5-2x                                                │
│  • Optimize for SEO                                             │
│  • Output: converted_html                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: HTML CLEANUP                                           │
│  • Remove em dashes                                             │
│  • Strip markdown fences                                        │
│  • Output: cleaned_html                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: SEO GENERATION                                         │
│  • Claude API call                                              │
│  • Extract title, keyphrase, description                        │
│  • Recommend categories & tags                                  │
│  • Output: seo_metadata{}                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: TAXONOMY MAPPING                                       │
│  • Map category names → WordPress IDs                           │
│  • Map tag names → WordPress IDs                                │
│  • Output: category_ids[], tag_ids[]                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 8: IMAGE PROCESSING                                       │
│  • Extract images from HTML                                     │
│  • Generate SEO filenames                                       │
│  • Generate alt text (50% with keyphrase)                       │
│  • Download from source                                         │
│  • Upload to WordPress media library                            │
│  • Update HTML with WordPress URLs                              │
│  • Remove first image (featured)                                │
│  • Output: final_html, featured_image_id                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 9: LINK REPLACEMENT                                       │
│  • Query Notion conversion database                             │
│  • Build URL mapping (full URLs)                                │
│  • Build slug mapping (simplifyingthemarket.com)                │
│  • Replace KCM links with WordPress URLs                        │
│  • Log warnings for missing links                               │
│  • Output: linked_html                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 10: WORDPRESS PUBLISHING                                  │
│  • POST /wp-json/wp/v2/posts                                    │
│  • Set title, content, slug                                     │
│  • Set categories, tags (as IDs)                                │
│  • Set featured_media                                           │
│  • Set meta[_yoast_wpseo_*] fields                              │
│  • Create as draft                                              │
│  • Output: post_id, post_url                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 11: NOTION TRACKING                                       │
│  • Create page in conversion database                           │
│  • Log KCM URL, WordPress URL, slugs                            │
│  • Log metadata, categories, tags                               │
│  • Set status = Published                                       │
│  • Output: notion_page_id                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                OUTPUT: SUCCESS                                  │
│  • WordPress Post ID: 42475                                     │
│  • WordPress URL: https://mikesellsnj.com/?p=42475              │
│  • Featured Image ID: 12345                                     │
│  • Notion Tracking ID: xyz                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Appendix B: Sample Prompts

### Topic Extraction Prompt
```
Analyze this real estate blog post and extract the key topics, themes, and concepts.
Focus on:
- Main real estate topics (e.g., "downsizing", "first-time buyers", "equity", "market trends")
- Target audience or demographics
- Seasonal or timing aspects
- Financial concepts or programs mentioned

Blog content:
{text_content}

Return a JSON array of 5-15 key topics/keywords that would be useful for finding relevant local context.
Return ONLY the JSON array, no additional text.
Example: ["downsizing", "equity", "senior homeowners", "spring selling season"]
```

### SEO Generation Prompt
```
Analyze this South Jersey real estate blog post and generate SEO metadata.

IMPORTANT: This article is from 2025. Do NOT reference old years (2023, 2024, etc.) in titles or descriptions.

ARTICLE TITLE: {article_title}

ARTICLE CONTENT (first 2000 chars):
{text_content[:2000]}

Generate the following SEO metadata in JSON format:

1. article_title: The main article title (what appears as H1)

2. categories: Array of 1-3 WordPress categories from these EXACT options:
   - Burlington County Real Estate
   - Camden County Real Estate
   - Cumberland County Real Estate
   - For Buyers
   - For Sellers
   - Gloucester County Real Estate
   - Housing Market Updates
   - Salem County Real Estate

3. tags: Array of 5-10 relevant tags (MUST use tags from approved list)

4. focus_keyphrase: The primary SEO keyword phrase (3-6 words) - should include "South Jersey" or specific town

5. seo_title: Optimized title tag (50-60 characters) including location

6. meta_description: ONLY provide if different from default. Default is: %%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%

Return ONLY valid JSON with these exact keys:
{
  "article_title": "...",
  "categories": [...],
  "tags": [...],
  "focus_keyphrase": "...",
  "seo_title": "...",
  "meta_description": "..."
}
```

---

## End of Handoff Document

**Document Version:** 1.0
**Last Updated:** 2025-02-08
**Total Pages:** 25+
**Word Count:** ~12,000 words

This document contains everything needed to rebuild the KCM Blog Converter in N8N. All business logic, API integrations, data mappings, and critical files are documented above.

Good luck with the rebuild! 🚀

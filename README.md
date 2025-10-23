# KCM Blog Converter

Automated tool to convert KeepingCurrentMatters.com blog posts into South Jersey localized content for MikeSellsNJ.com using AI-powered rewriting with Claude 3.7 Sonnet.

## Quick Start

1. **Install Python Dependencies**
   ```bash
   cd KCM-blog-converter
   pip install -r shared/requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp shared/.env.example shared/.env

   # Edit shared/.env with your API keys and configuration
   ```

3. **Start the Converter**
   ```bash
   # Windows
   start-kcm-converter.bat

   # Linux/Mac
   cd kcm-converter
   python kcm_converter_server.py
   ```

4. **Access the Web Interface**
   - The browser will automatically open to the converter interface
   - Or manually navigate to: `http://localhost:5000`

## Features

### AI-Powered Localization
- Converts generic real estate content to South Jersey specific content
- Uses Claude 3.7 Sonnet for intelligent rewriting
- Integrates with Notion knowledge base for accurate local context
- Maintains professional tone while localizing content

### Smart Content Processing
- Extracts topics from original blog posts
- Searches Notion database for relevant South Jersey information
- Generates SEO-optimized titles and meta descriptions
- Ensures 75-85 Flesch Reading Ease score for readability
- Maintains 95%+ active voice in writing

### Link Migration
- Automatically converts KCM links to MikeSellsNJ equivalents
- Preserves blog structure and formatting
- Handles internal and external links appropriately

### Image Processing
- Downloads images from original blog posts
- Generates SEO-friendly filenames based on focus keyphrase
- Creates descriptive alt text for accessibility and SEO
- Uploads images to WordPress media library
- Maintains image quality and proper formatting

### SEO Optimization
- Yoast SEO integration for WordPress
- Focus keyphrase extraction and optimization
- Meta description generation
- Alt text optimization for images
- Category and tag mapping from KCM to WordPress taxonomy

### WordPress Integration
- Direct REST API integration for draft creation
- n8n webhook support for automated publishing
- Custom taxonomy mapping (categories and tags)
- Draft post creation with all metadata

## Project Structure

```
KCM-blog-converter/
├── start-kcm-converter.bat          # Windows startup script
├── test-server.bat                   # Server health check script
├── kcm-converter/
│   ├── kcm_converter_server.py      # Main Flask application
│   └── docs/                        # Documentation files
└── shared/
    ├── requirements.txt             # Python dependencies
    ├── .env.example                 # Environment variable template
    └── .gitignore                   # Git ignore rules
```

## How It Works

### 1. Topic Extraction
The system analyzes the original KCM blog post HTML and extracts key real estate topics using Claude AI.

### 2. Knowledge Base Search
Extracted topics are used to search the Notion database for relevant South Jersey information, including:
- Local market statistics
- Town-specific information
- Regional real estate trends
- South Jersey context and references

### 3. AI Rewriting
Claude 3.7 Sonnet rewrites the blog post with:
- South Jersey localization (4-5 town mentions maximum)
- Professional, conversational tone
- Active voice (95%+ requirement)
- Improved readability (Flesch score 75-85)
- SEO optimization
- Proper HTML formatting

### 4. WordPress Publishing
The converted content is published to WordPress with:
- All images downloaded, renamed, and uploaded
- SEO metadata (title, description, focus keyphrase)
- Proper category and tag assignments
- Draft status for final review

## API Endpoints

### `POST /convert`
Convert a KCM blog post to South Jersey localized content.

**Request Body:**
```json
{
  "original_html": "<html>Blog post content...</html>"
}
```

**Response:**
```json
{
  "converted_html": "<html>Converted content...</html>",
  "original_html": "<html>Original content...</html>",
  "topics": ["Topic 1", "Topic 2"],
  "context_pages": [...],
  "images": [...],
  "seo": {
    "focus_keyphrase": "south jersey real estate",
    "seo_title": "...",
    "meta_description": "..."
  }
}
```

### `POST /process-images`
Upload images to WordPress media library.

**Request Body:**
```json
{
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "suggestedFilename": "south-jersey-real-estate-market.jpg",
      "altText": "South Jersey real estate market trends"
    }
  ]
}
```

### `POST /send-to-wordpress`
Send converted blog post to WordPress via n8n webhook.

**Request Body:**
```json
{
  "title": "Blog Post Title",
  "content": "<html>Content...</html>",
  "excerpt": "Brief excerpt...",
  "categories": [123, 456],
  "tags": [789, 101],
  "featured_media": 12345,
  "yoast_meta": {...}
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Configuration

### Environment Variables

Create a `shared/.env` file with the following variables:

```bash
# Claude API Key (get from: https://console.anthropic.com/)
CLAUDE_API_KEY=your_claude_api_key_here

# Notion API Settings (get from: https://www.notion.so/my-integrations)
NOTION_API_KEY=your_notion_integration_token_here
NOTION_DATABASE_ID=your_database_id_here

# WordPress Configuration
WORDPRESS_SITE_URL=https://mikesellsnj.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_wordpress_app_password_here
```

### WordPress Setup

1. **Install Required Plugins:**
   - Yoast SEO
   - Application Passwords plugin (or WordPress 5.6+)

2. **Create Application Password:**
   - Go to: Users → Profile → Application Passwords
   - Create new password for "KCM Converter"
   - Copy the generated password to `.env`

3. **Configure n8n Webhook:**
   - Set up n8n workflow for WordPress publishing
   - Configure webhook URL in the converter interface
   - Test webhook with sample post

### Notion Knowledge Base Setup

1. **Create Integration:**
   - Go to: https://www.notion.so/my-integrations
   - Create new integration: "KCM Converter"
   - Copy the Internal Integration Token

2. **Create Database:**
   - Create a new database in Notion
   - Add properties: Title, Content, Topics, Location
   - Share database with your integration

3. **Add Content:**
   - Populate database with South Jersey information
   - Include: town profiles, market data, local statistics
   - Tag content with relevant topics

## Conversion Guidelines

### Geographic Localization
- **Maximum 4-5 South Jersey town mentions per blog post**
- Use specific towns (e.g., Cherry Hill, Haddonfield, Moorestown)
- Avoid over-localization that seems forced
- Include broader "South Jersey" references when appropriate

### Writing Style
- **Active Voice:** 95%+ minimum
- **Tone:** Professional yet conversational
- **Readability:** Flesch Reading Ease score 75-85
- **Length:** Similar to original post length
- **Format:** Maintain HTML structure, headings, lists

### SEO Requirements
- Focus keyphrase in title, first paragraph, and throughout content
- Meta description: 150-160 characters
- Alt text for all images
- Proper heading hierarchy (H2, H3, H4)
- Internal links to relevant MikeSellsNJ.com content

### Link Migration
- Replace KCM blog links → MikeSellsNJ blog links
- Replace KCM homepage → MikeSellsNJ homepage
- Keep external authoritative links (e.g., NAR, government sites)
- Remove or replace KCM-specific resources

## Troubleshooting

### Server Won't Start
1. Check Python installation: `python --version` (requires 3.8+)
2. Verify all dependencies installed: `pip install -r shared/requirements.txt`
3. Check if port 5000 is available: `netstat -an | findstr 5000`
4. Review `.env` file configuration

### API Errors
1. **Claude API Errors:**
   - Verify `CLAUDE_API_KEY` is correct
   - Check API usage limits at console.anthropic.com
   - Ensure you're using model `claude-3-5-sonnet-20241022`

2. **Notion API Errors:**
   - Verify `NOTION_API_KEY` and `NOTION_DATABASE_ID`
   - Check database is shared with integration
   - Ensure database has required properties

3. **WordPress API Errors:**
   - Verify Application Password is correct
   - Check WordPress REST API is enabled
   - Ensure user has proper permissions
   - Verify Yoast SEO plugin is installed

### Image Upload Issues
1. Check image URLs are accessible
2. Verify WordPress media upload permissions
3. Check file size limits (WordPress default: 10MB)
4. Ensure proper image formats (JPG, PNG, WebP)

### Health Check
Run the health check script:
```bash
# Windows
test-server.bat

# Linux/Mac
curl http://localhost:5000/health
```

## Development

### Running in Development Mode
```bash
cd kcm-converter
# Set Flask environment
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

python kcm_converter_server.py
```

### Testing
```bash
# Test server health
curl http://localhost:5000/health

# Test conversion (requires full request body)
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"original_html": "..."}'
```

## Technical Stack

- **Backend:** Python 3.8+ with Flask
- **AI:** Anthropic Claude 3.7 Sonnet
- **Knowledge Base:** Notion API
- **CMS:** WordPress REST API
- **Automation:** n8n workflows
- **Frontend:** HTML/CSS/JavaScript (web interface)

## License

Proprietary - Internal tool for MikeSellsNJ.com

## Support

For issues or questions, contact the development team.

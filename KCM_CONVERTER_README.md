# KCM Blog Converter for South Jersey

Converts KeepingCurrentMatters.com (KCM) blogs to South Jersey localized content with AI-powered rewriting.

## Features

✅ **AI-Powered Localization**
- Uses Claude 3.7 Sonnet to rewrite national content for South Jersey markets
- Pulls context from your Notion knowledge base automatically
- Intelligently extracts topics and finds relevant local information

✅ **Smart Content Processing**
- **No Keyword Stuffing**: Town names mentioned max 1-2 times each
- **No Em Dashes**: Automatically removes all em dashes (—)
- **Stays On Topic**: No irrelevant additions (attorney review, transfer taxes, etc.)
- **Preserves Links**: All existing internal links maintained exactly

✅ **Automatic Link Migration**
- Converts KCM links to MSNJ format
- From: `https://www.simplifyingthemarket.com/en/2025/09/24/[slug]/?a=211199-...`
- To: `https://mikesellsnj.com/[slug]/`
- Strips tracking parameters automatically

✅ **Image URL Conversion**
- Converts to WordPress structure: `/wp-content/uploads/YYYY/MM/filename.png`
- Uses current year and month automatically

✅ **Modern Web Interface**
- Paste HTML directly in browser
- Real-time conversion with progress indicator
- Preview converted content
- Download HTML file or copy to clipboard

## Quick Start

### 1. Start the Server

```bash
py kcm_converter_server.py
```

You should see:
```
Starting KCM Blog Converter Server...
Server will run on http://localhost:5000
Open clipboard.html in your browser to use the converter
```

### 2. Open the Web Interface

Open `clipboard.html` in your web browser (double-click the file or drag into browser)

### 3. Convert a Blog

1. Copy the HTML from a KCM blog post
2. Paste it into the "Paste Original HTML" box
3. Click "🚀 Convert to South Jersey"
4. Wait 30-60 seconds for AI processing
5. Review the converted HTML and preview
6. Download or copy to clipboard

## How It Works

### Step 1: Topic Extraction
Claude analyzes the original blog and extracts key topics/themes

### Step 2: Context Retrieval
The system searches your Notion database for relevant documents:
- Always includes "South Jersey Real Estate Context Guide" (master doc)
- Finds top 5 most relevant additional documents based on topic matches

### Step 3: AI Rewriting
Claude rewrites the blog with strict instructions:
- Localizes to specific South Jersey towns
- Limits keyword usage (no stuffing)
- Removes em dashes
- Stays on topic (no tangential additions)
- Preserves all existing links
- Expands content 1.5-2x with meaningful local detail

### Step 4: Post-Processing
- Removes any remaining em dashes
- Migrates KCM links to MSNJ format
- Converts image URLs to WordPress structure

## Configuration

The converter uses your existing `.env` file:

```env
CLAUDE_API_KEY=your_claude_api_key
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id
```

## Notion Knowledge Base Setup

The converter expects these documents in your Notion database:

**Required:**
- A document titled "South Jersey Real Estate Context Guide" (master reference)

**Optional:**
- Any number of additional documents with relevant local content
- Documents should have "Keywords / Tags" field for better matching

## Output Format

The converted blog will:
- Be valid HTML ready for WordPress
- Have all links migrated to MSNJ format
- Have all images using WordPress URL structure
- Be free of em dashes
- Mention towns naturally (1-2 times each max)
- Include only relevant content (no tangential topics)
- Be 1.5-2x longer than original with local details

## Troubleshooting

### "Make sure the Python server is running"
- Ensure you ran `py kcm_converter_server.py`
- Check that you see "Running on http://0.0.0.0:5000"

### "No relevant context found in Notion database"
- Verify your `NOTION_DATABASE_ID` is correct in `.env`
- Check that you have a document named "South Jersey Real Estate Context Guide"
- Ensure the Notion integration has access to the database

### "Server error: 500"
- Check the Python server terminal for error messages
- Verify all API keys in `.env` are correct
- Make sure Claude 3.7 Sonnet is available to your API key

### Conversion Takes Too Long
- Normal conversion time is 30-60 seconds
- Large documents may take longer
- Check your Claude API rate limits

## API Costs

- **Claude 3.7 Sonnet**: ~$0.01-0.03 per conversion (varies by length)
- **Notion API**: Free (unlimited requests)

## Advanced Usage

### Command Line (Original Method)

You can still use the original blog_rewriter.py:

```bash
# Review mode (shows context before converting)
py blog_rewriter.py input.html

# Auto mode (converts immediately)
py blog_rewriter.py input.html --auto
```

### Customizing the Prompt

Edit `kcm_converter_server.py` and modify the prompt in the `rewrite_blog_post()` function to adjust:
- Town mention limits
- Content expansion ratio
- Tone and style
- Additional instructions

## Files

- `clipboard.html` - Web interface for conversions
- `kcm_converter_server.py` - Flask server backend
- `blog_rewriter.py` - Original CLI tool
- `sync_drive_to_notion.py` - Google Drive sync tool

## Tips for Best Results

1. **Feed the Knowledge Base**: Add more South Jersey-specific documents to Notion
2. **Use Keywords**: Tag Notion documents with relevant keywords for better matching
3. **Review Output**: Always review the converted content before publishing
4. **Test Links**: Verify migrated links work correctly
5. **Check Images**: Ensure image filenames are appropriate before uploading to WordPress

## Support

If you encounter issues:
1. Check the server terminal for detailed error messages
2. Review the `blog_rewriter_log.log` file
3. Verify all API credentials are correct
4. Ensure your Notion database structure matches expectations

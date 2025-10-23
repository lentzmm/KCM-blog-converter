# South Jersey Blog Rewriter Tool

Automatically localizes national real estate blog posts for South Jersey markets using your Notion knowledge base and Claude AI.

## Features

- **Intelligent Topic Extraction**: Automatically identifies key topics from the original blog
- **Smart Context Retrieval**: Searches your Notion database for relevant South Jersey content
- **Always Uses Master Doc**: Includes "South Jersey Real Estate Context Guide" in every rewrite
- **Two Modes**: Review mode (see context first) or Auto mode (just run it)
- **Comprehensive Localization**: Replaces generic content with specific South Jersey details
- **HTML Preservation**: Maintains WordPress-compatible formatting

## Installation

All dependencies are already installed from the sync project. No additional setup needed!

## Usage

### Review Mode (Recommended for first use)

```bash
python blog_rewriter.py input_blog.html
```

This will:
1. Extract topics from the blog
2. Search your Notion database
3. Show you what documents it found
4. Ask if you want to proceed
5. Generate the localized version

### Auto Mode (Fast)

```bash
python blog_rewriter.py input_blog.html --auto
```

This will automatically generate the localized version without stopping for review.

## Input Format

The input file should be HTML format. Example:

```html
<h1>5 Reasons to Downsize Your Home</h1>
<p>If you're thinking about moving to a smaller home...</p>
```

You can:
- Copy/paste blog HTML into a `.html` file
- Save directly from your source
- Use any text editor to create the input file

## Output

The tool generates a timestamped HTML file:
- Format: `rewritten_blog_YYYYMMDD_HHMMSS.html`
- Ready to paste into WordPress
- Fully localized with South Jersey details
- Typically 2-3x longer than the original

## What Gets Localized

### Geographic References
- Generic locations → Specific South Jersey towns
- States/regions → Gloucester, Camden, Burlington, Salem, Cumberland counties
- Adds proximity details (Philadelphia, Jersey Shore, highways)

### Financial Details
- National price ranges → South Jersey actuals ($300K-$600K typical)
- Generic programs → NJ-specific (Senior Freeze, NJHMFA, attorney review)
- Generic closing info → NJ-specific details

### Market Context
- Adds local market dynamics
- References housing diversity
- Includes market stability information
- Uses concrete local examples

### Content Expansion
- Each section expanded with local details
- Adds specific examples and scenarios
- Includes relevant local programs
- Maintains no-nonsense, analytical tone

## Examples

### Before (Generic):
```html
<p>Many homeowners in California and Florida are discovering that
downsizing can unlock equity...</p>
```

### After (Localized):
```html
<p>Many homeowners in Haddonfield, Moorestown, and Cherry Hill are
discovering that downsizing from their 4-bedroom colonial to a more
manageable ranch or townhome can unlock significant equity. In Gloucester
County's Washington Township, for example, a homeowner selling a
$550,000 home and moving to a $375,000 ranch can free up substantial
funds while staying in the same excellent school district, just 20
minutes from Philadelphia...</p>
```

## How It Works

1. **Topic Extraction**: Claude analyzes the original post and identifies key topics
2. **Database Search**: Searches your Notion "Knowledge Bank (MLT)" for relevant content
3. **Master Doc Inclusion**: Always retrieves "South Jersey Real Estate Context Guide"
4. **Relevance Scoring**: Ranks other documents by keyword matches
5. **Context Assembly**: Gathers full content from top 5-6 relevant pages
6. **AI Rewriting**: Claude rewrites using comprehensive localization instructions
7. **Output Generation**: Saves HTML file ready for WordPress

## Logging

All operations are logged to `blog_rewriter_log.log` including:
- Topics extracted
- Documents found and used
- API calls
- Success/failure status
- Timestamps

## Tips for Best Results

1. **Use Review Mode First**: See what context is being used
2. **Check Master Doc**: Ensure "South Jersey Real Estate Context Guide" is in your database
3. **Add More Context**: The more relevant docs in your Notion database, the better
4. **Use Descriptive Titles**: Notion document titles help with relevance matching
5. **Tag Documents**: Use Keywords/Tags in Notion to improve search

## Configuration

Uses the same `.env` file as the sync script:
```
CLAUDE_API_KEY=your_key_here
NOTION_API_KEY=your_key_here
NOTION_DATABASE_ID=your_database_id
```

## Troubleshooting

### No relevant documents found
- Check that your Notion database has content
- Verify the master doc name matches exactly
- Try running the sync script first to populate the database

### Authentication failed
- Verify your `.env` file is in the same directory
- Check that all API keys are valid
- Ensure Notion integration has access to the database

### Output seems generic
- Check that context documents were actually retrieved (see log)
- Verify the master doc has comprehensive content
- Review mode will show you what context is being used

### HTML formatting issues
- Input file should be valid HTML
- WordPress-compatible tags work best
- Check output file for proper tag closure

## Technical Details

- **Language**: Python 3
- **APIs Used**: Notion API, Anthropic Claude API
- **Model**: Claude 3.7 Sonnet
- **Max Output**: ~16K tokens (very long blog posts)
- **Context Limit**: Top 5-6 most relevant documents

## File Outputs

- `rewritten_blog_YYYYMMDD_HHMMSS.html` - Localized blog post
- `blog_rewriter_log.log` - Detailed operation log

## Support

Check the log file for detailed error messages. Common issues:
- Missing API credentials → Check `.env` file
- Empty output → Check that Notion pages have content
- Authentication errors → Verify API keys are valid

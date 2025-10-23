# Quick Start Guide - Blog Rewriter

## Test It Right Now

I've included a sample blog post so you can test the tool immediately:

```bash
cd "C:\Users\lentz\Dropbox\ClaudeCode\KnowledgeBaseSync"
python blog_rewriter.py sample_blog.html
```

This will run in **review mode** so you can see:
- What topics it extracts from the blog
- What documents it finds in your Notion database
- A chance to approve before it rewrites

## Expected Flow

### Review Mode
```
1. Tool extracts topics: "downsizing", "equity", "empty nesters", etc.
2. Searches your Notion database
3. Shows you found documents:
   • South Jersey Real Estate Context Guide [MASTER DOCUMENT]
   • (other relevant docs if found)
4. Asks: "Proceed with rewriting? (yes/no)"
5. You type: yes
6. Claude rewrites the blog with South Jersey details
7. Saves to: rewritten_blog_YYYYMMDD_HHMMSS.html
```

### What You'll See in the Output

The generic blog about downsizing will become:

**Before:**
> "Many homeowners are discovering that downsizing can unlock equity..."

**After:**
> "Many homeowners in Haddonfield, Moorestown, and Cherry Hill are discovering that downsizing from their 4-bedroom colonial to a more manageable ranch or townhome can unlock significant equity. In Gloucester County's Washington Township, for example, a homeowner selling a $550,000 home and moving to a $375,000 ranch..."

The output will be:
- ✓ 2-3x longer with local details
- ✓ All generic locations replaced with South Jersey towns
- ✓ Specific price ranges ($300K-$600K)
- ✓ References to local programs (Senior Freeze, etc.)
- ✓ Proximity mentions (Philadelphia, Jersey Shore)
- ✓ County-specific examples
- ✓ Ready to paste into WordPress

## Try Auto Mode

Once you're comfortable with how it works:

```bash
python blog_rewriter.py sample_blog.html --auto
```

This skips the review step and just generates the output.

## Use Your Own Blog Posts

1. Copy the blog HTML from your source
2. Save to a file (e.g., `my_blog.html`)
3. Run: `python blog_rewriter.py my_blog.html`

## Common First-Time Issues

### "No relevant documents found"
**Solution**: Your Notion database might be empty or the master doc is missing.

Run the sync script first:
```bash
python sync_drive_to_notion.py
```

This will populate your Notion database with content from Google Drive.

### "Authentication failed"
**Solution**: Check your `.env` file exists and has valid API keys:
```
CLAUDE_API_KEY=sk-ant-...
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...
```

### Output is too generic
**Solution**: The tool needs more context. Check:
1. Is "South Jersey Real Estate Context Guide" in your Notion database?
2. Does it have actual content (not just a summary)?
3. Run in review mode to see what context it found

## Next Steps

1. **Test with sample**: `python blog_rewriter.py sample_blog.html`
2. **Review the output**: Open the generated HTML file
3. **Try your own content**: Save a blog post and run the tool
4. **Build your knowledge base**: Add more docs to Notion for better results

## Need Help?

Check these files:
- `BLOG_REWRITER_README.md` - Full documentation
- `blog_rewriter_log.log` - Detailed operation log
- See what went wrong in each step

## Pro Tips

✓ **Keep your context docs updated**: The better your Notion content, the better the rewrites

✓ **Use descriptive titles**: Help the tool find relevant content by using clear document titles in Notion

✓ **Tag your docs**: Add keywords/tags in Notion to improve search relevance

✓ **Review mode first**: Always use review mode when trying a new blog topic to see what context is being used

✓ **Build a workflow**:
   1. Receive generic blog
   2. Save as HTML
   3. Run rewriter in review mode
   4. Check output
   5. Paste into WordPress
   6. Quick edit for final polish

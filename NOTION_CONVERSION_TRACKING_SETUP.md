# Notion Conversion Tracking Setup

This guide explains how to set up the Notion database for tracking converted blog posts and automatically replacing KCM internal links with WordPress links.

---

## What This Does

1. **Tracks Every Conversion**: Creates a database record for each KCM article you convert
2. **Replaces Internal Links**: Automatically updates KCM links to point to your WordPress articles
3. **Prevents Broken Links**: Warns you when a post links to articles you haven't converted yet
4. **Provides Analytics**: See all your conversions in one place with filters and views

---

## Setup Steps (5 Minutes)

### Step 1: Create the Notion Database

1. Go to your Notion workspace
2. Click **"+ New page"**
3. Name it: **"Blog Post Conversions"**
4. Click **"Table"** to create a database

### Step 2: Add Database Properties

Click **"+ New property"** for each of these:

| Property Name | Type | Notes |
|---------------|------|-------|
| Article Title | Title | (Already exists - rename it) |
| KCM URL | URL | Original KCM article link |
| KCM Slug | Text | e.g. "homebuyer-tips-2024" |
| WordPress URL | URL | Your new WordPress article link |
| WordPress Slug | Text | e.g. "south-jersey-buyers-guide" |
| WordPress Post ID | Number | WordPress post ID |
| Focus Keyphrase | Text | SEO keyphrase used |
| Converted Date | Date | When you converted it |
| Categories | Multi-select | WordPress categories |
| Tags | Multi-select | WordPress tags |
| SEO Title | Text | The SEO title |
| Meta Description | Text | The meta description |
| Internal Links Count | Number | How many KCM links were in the article |
| Status | Select | Published, Draft, or Failed |

### Step 3: Configure Status Options

1. Click the **"Status"** property
2. Add these three options:
   - **Published** (green)
   - **Draft** (yellow)
   - **Failed** (red)

### Step 4: Share Database with Your Integration

1. Click **"Share"** (top right of the database page)
2. Click **"Invite"**
3. Select your Notion integration (the same one you used for context documents)
4. Click **"Invite"**

### Step 5: Copy the Database ID

1. Look at the URL of your database page
2. It looks like: `https://www.notion.so/workspace/DATABASE_ID?v=...`
3. Copy the **DATABASE_ID** part (it's a long string of letters and numbers)
4. Remove any hyphens from it

Example:
- URL: `https://www.notion.so/mike/1a2b-3c4d-5e6f?v=123`
- Database ID: `1a2b3c4d5e6f`

### Step 6: Add to Environment Variables

1. Open `shared/.env` file in your project
2. Find the line: `NOTION_CONVERSION_DB_ID=your_conversion_tracking_database_id_here`
3. Replace with your database ID:
   ```
   NOTION_CONVERSION_DB_ID=1a2b3c4d5e6f
   ```
4. Save the file

### Step 7: Restart Your Server

1. Stop the server (Ctrl+C)
2. Start it again with `start-kcm-converter-CLEAN.bat`

---

## How It Works

### During Conversion

When you click "Convert":
1. Server queries your Notion database for all converted posts
2. Looks for any KCM internal links in the article
3. Replaces them with WordPress URLs (if found in database)
4. Shows warnings for links that haven't been converted yet

**Check the black server window** to see:
```
✅ Replaced 3 KCM links with WordPress URLs
⚠️  2 KCM links not yet converted:
   - https://www.keepingcurrentmatters.com/article-1
   - https://www.keepingcurrentmatters.com/article-2
```

### After WordPress Upload

When you click "Send to WordPress":
1. Article is published to WordPress (as draft)
2. Server automatically adds a new row to your Notion database
3. Includes all metadata: title, URLs, categories, tags, etc.

---

## Viewing Your Conversions

### Table View
See all conversions in a spreadsheet format

### Filters You Can Create
- Show only published posts
- Show posts with broken links (Internal Links Count > 0 and not all replaced)
- Show posts from this month
- Show posts by category

### Example Filters

**"Posts that need link updates":**
```
Internal Links Count > 0
```

**"Recently converted":**
```
Converted Date is within last 7 days
```

**"Buyer-focused content":**
```
Categories contains "For Buyers"
```

---

## Troubleshooting

### "No URL mapping provided - skipping link replacement"

**Cause:** `NOTION_CONVERSION_DB_ID` not set in `.env`

**Fix:**
1. Make sure you added the database ID to `shared/.env`
2. Restart the server
3. Check server logs - should NOT see this warning

### "Failed to load URL mappings from Notion"

**Cause:** Database not shared with integration, or database ID is wrong

**Fix:**
1. Check that you shared the database with your Notion integration
2. Verify the database ID in `.env` is correct
3. Make sure there are no spaces or hyphens in the database ID

### Conversion tracking isn't working

**Symptoms:** No new rows appear in Notion after WordPress upload

**Check:**
1. Look for "Missing KCM URL or WordPress details" in server logs
2. Make sure all database properties are named exactly as listed above
3. Check that Status property has "Published" option (case-sensitive)

### Link replacement isn't working

**Check:**
1. Make sure you have at least one "Published" post in the database
2. URLs in database must match exactly (including https://)
3. Check server logs for "Replaced N KCM links" message

---

## Optional: Create Useful Views

### Timeline View
1. Click "+ Add a view"
2. Select "Timeline"
3. Use "Converted Date" as the timeline property
4. See conversions over time

### Gallery View
1. Click "+ Add a view"
2. Select "Gallery"
3. Preview each conversion as a card

---

## Benefits

✅ **Never lose track** of what you've converted
✅ **No broken internal links** - automatic replacement
✅ **SEO boost** - keeps link equity flowing to your WordPress site
✅ **Analytics ready** - export to CSV for reporting
✅ **Team visibility** - share database with others if needed

---

## Notes

- This is **completely optional** - converter works without it
- Database only tracks posts you convert going forward
- You can manually add old conversions to "catch up"
- The database is queryable with Notion API for future automation

---

## Next Steps

After setup:
1. Convert a test article
2. Check server logs for link replacement messages
3. Verify new row appears in Notion database
4. Check that WordPress article has correct internal links

Need help? Look for these messages in the server window:
- ✅ "Conversion tracked in Notion"
- ✅ "Replaced N KCM links"
- ⚠️ "N KCM links not yet converted" (this is normal for new conversions)

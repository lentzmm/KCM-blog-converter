# QUICK FIX: Add Featured Image Support to n8n Workflow

## Problem
Featured image is not being set when posts are created in WordPress.

## Root Cause
The n8n "Post" HTTP Request node is missing the `featured_media` parameter, so it's not forwarding the image ID to WordPress.

## Solution (2 minutes)

### Step 1: Open Your n8n Workflow
1. Go to your n8n instance
2. Open the "WordPress Blog Automation" workflow

### Step 2: Edit the "Post" Node
1. Click on the **"Post"** node (the HTTP Request node that creates the WordPress post)
2. Scroll down to **"Body Parameters"** section

### Step 3: Add the Featured Media Parameter
1. Click **"Add Parameter"** (at the bottom of the body parameters list)
2. Fill in the new parameter:
   - **Name:** `featured_media`
   - **Value:** `={{ $('Webhook').item.json.body.body.featured_media }}`

### Step 4: Save and Test
1. Click **"Execute Node"** to test
2. Click **"Save"** to save the workflow
3. Run a test conversion from Python

## Complete Body Parameters List

After adding the parameter, your "Post" node should have these 10 body parameters:

1. ✅ `title` → `={{ $('Webhook').item.json.body.body.title }}`
2. ✅ `content` → `={{ $('Webhook').item.json.body.body.content }}`
3. ✅ `slug` → `={{ $('Webhook').item.json.body.body.slug }}`
4. ✅ `excerpt` → `={{ $('Webhook').item.json.body.body.excerpt }}`
5. ✅ `status` → `draft` (hardcoded)
6. ✅ `categories` → `={{ $('Webhook').item.json.body.body.categories }}`
7. ✅ `tags` → `={{ $('Webhook').item.json.body.body.tags }}`
8. ✅ `featured_media` → `={{ $('Webhook').item.json.body.body.featured_media }}` **← ADD THIS**
9. ✅ `meta[_yoast_wpseo_metadesc]` → `={{ $('Webhook').item.json.body.body.yoast_meta_description }}`
10. ✅ `meta[_yoast_wpseo_focuskw]` → `={{ $('Webhook').item.json.body.body.yoast_focus_keyword }}`

## Optional: Add SEO Title
If you also want to set the Yoast SEO Title field, add this 11th parameter:

11. ⭐ `meta[_yoast_wpseo_title]` → `={{ $('Webhook').item.json.body.body.yoast_seo_title }}`

## Verification

After adding the parameter, test a conversion and check:

1. **Python logs** should show:
   ```
   Featured Media ID: 12345
   ```

2. **WordPress post** should display the featured image

3. **WordPress REST API response** should show:
   ```json
   {
     "id": 42475,
     "featured_media": 12345  // ← Should NOT be 0
   }
   ```

## Why This Was Missing

The Python code has **always been sending** the `featured_media` field:

```python
payload = {
    'featured_media': 12345,  # ← Python sends this
    # ... other fields
}
```

But your n8n workflow wasn't configured to forward it to WordPress. Now it will!

## Data Flow (After Fix)

```
┌──────────────────┐
│ Python           │
│ featured_media:  │ ──┐
│ 12345            │   │
└──────────────────┘   │
                       │
                       ▼
┌──────────────────────────────────────────┐
│ n8n Webhook                              │
│ $('Webhook').item.json.body.body.        │
│   featured_media = 12345                 │
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│ n8n HTTP Request "Post" Node             │
│ Body Parameter:                          │
│   featured_media = 12345                 │ **← YOU ARE HERE**
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│ WordPress REST API                       │
│ POST /wp-json/wp/v2/posts                │
│ {                                        │
│   "featured_media": 12345                │
│ }                                        │
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│ WordPress                                │
│ Post created with featured image ✅      │
└──────────────────────────────────────────┘
```

## That's It!

Just add the one parameter to n8n and your featured images will start working! 🎉

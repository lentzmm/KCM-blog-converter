# n8n Workflow Configuration for WordPress Posts

## Current n8n HTTP Request Node Configuration (v2.1)

Your n8n "Post" node should have these body parameters:

### Core WordPress Parameters (Required)

```javascript
// Title
{
  "name": "title",
  "value": "={{ $('Webhook').item.json.body.body.title }}"
}

// Slug
{
  "name": "slug",
  "value": "={{ $('Webhook').item.json.body.body.slug }}"
}

// Content
{
  "name": "content",
  "value": "={{ $('Webhook').item.json.body.body.content }}"
}

// Excerpt
{
  "name": "excerpt",
  "value": "={{ $('Webhook').item.json.body.body.excerpt }}"
}

// Status (hardcoded to draft)
{
  "name": "status",
  "value": "draft"
}

// Categories (array of IDs)
{
  "name": "categories",
  "value": "={{ $('Webhook').item.json.body.body.categories }}"
}

// Tags (array of IDs)
{
  "name": "tags",
  "value": "={{ $('Webhook').item.json.body.body.tags }}"
}

// Featured Image (media ID)
{
  "name": "featured_media",
  "value": "={{ $('Webhook').item.json.body.body.featured_media }}"
}
```

### Yoast SEO Parameters (Required for SEO)

```javascript
// Focus Keyword
{
  "name": "meta[_yoast_wpseo_focuskw]",
  "value": "={{ $('Webhook').item.json.body.body.yoast_focus_keyword }}"
}

// Meta Description
{
  "name": "meta[_yoast_wpseo_metadesc]",
  "value": "={{ $('Webhook').item.json.body.body.yoast_meta_description }}"
}

// SEO Title (optional but recommended)
{
  "name": "meta[_yoast_wpseo_title]",
  "value": "={{ $('Webhook').item.json.body.body.yoast_seo_title }}"
}
```

## Data Flow

1. **Python script** sends to n8n webhook:
   ```json
   {
     "body": {
       "title": "Why Home Prices Are Rising in 2025",
       "slug": "why-home-prices-are-rising-in-2025",
       "content": "<p>Full article content...</p>",
       "excerpt": "Short excerpt...",
       "categories": [123, 456],
       "tags": [789, 101],
       "featured_media": 12345,
       "yoast_focus_keyword": "real estate tips",
       "yoast_meta_description": "Learn about...",
       "yoast_seo_title": "SEO Title Here"
     }
   }
   ```

2. **n8n** receives this data and transforms it for WordPress REST API:
   ```
   POST https://yoursite.com/wp-json/wp/v2/posts
   Body Parameters:
     - meta[_yoast_wpseo_focuskw]: "real estate tips"
     - meta[_yoast_wpseo_metadesc]: "Learn about..."
     - meta[_yoast_wpseo_title]: "SEO Title Here"
   ```

3. **WordPress** receives this and parses it as:
   ```json
   {
     "meta": {
       "_yoast_wpseo_focuskw": "real estate tips",
       "_yoast_wpseo_metadesc": "Learn about...",
       "_yoast_wpseo_title": "SEO Title Here"
     }
   }
   ```

4. **WordPress plugin** (Yoast REST API Support v2.1) intercepts the `meta` parameter and updates the Yoast fields.

## Field Name Mapping

### Core WordPress Fields
| Python Field Name | n8n Expression | WordPress Field |
|------------------|----------------|----------------|
| `title` | `body.body.title` | `title` |
| `slug` | `body.body.slug` | `slug` |
| `content` | `body.body.content` | `content` |
| `excerpt` | `body.body.excerpt` | `excerpt` |
| `categories` | `body.body.categories` | `categories` (array of IDs) |
| `tags` | `body.body.tags` | `tags` (array of IDs) |
| `featured_media` | `body.body.featured_media` | `featured_media` (media ID) |

### Yoast SEO Fields
| Python Field Name | n8n Expression | WordPress Meta Key |
|------------------|----------------|-------------------|
| `yoast_focus_keyword` | `body.body.yoast_focus_keyword` | `_yoast_wpseo_focuskw` |
| `yoast_meta_description` | `body.body.yoast_meta_description` | `_yoast_wpseo_metadesc` |
| `yoast_seo_title` | `body.body.yoast_seo_title` | `_yoast_wpseo_title` |

### Slug Auto-Generation
If no slug is provided, Python automatically generates a URL-friendly slug from the title:
- "Why Home Prices Are Rising!" → "why-home-prices-are-rising"
- "First-Time Home Buyer's Guide" → "first-time-home-buyer-s-guide"

## Troubleshooting

### n8n shows "undefined" for fields?

**Common undefined fields:**
- `{{$('Webhook').item.json.body.body.slug}}`
- `{{$('Webhook').item.json.body.body.yoast_focus_keyword}}`
- `{{$('Webhook').item.json.body.body.yoast_meta_description}}`

**Solution:** Check that Python script is sending the correct field names (see Field Name Mapping above).

1. **Check Python logs** - Verify the payload contains all fields:
   ```
   Title: Why Home Prices Are Rising
   Slug: why-home-prices-are-rising
   🔍 YOAST FIELDS (v2.1 - N8N FORMAT):
     - yoast_focus_keyword: real estate tips
     - yoast_meta_description: Learn about...
     - yoast_seo_title: SEO optimized title
   ```

2. **Check n8n webhook data** - In n8n, click on the Webhook node and check "Test URL" to see what data is being received

### Yoast fields not being set in WordPress?

1. **Check n8n expressions** - Make sure n8n "Post" node has the body parameters configured correctly

2. **Check WordPress plugin** - Ensure `wordpress-yoast-rest-api.php` v2.1 is active in WordPress

3. **Check WordPress logs** - Look for these messages in error logs:
   ```
   Yoast REST API (meta interceptor): Updated _yoast_wpseo_focuskw for post 12345
   ```

### Featured image not being set?

**Symptoms:** Post is created but `featured_media` returns 0 or is missing

**Common Causes:**

1. **Missing n8n parameter** - n8n is not forwarding the featured_media field to WordPress

   **Solution:** Add this parameter to your n8n "Post" node:
   ```javascript
   {
     "name": "featured_media",
     "value": "={{ $('Webhook').item.json.body.body.featured_media }}"
   }
   ```

2. **Image not uploaded** - Python didn't upload the image before creating the post

   **Solution:** Check Python logs for:
   ```
   Featured Media ID: 12345
   ```
   If it shows `Featured Media ID: None`, the image upload failed.

3. **WordPress permission issue** - WordPress can't read the attachment

   **Solution:** The v2.1 plugin includes a fix for this. Ensure the plugin is active.

4. **Invalid media ID** - The featured_media ID doesn't exist in WordPress

   **Solution:** Check that the image was successfully uploaded and the ID is valid.

## WordPress Plugin Requirements

The WordPress plugin `wordpress-yoast-rest-api.php` (v2.1) must be:
- Installed in `wp-content/plugins/` directory
- Activated in WordPress Admin → Plugins
- Version 2.1 or higher (supports both meta object and top-level field formats)

## Version History

- **v2.1**: Added n8n HTTP Request node support via `rest_insert_post` action hook
- **v2.0**: Attempted to use `register_rest_field()` with top-level fields (didn't work with n8n)
- **v1.0**: Used `register_post_meta()` (failed due to WordPress private meta restrictions)

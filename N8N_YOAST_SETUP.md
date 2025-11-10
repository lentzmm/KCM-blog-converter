# n8n Workflow Configuration for Yoast SEO Fields

## Current n8n HTTP Request Node Configuration (v2.1)

Your n8n "Post" node should have these body parameters to send Yoast SEO fields to WordPress:

### Required Parameters (Already Configured)

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
```

### Optional Parameter (Add if you want SEO Title support)

```javascript
// SEO Title
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
       "title": "...",
       "content": "...",
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

| Python Field Name | n8n Expression | WordPress Meta Key |
|------------------|----------------|-------------------|
| `yoast_focus_keyword` | `body.body.yoast_focus_keyword` | `_yoast_wpseo_focuskw` |
| `yoast_meta_description` | `body.body.yoast_meta_description` | `_yoast_wpseo_metadesc` |
| `yoast_seo_title` | `body.body.yoast_seo_title` | `_yoast_wpseo_title` |

## Troubleshooting

### Yoast fields not being set?

1. **Check Python logs** - Verify the payload contains the Yoast fields:
   ```
   🔍 YOAST FIELDS (v2.1 - N8N FORMAT):
     - yoast_focus_keyword: real estate tips
     - yoast_meta_description: Learn about...
   ```

2. **Check n8n expressions** - Make sure n8n "Post" node has the body parameters configured correctly

3. **Check WordPress plugin** - Ensure `wordpress-yoast-rest-api.php` v2.1 is active in WordPress

4. **Check WordPress logs** - Look for these messages in error logs:
   ```
   Yoast REST API (meta interceptor): Updated _yoast_wpseo_focuskw for post 12345
   ```

## WordPress Plugin Requirements

The WordPress plugin `wordpress-yoast-rest-api.php` (v2.1) must be:
- Installed in `wp-content/plugins/` directory
- Activated in WordPress Admin → Plugins
- Version 2.1 or higher (supports both meta object and top-level field formats)

## Version History

- **v2.1**: Added n8n HTTP Request node support via `rest_insert_post` action hook
- **v2.0**: Attempted to use `register_rest_field()` with top-level fields (didn't work with n8n)
- **v1.0**: Used `register_post_meta()` (failed due to WordPress private meta restrictions)

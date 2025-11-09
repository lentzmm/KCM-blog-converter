# Critical Issues Analysis and Required Fixes

**Date:** 2025-11-09
**Status:** RESEARCH COMPLETE - WordPress Configuration Required

---

## ROOT CAUSE IDENTIFIED

After deep research, I've identified the core problem: **WordPress is NOT configured to accept Yoast meta fields via REST API**.

---

## Issue 1: Focus Keyphrase Not Set ❌

### Root Cause
Yoast SEO fields are **NOT exposed via WordPress REST API by default** - not even with Yoast Premium. The REST API ignores any Yoast meta fields sent in the payload unless you explicitly register them.

### Evidence
- WordPress REST API response shows `"meta": {}` without Yoast fields
- Research confirms: "in 2025 yoast field can't be editing via the API" without custom code
- GitHub plugin `wp-api-yoast-meta` exists specifically to solve this problem

### Required Fix (WordPress Side)
You must add this code to your WordPress `functions.php` or create a custom plugin:

```php
add_action('rest_api_init', function() {
    // Register Yoast SEO fields for REST API access
    $yoast_fields = array(
        '_yoast_wpseo_focuskw',      // Focus keyphrase
        '_yoast_wpseo_title',         // SEO title
        '_yoast_wpseo_metadesc'       // Meta description
    );

    foreach ($yoast_fields as $field) {
        register_post_meta('post', $field, array(
            'show_in_rest' => true,
            'single' => true,
            'type' => 'string',
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ));
    }
});
```

**OR** install this plugin: https://github.com/ChazUK/wp-api-yoast-meta

### Current Payload Format
We're currently sending:
```json
{
  "meta": {
    "_yoast_wpseo_focuskw": "South Jersey home equity",
    "_yoast_wpseo_metadesc": "...",
    "_yoast_wpseo_title": "..."
  }
}
```

**This is correct** but WordPress ignores it without the code above.

---

## Issue 2: Meta Description Not Set ❌

### Root Cause
Same as Issue 1 - WordPress doesn't expose Yoast fields via REST API.

### Required Fix
Same WordPress configuration as Issue 1.

---

## Issue 3: Featured Image Not Set ❌

### Possible Causes (Need User Verification)

1. **Media ID doesn't exist**
   - Verify the image was successfully uploaded to WordPress
   - Check the media ID returned from `/process-images` endpoint

2. **Permission issue**
   - WordPress user needs `edit_posts` capability
   - Check if HTTP Basic Auth user has proper permissions

3. **Cache issue**
   - WordPress caching plugin might be interfering
   - Try clearing WordPress cache

4. **Media belongs to different user**
   - Media must be owned by or accessible to the API user

### Debugging Steps
1. Check server logs for: `"Featured Media ID: XXXXX"`
2. Verify that ID exists in WordPress Media Library
3. Try manually setting featured image on a test post via WordPress admin
4. Check if N8N is actually sending the `featured_media` field to WordPress

### Current Code
```python
if featured_media_id:
    payload['featured_media'] = featured_media_id  # Sent as integer
```

This is **correct format** according to WordPress REST API docs.

---

## Issue 4: Notion Links Count - FIXED ✅

### What Was Wrong
The `/send-to-wordpress` endpoint was trying to extract KCM links from HTML that had already been converted (links already replaced), finding 0 links.

### Fix Applied
- Store `link_stats` globally when `/convert` runs
- Use stored stats in `/send-to-wordpress`
- Count = replaced + not_found links

### Status
FIXED in commit `6dc3099`

---

## Issue 5: Notion KCM Slug Incorrect ❌

### Current Behavior
```python
kcm_slug = urlparse(kcm_url).path.rstrip('/')
# Result: /en/2025/09/24/do-you-know-how-much-your-house-is-really-worth
```

### Expected Behavior
You probably want just the slug part:
```
do-you-know-how-much-your-house-is-really-worth
```

### Required Fix
```python
kcm_slug = urlparse(kcm_url).path.rstrip('/').split('/')[-1] if kcm_url else ''
```

This extracts only the last segment of the path.

---

## REQUIRED ACTIONS

### For You (WordPress Configuration)

1. **Add Yoast REST API Support**
   - Go to WordPress → Appearance → Theme Functions (or functions.php)
   - Add the code from Issue 1
   - Save and test

   **OR**

   - Install plugin: https://github.com/ChazUK/wp-api-yoast-meta
   - Activate plugin
   - Test

2. **Verify Featured Image Upload**
   - Check server logs after uploading images
   - Verify media IDs are valid
   - Check WordPress user permissions

3. **Test One Post End-to-End**
   - Convert a blog post
   - Upload images
   - Send to WordPress
   - Check server logs for all field values being sent
   - Check WordPress draft to see what was received

### For Me (Code Fixes)

1. **Fix KCM Slug Extraction** - Extract only slug segment, not full path
2. **Add More Logging** - Log exactly what WordPress REST API returns
3. **Validate Media IDs** - Check if media exists before sending

---

## PAYLOAD STRUCTURE COMPARISON

### What We Send (Python → N8N → WordPress)
```json
{
  "body": {
    "title": "Article Title",
    "content": "<p>HTML content</p>",
    "status": "draft",
    "categories": [881, 884],
    "tags": [1145, 1147],
    "featured_media": 12345,
    "meta": {
      "_yoast_wpseo_focuskw": "focus keyphrase",
      "_yoast_wpseo_metadesc": "meta description",
      "_yoast_wpseo_title": "SEO title"
    }
  }
}
```

### What WordPress REST API Expects
- ✅ `title`, `content`, `status` - Standard fields (work)
- ✅ `categories`, `tags` - Standard fields (work)
- ✅ `featured_media` - Standard field (should work if ID valid)
- ❌ `meta._yoast_wpseo_*` - **BLOCKED unless registered in WordPress**

---

## NEXT STEPS

1. **You:** Add WordPress code to register Yoast fields
2. **Me:** Fix KCM slug extraction
3. **You:** Test and provide server logs
4. **Me:** Debug featured_media based on logs

---

## References

- WordPress REST API Posts: https://developer.wordpress.org/rest-api/reference/posts/
- Yoast REST API Plugin: https://github.com/ChazUK/wp-api-yoast-meta
- Register Post Meta: https://developer.wordpress.org/reference/functions/register_post_meta/

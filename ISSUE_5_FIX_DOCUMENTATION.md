# Issue #5 Fix: Yoast Fields Not Saving via REST API

**Date:** 2025-11-09
**Version:** 2.0
**Status:** CRITICAL FIX DEPLOYED

---

## The Problem (Root Cause Identified)

WordPress treats **underscore-prefixed meta fields as "private"** and **BLOCKS** REST API updates, even when registered with `register_post_meta()`.

### What Was Happening:
1. We sent Yoast fields in the payload: `{"meta": {"_yoast_wpseo_focuskw": "value"}}`
2. WordPress accepted the field NAMES but **ignored the VALUES**
3. WordPress returned: `{"_yoast_wpseo_focuskw": ""}` (empty)
4. Featured image also returned 0 due to permission issues

### Server Logs Showed:
```
✅ Sent: "_yoast_wpseo_focuskw": "South Jersey home equity"
❌ WordPress returned: _yoast_wpseo_focuskw: EMPTY or NOT SET
```

---

## The Solution (Version 2.0)

### 1. WordPress Plugin Rewrite (`wordpress-yoast-rest-api.php` v2.0)

**Changed from:**
- `register_post_meta()` - WordPress blocks updates to underscore-prefixed fields

**Changed to:**
- `register_rest_field()` - Creates top-level REST API fields with direct `update_callback()`
- Bypasses WordPress's private meta field restrictions
- Directly calls `update_post_meta()` to save values

**New Code:**
```php
register_rest_field('post', '_yoast_wpseo_focuskw', array(
    'get_callback' => function($post) {
        return get_post_meta($post['id'], '_yoast_wpseo_focuskw', true);
    },
    'update_callback' => function($value, $post) {
        if (!empty($value)) {
            update_post_meta($post->ID, '_yoast_wpseo_focuskw', sanitize_text_field($value));
            error_log("Yoast REST API: Updated _yoast_wpseo_focuskw = " . $value);
        }
    },
    'schema' => array(
        'type' => 'string',
        'description' => 'Yoast SEO Focus Keyphrase',
    ),
));
```

### 2. Python Server Changes

**Changed payload structure:**

**BEFORE (v1.x - didn't work):**
```json
{
  "meta": {
    "_yoast_wpseo_focuskw": "South Jersey home equity",
    "_yoast_wpseo_title": "SEO Title",
    "_yoast_wpseo_metadesc": "Meta description"
  }
}
```

**AFTER (v2.0 - should work):**
```json
{
  "_yoast_wpseo_focuskw": "South Jersey home equity",
  "_yoast_wpseo_title": "SEO Title",
  "_yoast_wpseo_metadesc": "Meta description"
}
```

Yoast fields are now **top-level fields** in the REST API payload, not nested under `meta`.

---

## Installation Steps (CRITICAL)

### Step 1: Update WordPress Plugin

1. Go to WordPress → Plugins
2. **Deactivate** "Yoast SEO REST API Support"
3. **Delete** the old plugin file
4. **Upload** the new file from: `/home/user/KCM-blog-converter/wordpress-yoast-rest-api.php`
5. **Activate** the plugin
6. Verify version shows **2.0** in the plugin list

### Step 2: Enable WordPress Debug Logging (Optional but Recommended)

Add to `wp-config.php`:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

This will log Yoast field updates to `/wp-content/debug.log`

### Step 3: Restart Python Server

1. Stop the current server (Ctrl+C)
2. Restart: `python kcm-converter/kcm_converter_server.py`
3. Server will use new v2.0 payload structure

---

## Testing Instructions

### 1. Convert a Blog Post
- Paste HTML into converter
- Click "Convert to South Jersey"
- Upload images
- Send to WordPress

### 2. Check Python Server Logs

Look for these new log entries:

```
🔍 YOAST FIELDS (v2.0 - TOP-LEVEL):
  - _yoast_wpseo_focuskw: South Jersey home equity
  - _yoast_wpseo_title: Why Your South Jersey Home Equity...
  - _yoast_wpseo_metadesc: Despite market adjustments, South Jersey homeowners...
```

Then check WordPress response:

```
WordPress Response - Yoast Fields (v2.0 - TOP-LEVEL):
  ✅ _yoast_wpseo_focuskw: 'South Jersey home equity'
  ✅ _yoast_wpseo_title: 'Why Your South Jersey Home Equity...'
  ✅ _yoast_wpseo_metadesc: 'Despite market adjustments, South Jersey homeowners...'
```

### 3. Check WordPress Debug Log (if enabled)

Look for:
```
Yoast REST API: Updated _yoast_wpseo_focuskw = South Jersey home equity
Yoast REST API: Updated _yoast_wpseo_title = Why Your South Jersey Home Equity...
Yoast REST API: Updated _yoast_wpseo_metadesc = Despite market adjustments...
```

### 4. Check WordPress Admin

1. Go to Posts → All Posts
2. Open the draft post
3. Scroll down to Yoast SEO panel
4. Verify:
   - ✅ Focus keyphrase is set
   - ✅ SEO title is set
   - ✅ Meta description is set
   - ✅ Featured image is set

---

## What Should Work Now

✅ **Focus Keyphrase** - Set via `_yoast_wpseo_focuskw` top-level field
✅ **SEO Title** - Set via `_yoast_wpseo_title` top-level field
✅ **Meta Description** - Set via `_yoast_wpseo_metadesc` top-level field
⚠️ **Featured Image** - Still needs testing (permission fix included in v2.0 plugin)

---

## If It Still Doesn't Work

### Check These:

1. **Plugin Active?**
   - WordPress → Plugins → Verify "Yoast SEO REST API Support" is **Active**
   - Version should show **2.0**

2. **WordPress Debug Log**
   - Check `/wp-content/debug.log` for "Yoast REST API: Updated..." messages
   - If missing, the update_callback is not firing

3. **Server Logs**
   - Check if Yoast fields are being SENT as top-level fields
   - Check if WordPress RETURNS values or empties

4. **WordPress Cache**
   - Clear all caches (object cache, page cache, etc.)
   - Try disabling caching plugins temporarily

5. **REST API Permissions**
   - Verify the App Password user has `edit_posts` capability
   - Try creating a test post manually in WordPress admin first

---

## Technical Reference

### Files Changed:
1. `wordpress-yoast-rest-api.php` - WordPress plugin v2.0
2. `shared/wordpress_taxonomy_ids.py` - Payload builder (top-level fields)
3. `kcm-converter/kcm_converter_server.py` - Logging updates

### Commits:
- `999ca69` - CRITICAL FIX v2.0: Use register_rest_field()
- `dfd28e1` - Add *.zip to gitignore
- `f3e5f18` - Fix Yoast fields and featured_media issues
- `15afe91` - Add WordPress plugin to fix Yoast REST API fields

### Branch:
`claude/fix-yoast-error-011CUeK1jdjtuthXNai8e59x`

---

## Support

If the issue persists after following all steps:
1. Paste the FULL server log output (from conversion to WordPress response)
2. Paste the WordPress debug.log content (if enabled)
3. Confirm the WordPress plugin version shows 2.0
4. Confirm you've deactivated and reactivated the plugin

This will give enough data to diagnose the exact failure point.

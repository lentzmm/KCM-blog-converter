# How to Resolve the Merge Conflict in `shared/wordpress_taxonomy_ids.py`

## The Conflict

When merging `claude/fix-yoast-error-011CUeK1jdjtuthXNai8e59x` into `main`, there's a conflict in the `build_webhook_payload()` function.

### Main Branch (OLD - INCORRECT)
```python
# n8n expects Yoast fields at the root level with specific field names
# n8n accesses: body.body.yoast_focus_keyword and body.body.yoast_meta_description
if yoast_meta:
    payload['yoast_focus_keyword'] = yoast_meta.get('yoast_wpseo_focuskw', '')
    payload['yoast_meta_description'] = yoast_meta.get('yoast_wpseo_metadesc', '')
    payload['yoast_title'] = yoast_meta.get('yoast_wpseo_title', '')
```

### Feature Branch (NEW - CORRECT)
```python
# CRITICAL: N8N workflow uses HTTP Request node (NOT WordPress node)
# WordPress REST API requires Yoast fields in the 'meta' object with underscore-prefixed keys
# Format: meta: { _yoast_wpseo_focuskw: '...', _yoast_wpseo_metadesc: '...', _yoast_wpseo_title: '...' }
# This is the correct format for Yoast Premium REST API
if yoast_meta:
    payload['meta'] = {
        '_yoast_wpseo_focuskw': yoast_meta.get('yoast_wpseo_focuskw', ''),
        '_yoast_wpseo_metadesc': yoast_meta.get('yoast_wpseo_metadesc', ''),
        '_yoast_wpseo_title': yoast_meta.get('yoast_wpseo_title', '')
    }
```

## Resolution Instructions

### Option 1: Resolve on GitHub (Web Editor)

1. Go to the Pull Request on GitHub
2. Click "Resolve conflicts"
3. In `shared/wordpress_taxonomy_ids.py`, find the conflict markers:
   ```
   <<<<<<< main
   ... main branch code ...
   =======
   ... feature branch code ...
   >>>>>>> claude/fix-yoast-error-011CUeK1jdjtuthXNai8e59x
   ```
4. **Delete the main branch version** and **keep the feature branch version**
5. Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
6. The final code should look like this:

```python
if featured_media_id:
    payload['featured_media'] = featured_media_id

# CRITICAL: N8N workflow uses HTTP Request node (NOT WordPress node)
# WordPress REST API requires Yoast fields in the 'meta' object with underscore-prefixed keys
# Format: meta: { _yoast_wpseo_focuskw: '...', _yoast_wpseo_metadesc: '...', _yoast_wpseo_title: '...' }
# This is the correct format for Yoast Premium REST API
if yoast_meta:
    payload['meta'] = {
        '_yoast_wpseo_focuskw': yoast_meta.get('yoast_wpseo_focuskw', ''),
        '_yoast_wpseo_metadesc': yoast_meta.get('yoast_wpseo_metadesc', ''),
        '_yoast_wpseo_title': yoast_meta.get('yoast_wpseo_title', '')
    }

return payload
```

7. Click "Mark as resolved"
8. Click "Commit merge"

### Option 2: Resolve Locally (Command Line)

```bash
# Pull latest changes
git checkout main
git pull origin main

# Merge the feature branch
git merge claude/fix-yoast-error-011CUeK1jdjtuthXNai8e59x

# You'll see a conflict - open shared/wordpress_taxonomy_ids.py
# Keep the feature branch version (the one with payload['meta'] = {...})
# Remove all conflict markers

# Stage the resolved file
git add shared/wordpress_taxonomy_ids.py

# Complete the merge
git commit -m "Merge: Fix Yoast SEO fields for HTTP Request node"

# Push to main
git push origin main
```

## Why Keep the Feature Branch Version?

The feature branch version is **correct** because:

1. ✅ **N8N uses HTTP Request node** (not WordPress node)
2. ✅ **WordPress REST API requires `meta` object** for custom fields
3. ✅ **Yoast Premium has REST API support** and recognizes these meta keys
4. ✅ **Underscore-prefixed keys** (_yoast_wpseo_*) are the actual WordPress meta field names

The main branch version **doesn't work** because:

❌ WordPress REST API doesn't recognize `yoast_focus_keyword`, `yoast_meta_description`, or `yoast_title` as valid fields
❌ These fields are only available in N8N's WordPress node (which we're not using)
❌ Without the `meta` object, Yoast fields won't be saved to the WordPress post

## After Resolution

Once the conflict is resolved and merged:

1. Test by converting a blog post
2. Check the WordPress draft
3. Verify Yoast SEO panel shows:
   - ✅ Focus keyphrase populated
   - ✅ SEO title populated
   - ✅ Meta description populated

---

**Created:** 2025-11-09
**For PR:** `claude/fix-yoast-error-011CUeK1jdjtuthXNai8e59x` → `main`

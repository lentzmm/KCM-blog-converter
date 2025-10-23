# Image Processing Fixes - October 21, 2025

## Issues Fixed

### 1. **Generic Filenames Instead of SEO-Optimized Names**
**Problem:** Images were uploaded with generic WordPress-generated names instead of the SEO-optimized filenames.

**Root Cause:** WordPress REST API ignores the `Content-Disposition` header filename and generates its own.

**Solution:** After uploading, we now update the media post's slug, title, and alt text via a second API call:
- Sets slug to the SEO-optimized name (e.g., `equity-south-jersey-guide`)
- Sets title to human-readable version
- Sets alt text with geographic keywords
- Returns the updated WordPress URL

**Code Location:** `upload_image_to_wordpress()` function (lines 391-480)

### 2. **Images Not Linking Properly in Post**
**Problem:** The HTML contained original KCM image URLs or generic paths, not the actual WordPress URLs.

**Root Cause:** The `convert_image_urls()` function was called during blog rewriting, before images were uploaded, so it couldn't use actual WordPress URLs.

**Solution:**
- Removed early `convert_image_urls()` call from `rewrite_blog_post()`
- Modified `convert_image_urls()` to accept an `uploaded_image_mapping` parameter
- Now called in `send_to_wordpress()` AFTER images are uploaded
- Maps original URLs → actual WordPress URLs with SEO filenames

**Code Locations:**
- `convert_image_urls()` updated (lines 90-129)
- `rewrite_blog_post()` updated (lines 757-758)
- `send_to_wordpress()` updated (lines 862-867)

### 3. **Featured Image Not Set**
**Problem:** Featured image wasn't being set on the WordPress post.

**Root Cause:** The `featured_image_id` was being passed but needed to be explicitly retrieved from uploaded images.

**Solution:**
- In `send_to_wordpress()`, automatically use first uploaded image as featured image if not specified
- Pass `featured_image_id` to `build_webhook_payload()`
- Webhook payload includes `featured_media` field with the WordPress media ID

**Code Location:** `send_to_wordpress()` function (lines 857-870)

## Workflow Changes

### Old Workflow (Broken)
1. Convert blog post → images extracted with SEO names
2. Rewrite HTML → image URLs converted to generic paths
3. Upload images → uploaded with generic names
4. Send to WordPress → images don't match, featured image not set

### New Workflow (Fixed)
1. Convert blog post → images extracted with SEO-optimized filenames
2. Rewrite HTML → images remain as original URLs (placeholders)
3. **Upload images** → uploaded AND renamed with SEO filenames via WordPress API
4. **Send to WordPress** →
   - Image URLs updated in HTML using uploaded mapping
   - Featured image set to first uploaded image
   - Payload sent with correct content and featured_media ID

## Testing Checklist

- [ ] Images upload with SEO-optimized filenames (e.g., `equity-south-jersey-guide.png`)
- [ ] Image slugs in WordPress match SEO filenames
- [ ] Alt text includes geographic keywords
- [ ] HTML `<img>` tags use WordPress URLs (e.g., `https://mikesellsnj.com/wp-content/uploads/2025/10/equity-south-jersey-guide.png`)
- [ ] Featured image is set on WordPress post
- [ ] All images display correctly in published post

## Key Functions Modified

1. **`upload_image_to_wordpress()`** - Now updates slug, title, and alt text after upload
2. **`convert_image_urls()`** - Now accepts uploaded image mapping and uses actual WordPress URLs
3. **`rewrite_blog_post()`** - Removed premature image URL conversion
4. **`send_to_wordpress()`** - Updates HTML with WordPress URLs before sending

## Notes

- Images must be uploaded BEFORE sending HTML to WordPress for proper URL replacement
- The `uploaded_images` global variable stores the mapping between original and WordPress URLs
- Featured image defaults to the first uploaded image
- SEO filenames follow format: `{topic}-{geo}-{descriptor}.{ext}`

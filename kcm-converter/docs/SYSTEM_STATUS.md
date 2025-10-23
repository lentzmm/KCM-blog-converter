# KCM Converter System Status - October 21, 2025

## Current Configuration

### Active Prompt Template
**File:** `kcm_prompt_ACTIVE.md`
- Dynamically loaded at runtime by `rewrite_blog_post()` function
- Previous versions (v3, v4) preserved for reference
- Clear naming convention ensures no confusion about which prompt is in use

### Image Processing Pipeline

#### 1. Filename Generation
**Function:** `extract_images()` (lines 505-625)

**SEO Optimization Strategy:**
- 22 topic keywords (expanded from original 11)
- Intelligent fallback: extracts first 2-3 meaningful words from slug
- Pattern: `{topic}-{geo}-{descriptor}.{ext}`

**Examples:**
- "why-home-prices-arent-flat" → `prices-south-jersey-guide.png`
- "understanding-equity-growth" → `equity-south-jersey-guide.png`
- "spring-market-outlook-2025" → `market-south-jersey-guide.png`
- "when-conditions-improve" → `when-conditions-south-jersey-guide.png`

#### 2. Alt Text Generation
**Function:** `extract_images()` (lines 586-620)

**SEO Strategy (matches ACTIVE prompt):**
- **50%+ Rule:** Odd-numbered images get exact focus keyphrase
- **Natural Variation:** Even-numbered images use descriptive alternatives
- **Pattern for odd images:** `{focus_keyphrase}: {original_alt}` or `{focus_keyphrase} - infographic {index}`
- **Pattern for even images:** `{original_alt} - South Jersey real estate` or `{slug} guide - visual {index}`

**Example (3 images, keyphrase: "South Jersey home prices"):**
1. Image 1 (odd): `South Jersey home prices: housing market trends chart` ✅
2. Image 2 (even): `South Jersey Home Prices 2025 guide - visual 2` ℹ️
3. Image 3 (odd): `South Jersey home prices - infographic 3` ✅

**Result:** 66% include exact keyphrase (exceeds 50% requirement)

#### 3. WordPress Upload
**Function:** `upload_image_to_wordpress()` (lines 413-502)

**Process:**
1. Upload image file via WordPress REST API
2. Update media post metadata:
   - `slug`: SEO-optimized filename (without extension)
   - `alt_text`: Geographic + keyphrase optimized
   - `title`: Human-readable version of slug
3. Return WordPress URL with SEO filename

#### 4. HTML URL Replacement
**Function:** `convert_image_urls()` (lines 90-151)

**Two-Pass Replacement:**
1. **First Pass:** Update all `<img src>` attributes
2. **Second Pass:** Update all `<a href>` attributes linking to images

**Result:** Both links and images point to WordPress URLs

#### 5. Featured Image
**Function:** `send_to_wordpress()` (lines 862-870)

**Logic:**
- Automatically sets first uploaded image as featured image
- Includes `featured_media` field in webhook payload

## Workflow

### Step-by-Step Process

1. **User Input**
   - Paste original KCM blog HTML
   - Enter SEO metadata (title, slug, focus keyphrase, etc.)

2. **Convert to South Jersey** (`/convert` endpoint)
   - Load ACTIVE prompt template
   - Send to Claude API for rewriting
   - Extract images with SEO-optimized filenames
   - Apply 50% keyphrase rule to alt text
   - Return preview with image list

3. **Upload Images** (`/process-images` endpoint)
   - Upload each image to WordPress
   - Update media metadata (slug, alt, title)
   - Store mapping: original URL → WordPress URL

4. **Send HTML to WordPress** (`/send-to-wordpress` endpoint)
   - Update image URLs in HTML using mapping
   - Build webhook payload with SEO metadata
   - Set featured image to first uploaded image
   - Send to Make.com webhook
   - WordPress creates/updates post

## Files Modified Today

### kcm_converter_server.py
- `rewrite_blog_post()`: Load prompt from ACTIVE file
- `extract_images()`: Expanded keywords, intelligent fallback, 50% keyphrase rule
- `upload_image_to_wordpress()`: Post-upload metadata update
- `convert_image_urls()`: Two-pass replacement (img src + a href)
- `send_to_wordpress()`: Image URL mapping and featured image
- `/convert` endpoint: Pass focus keyphrase to extract_images()

### clipboard.html
- Created in kcm-converter directory
- Reorganized UI:
  - Step 1B before Convert button
  - Upload Images + Send HTML grouped together
  - Manual options (download, copy) less prominent

### refined_kcm_prompt_v4.md → kcm_prompt_ACTIVE.md
- Renamed for clarity
- Contains active conversion guidelines
- Includes 50% alt text keyphrase rule

## Documentation Created

1. **IMAGE_FIXES.md** - Initial image processing fixes (upload, linking, featured image)
2. **IMAGE_FILENAME_FIXES.md** - Filename generation improvements
3. **ALT_TEXT_SEO_UPDATE.md** - 50% keyphrase rule implementation
4. **SYSTEM_STATUS.md** - This file (complete system overview)

## Testing Checklist

### Before Upload
- [ ] Preview shows SEO-optimized filenames (not "article-south-jersey-1.png")
- [ ] Alt text for 50%+ of images includes exact focus keyphrase
- [ ] Alt text reads naturally (not keyword-stuffed)

### After Upload to WordPress
- [ ] Images uploaded with SEO filenames
- [ ] Image slugs in WordPress media library match SEO names
- [ ] Both `<img src>` and `<a href>` point to WordPress URLs
- [ ] Featured image is set
- [ ] All images display correctly in published post
- [ ] Alt text viewable in WordPress matches preview

## Next Test Recommendations

1. Choose a KCM blog post with 3+ images
2. Use a clear focus keyphrase (e.g., "South Jersey home prices")
3. Check preview carefully before uploading
4. Verify WordPress media library after upload
5. View published post to confirm all images display
6. Check HTML source to verify both src and href are correct
7. Verify alt text in WordPress matches SEO strategy

## Key Technical Decisions

### Why Two-Pass URL Replacement?
Original KCM posts wrap images in `<a>` tags. We need to update both the image source AND the link destination to point to WordPress URLs.

### Why 50% Keyphrase Rule?
SEO best practice: include focus keyphrase in multiple images without keyword stuffing. Alternating pattern ensures natural distribution.

### Why Post-Upload Metadata Update?
WordPress REST API ignores `Content-Disposition` header filename. We must update the media post after upload to set the SEO-optimized slug.

### Why Dynamic Prompt Loading?
Allows quick iteration on conversion strategy without modifying Python code. Simply edit the ACTIVE markdown file and restart the server.

## System Health

✅ All requested features implemented
✅ All reported bugs fixed
✅ SEO optimization complete
✅ Documentation comprehensive
✅ Ready for production testing

# Image Filename Generation Fixes - October 21, 2025

## Issues Fixed

### 1. **Generic "article-south-jersey-1.png" Filenames**

**Problem:** Images were being named generically like "article-south-jersey-1.png" instead of SEO-optimized names.

**Root Cause:** The `extract_images()` function had a fallback that used the full article slug when no topic keyword was found. Since many slugs don't contain keywords like "equity" or "mortgage", it would fall back to the else clause which used the entire slug (often just "article").

**Solution:**
- **Expanded keyword list**: Added more topic keywords including plurals (homes, buyers, sellers, prices, etc.)
- **Intelligent fallback**: If no keyword match, extract first 2-3 meaningful words from slug
- **Removed generic fallback**: Eliminated the code path that created "article-south-jersey" names

**Code Location:** `extract_images()` function (lines 491-515)

**Before:**
```python
topic_keywords = ['home', 'house', 'real-estate', 'buyer', 'seller', 'market',
                 'equity', 'mortgage', 'property', 'downsizing', 'first-time']
topic_term = next((kw for kw in topic_keywords if kw in slug), None)

if topic_term:
    suggested_filename = f"{topic_term}-{geo_term}-guide{ext}"
else:
    suggested_filename = f"{slug}-south-jersey-{index}{ext}"  # Generic!
```

**After:**
```python
topic_keywords = ['home', 'homes', 'house', 'buyer', 'buyers', 'seller', 'sellers',
                 'market', 'equity', 'mortgage', 'property', 'properties', 'downsizing',
                 'first-time', 'price', 'prices', 'value', 'sell', 'buy', 'buying', 'selling']

topic_term = next((kw for kw in topic_keywords if kw in slug), None)

if not topic_term:
    # Extract first 2-3 meaningful words from slug
    slug_words = [w for w in slug.split('-') if w not in ['the', 'a', 'an', 'and', 'or', 'but'...]]
    if len(slug_words) >= 2:
        topic_term = '-'.join(slug_words[:2])
    else:
        topic_term = 'real-estate'

# Always use topic-geo pattern
suggested_filename = f"{topic_term}-{geo_term}-guide{ext}"
```

**Result:**
- Slug: "why-home-prices-arent-flat" → Image: `home-prices-south-jersey-guide.png`
- Slug: "understanding-buyer-demand" → Image: `buyer-demand-south-jersey-guide.png`
- Slug: "new-construction-trends" → Image: `new-construction-south-jersey-guide.png`

---

### 2. **Image href Links Not Updated**

**Problem:** The `<a href>` tags wrapping images still pointed to original KCM URLs, even though `<img src>` was updated.

**Example of the issue:**
```html
<!-- Before fix -->
<a href="https://www.simplifyingthemarket.com/image.png">
  <img src="https://mikesellsnj.com/wp-content/uploads/2025/10/equity-south-jersey-guide.png">
</a>

<!-- After fix -->
<a href="https://mikesellsnj.com/wp-content/uploads/2025/10/equity-south-jersey-guide.png">
  <img src="https://mikesellsnj.com/wp-content/uploads/2025/10/equity-south-jersey-guide.png">
</a>
```

**Root Cause:** The `convert_image_urls()` function only updated `<img src>` attributes, not `<a href>` attributes.

**Solution:** Added a second regex replacement pass to update `<a href>` tags that match image URLs.

**Code Location:** `convert_image_urls()` function (lines 125-144)

**Implementation:**
```python
# First pass: Update <img src> attributes
img_pattern = r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>'
modified_html = re.sub(img_pattern, replace_img, html)

# Second pass: Update <a href> attributes for image links
link_pattern = r'<a\s+([^>]*?)href="([^"]+)"([^>]*?)>'
modified_html = re.sub(link_pattern, replace_link, modified_html)
```

---

## Testing Examples

### Example 1: "Why Home Prices Aren't Flat in South Jersey"
- **Slug:** `why-home-prices-arent-flat-south-jersey`
- **Topic found:** `prices` (from expanded keyword list)
- **Image 1:** `prices-south-jersey-guide.png`
- **Image 2:** `prices-south-jersey-2.png`
- **Image 3:** `prices-south-jersey-3.png`

### Example 2: "Understanding Equity Growth"
- **Slug:** `understanding-equity-growth`
- **Topic found:** `equity` (from keyword list)
- **Image 1:** `equity-south-jersey-guide.png`
- **Image 2:** `equity-south-jersey-2.png`

### Example 3: "Spring Market Outlook 2025"
- **Slug:** `spring-market-outlook-2025`
- **Topic found:** `market` (from keyword list)
- **Image 1:** `market-south-jersey-guide.png`

### Example 4: "When Conditions Improve" (no obvious keyword)
- **Slug:** `when-conditions-improve`
- **Topic found:** None initially
- **Fallback:** Extract first 2 words → `when-conditions`
- **Image 1:** `when-conditions-south-jersey-guide.png`

---

## Summary of Changes

1. **Expanded topic keyword list** from 11 to 22 keywords
2. **Added intelligent fallback** using first 2-3 slug words
3. **Removed generic "article" fallback** completely
4. **Updated both src and href** for complete image URL replacement
5. **Added logging** to track slug extraction and topic term selection

## Files Modified

- `kcm_converter_server.py`:
  - `extract_images()` (lines 483-575)
  - `convert_image_urls()` (lines 90-151)

## Next Test

Upload a new blog post and verify:
1. Preview shows SEO-optimized filenames (not "article-south-jersey-1.png")
2. After upload, both `<img src>` and `<a href>` point to WordPress URLs
3. Featured image is set correctly
4. All images display in published post

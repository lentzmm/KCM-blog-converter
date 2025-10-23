# Alt Text SEO Optimization - October 21, 2025

## Changes Made

### Updated Alt Text Generation to Match ACTIVE Prompt Guidelines

**ACTIVE Prompt Requirements:**
- **50%+ of images** must include the exact focus keyphrase
- Remaining images use variations or descriptive text
- Keep alt text natural and descriptive

## Implementation

### 1. **Pass Focus Keyphrase to Image Extraction**

Modified the `/convert` endpoint to pass the focus_keyphrase to `extract_images()`:

```python
# Extract images with focus keyphrase for SEO-optimized alt text
focus_keyphrase = seo_metadata.get('focus_keyphrase', '')
images = extract_images(original_html, converted_html, focus_keyphrase)
```

**Location:** `kcm_converter_server.py:864-866`

### 2. **Updated extract_images() Function Signature**

Added `focus_keyphrase` parameter:

```python
def extract_images(original_html: str, converted_html: str, focus_keyphrase: str = "") -> List[Dict]:
```

**Location:** `kcm_converter_server.py:505`

### 3. **Implemented 50% Keyphrase Rule**

New alt text logic (lines 586-620):

```python
# Determine if this image should include the exact keyphrase (50% rule)
include_keyphrase = (index % 2 == 1)  # Odd-numbered images get exact keyphrase

if include_keyphrase and focus_keyphrase:
    # Include exact focus keyphrase
    if original_alt:
        alt_text = f"{focus_keyphrase}: {original_alt}"
    else:
        alt_text = f"{focus_keyphrase} - infographic {index}"
else:
    # Use variation or descriptive alt text
    if original_alt:
        alt_text = f"{original_alt} - South Jersey real estate"
    else:
        alt_text = f"{clean_slug} guide - visual {index}"
```

## Examples

### Article: "South Jersey Home Prices 2025"
**Focus Keyphrase:** "South Jersey home prices"

**3 Images in Post:**

1. **Image 1 (odd):**
   - Filename: `home-prices-south-jersey-guide.png`
   - Alt: `South Jersey home prices: housing market trends chart`
   - ✅ Includes exact keyphrase

2. **Image 2 (even):**
   - Filename: `home-prices-south-jersey-2.png`
   - Alt: `South Jersey Home Prices 2025 guide - visual 2`
   - ℹ️ Descriptive variation

3. **Image 3 (odd):**
   - Filename: `home-prices-south-jersey-3.png`
   - Alt: `South Jersey home prices - infographic 3`
   - ✅ Includes exact keyphrase

**Result:** 2 out of 3 images (66%) include exact keyphrase ✅ Exceeds 50% requirement

## Logging

Added detailed logging to track keyphrase usage:

```
Extracting images from blog post...
Focus keyphrase for alt text: South Jersey home prices
Extracted slug for images: south-jersey-home-prices-2025
Topic term for images: home-prices, Geo term: south-jersey
  Image 1: Using exact keyphrase in alt text
  Image 2: Using descriptive alt text (variation)
  Image 3: Using exact keyphrase in alt text
Extracted 3 images with SEO/GEO optimized filenames
```

## SEO Benefits

1. **Improved Image SEO:** Exact keyphrase in 50%+ of alt text strengthens relevance signals
2. **Natural Variation:** Remaining images avoid keyword stuffing while staying descriptive
3. **Accessibility:** Alt text remains helpful for screen readers
4. **Consistent with ACTIVE Prompt:** Follows documented SEO strategy

## Testing Checklist

- [ ] Alt text for odd-numbered images includes exact focus keyphrase
- [ ] Alt text for even-numbered images uses variations
- [ ] At least 50% of images have exact keyphrase
- [ ] Alt text reads naturally (not stuffed)
- [ ] Logs show keyphrase usage for each image

## Files Modified

- `kcm_converter_server.py`:
  - `extract_images()` function signature and logic (lines 505-625)
  - `/convert` endpoint (lines 864-866)

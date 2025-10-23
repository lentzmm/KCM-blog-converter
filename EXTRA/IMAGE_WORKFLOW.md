# Image Workflow for KCM Blog Converter

## Current Status

The converter currently handles images by:
1. Detecting image `<img>` tags in the HTML
2. Converting URLs to WordPress structure: `/wp-content/uploads/YYYY/MM/filename`
3. Using current year and month automatically

## Issues to Address

### 1. **Inconsistent Naming**
- KCM images have inconsistent filenames
- Need a standardized naming convention

### 2. **Manual Upload Required**
- Images still need to be downloaded from KCM
- Images must be manually uploaded to WordPress
- Current process doesn't automate this

## Proposed Workflow Options

### Option A: Semi-Automated (Recommended)

**Step 1: During Conversion**
- Extract all image URLs from KCM blog
- Generate standardized filenames based on:
  - Article slug
  - Image position (image-1, image-2, etc.)
  - Example: `buying-homes-south-jersey-1.png`

**Step 2: Create Download List**
- Output a JSON file with:
  - Original KCM URL
  - Suggested filename
  - Suggested WordPress path

**Step 3: Manual Upload**
- User downloads images from KCM
- User renames according to suggestions
- User uploads to WordPress media library
- WordPress auto-organizes by date

**Benefits:**
- Simple and reliable
- No risk of copyright issues
- User has control over image quality

### Option B: Fully Automated

**Step 1: Download Images**
- Python script downloads all images from KCM
- Saves locally with standardized names

**Step 2: Upload to WordPress**
- Use WordPress REST API to upload images
- Requires WordPress credentials
- Auto-generates media library entries

**Benefits:**
- Completely automated
- Faster workflow

**Risks:**
- Requires WordPress API access
- May hit rate limits
- Copyright/attribution concerns

### Option C: Image Reference Guide

**Step 1: During Conversion**
- Create a markdown table showing:
  - Image position in article
  - KCM URL
  - Suggested filename
  - WordPress path

**Step 2: Manual Process**
- User follows guide to download and upload
- User updates image names in HTML if needed

## Recommended Implementation (Option A+)

Enhance the converter to output:

```json
{
  "converted_html": "...",
  "seo": {...},
  "images": [
    {
      "position": 1,
      "original_url": "https://www.simplifyingthemarket.com/images/abc123.png",
      "suggested_filename": "article-slug-image-1.png",
      "wordpress_path": "/wp-content/uploads/2025/10/article-slug-image-1.png",
      "alt_text": "Suggested alt text for SEO",
      "current_html": "<img src='original'>",
      "updated_html": "<img src='/wp-content/uploads/2025/10/article-slug-image-1.png' alt='...'>"
    }
  ]
}
```

### Implementation Steps:

1. **Extract Image Data**
   - Parse all `<img>` tags from original HTML
   - Extract src, alt, title attributes
   - Determine image position in article

2. **Generate Naming Convention**
   - Extract article slug from title or first H1
   - Format: `{slug}-image-{number}.{ext}`
   - Example: `south-jersey-home-equity-image-1.png`

3. **Create Download Instructions**
   - Display table in UI showing:
     - Thumbnail (if possible)
     - Original URL (clickable to download)
     - Suggested filename
     - WordPress path

4. **Provide WordPress-Ready HTML**
   - Replace image URLs with final WordPress paths
   - Add proper alt text for SEO
   - Include responsive image attributes if needed

## User Workflow

1. **Run Conversion** → Get converted HTML + image manifest
2. **Review Images** → See list of all images with download links
3. **Download Images** → Click each image URL, save with suggested name
4. **Upload to WordPress** → Use WordPress media library
5. **Verify Paths** → Ensure uploaded images match suggested paths
6. **Publish** → HTML already has correct image references

## Naming Convention Standards

### Format
```
{article-slug}-image-{number}.{extension}
or
{article-slug}-{descriptive-name}.{extension}
```

### Examples
```
downsizing-south-jersey-image-1.png
downsizing-south-jersey-couple-planning.png
first-time-buyers-cherry-hill-image-1.jpg
first-time-buyers-cherry-hill-savings-chart.png
```

### Rules
- Use article slug (kebab-case)
- Add descriptive name if meaningful
- Use sequential numbers for generic images
- Keep extensions from original (png, jpg, etc.)
- Max 50 characters total

## Next Steps

1. Add image extraction function to server
2. Generate standardized filenames
3. Create image manifest in response
4. Add image table to UI
5. Provide downloadable CSV/JSON of image list
6. Update HTML with final WordPress paths

## Alternative: WordPress Integration

If you want full automation:
- Provide WordPress site URL
- Provide WordPress application password
- Server downloads images from KCM
- Server uploads to WordPress via REST API
- Returns HTML with actual uploaded image URLs

**Requires:**
- WordPress REST API enabled
- Application password for authentication
- Proper CORS settings
- Media upload permissions

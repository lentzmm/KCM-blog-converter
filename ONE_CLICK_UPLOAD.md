# ONE-CLICK Upload Feature

## Overview

New `/upload-all` endpoint that uploads images AND sends the blog post to WordPress in a single operation. This replaces the two-step process of:
1. Click "Upload Images to WordPress"
2. Click "Send to WordPress"

With a single button click!

## API Endpoint

### POST `/upload-all`

**Description:** Upload images and create WordPress post in one operation

**Request Body:**
```json
{
  "converted_html": "<h3>Blog post title...</h3><p>Content...</p>",
  "seo_metadata": {
    "seo_title": "Blog Post Title",
    "focus_keyphrase": "south jersey homes",
    "meta_description": "Description here...",
    "categories": ["For Buyers", "Housing Market Updates"],
    "tags": ["Home Prices", "Cherry Hill", "First Time Home Buyers"]
  },
  "images": [
    {
      "original_url": "https://kcmblog.com/wp-content/uploads/image.jpg",
      "suggested_filename": "home-prices-south-jersey-2025.jpg",
      "alt_text": "South Jersey home prices rising in 2025"
    }
  ]
}
```

**Response (Success):**
```json
{
  "success": true,
  "wordpress_response": {
    "id": 42475,
    "link": "https://mikesellsnj.com/?p=42475",
    "featured_media": 12345
  },
  "images_processed": 3,
  "post_id": 42475,
  "post_url": "https://mikesellsnj.com/?p=42475",
  "featured_image_id": 12345
}
```

**Response (Error):**
```json
{
  "error": "Error message here",
  "details": "Additional details..."
}
```

## How It Works

### Step 1: Upload Images to WordPress (if any)
1. Downloads each image from the original KCM URL
2. Uploads to WordPress Media Library with SEO-optimized filename
3. Sets alt text for accessibility and SEO
4. Tracks WordPress media IDs and URLs
5. First image becomes the featured image

### Step 2: Update HTML with WordPress Image URLs
1. Replaces all KCM image URLs with WordPress URLs
2. Updates both `<img src>` and `<a href>` tags
3. Removes first image from content (it's now the featured image)
4. Cleans up any surrounding `<br>` tags

### Step 3: Send Post to WordPress
1. Builds n8n webhook payload with:
   - Title, content, excerpt, slug
   - Categories and tags (as WordPress IDs)
   - Featured image ID
   - Yoast SEO fields (focus keyword, meta description, SEO title)
2. Sends to n8n webhook
3. n8n forwards to WordPress REST API
4. WordPress creates the post as a draft

## Logging Output

When you use the one-click upload, you'll see this in the Python logs:

```
======================================================================
ONE-CLICK UPLOAD: Starting combined image + WordPress upload
======================================================================
STEP 1/2: Processing 3 images...
  Processing image: https://kcmblog.com/wp-content/uploads/image1.jpg
  Processing image: https://kcmblog.com/wp-content/uploads/image2.jpg
  Processing image: https://kcmblog.com/wp-content/uploads/image3.jpg
✅ Uploaded 3 images, using first as featured image: ID 12345
  Updating 3 image URLs in HTML
  Removed first image (featured) from content
STEP 2/2: Sending post to WordPress...
======================================================================
✅ ONE-CLICK UPLOAD COMPLETE!
   WordPress Post ID: 42475
   Post URL: https://mikesellsnj.com/?p=42475
   Featured Image: 12345
======================================================================
```

## Benefits

### For Users
- **Faster workflow**: One click instead of two
- **Fewer errors**: No risk of forgetting to upload images
- **Better UX**: Clear progress indication in logs

### For Development
- **Atomic operation**: Both steps succeed or fail together
- **Better error handling**: Single point of failure detection
- **Comprehensive logging**: Easy to debug issues

## Comparison: Old vs New Workflow

### Old Workflow (2 Steps)
1. Click "Upload Images to WordPress" → Wait for upload
2. Click "Send to WordPress" → Wait for post creation
3. Check if featured image was set correctly
4. Verify image URLs are WordPress URLs

### New Workflow (1 Step)
1. Click "Upload All to WordPress" → Everything happens automatically
2. Done! ✅

## Error Handling

The endpoint handles these error scenarios:

1. **No HTML provided** → Returns 400 error
2. **No SEO metadata provided** → Returns 400 error
3. **WordPress credentials not configured** → Returns 400 error with setup instructions
4. **Image download fails** → Tracks failed images, continues with successful ones
5. **Image upload fails** → Tracks failed images, continues with successful ones
6. **WordPress webhook fails** → Returns detailed error with response
7. **Request timeout** → Returns 504 error after 30 seconds
8. **Network error** → Returns 500 error with connection details

## Backward Compatibility

The original endpoints are still available:
- `/process-images` - Upload images only
- `/send-to-wordpress` - Send post only (requires images already uploaded)

So existing integrations continue to work while new implementations can use the one-click endpoint.

## Usage in Frontend

To use this endpoint in your frontend/UI, make a single POST request with all the data:

```javascript
// JavaScript example
const response = await fetch('http://localhost:5000/upload-all', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    converted_html: convertedHtml,
    seo_metadata: seoMetadata,
    images: imageList
  })
});

const result = await response.json();

if (result.success) {
  console.log('Post created!', result.post_url);
  console.log('Featured image:', result.featured_image_id);
} else {
  console.error('Error:', result.error);
}
```

## Testing

To test the endpoint manually:

```bash
curl -X POST http://localhost:5000/upload-all \
  -H "Content-Type: application/json" \
  -d '{
    "converted_html": "<h3>Test Post</h3><p>Content here...</p>",
    "seo_metadata": {
      "seo_title": "Test Post Title",
      "focus_keyphrase": "south jersey homes",
      "meta_description": "Test description",
      "categories": ["For Buyers"],
      "tags": ["Home Prices"]
    },
    "images": []
  }'
```

## Next Steps

After deploying this update:

1. **Restart Python server** to load the new endpoint
2. **Update UI/frontend** to add "Upload All to WordPress" button
3. **Test with a sample post** to verify it works
4. **Update any automation scripts** to use the new endpoint (optional)

The two-step buttons can remain as a fallback option for users who want more control over the process.

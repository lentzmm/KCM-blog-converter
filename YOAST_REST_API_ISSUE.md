# Yoast SEO Fields Not Updating via WordPress REST API

## Problem
When sending blog posts to WordPress via n8n webhook → WordPress REST API, the Yoast SEO fields (focus keyphrase and meta description) are not being saved, even though they're being sent in the payload.

## What We're Sending
```json
{
  "meta[_yoast_wpseo_focuskw]": "South Jersey home equity value",
  "meta[_yoast_wpseo_metadesc]": "Despite market shifts, South Jersey homeowners maintain strong equity positions..."
}
```

## What WordPress Returns
WordPress creates the post successfully but uses default/template values for Yoast fields instead of our custom values:
- Focus keyphrase: Empty
- Meta description: Uses template: "Why Your South Jersey Home Equity Still Puts You Way Ahead - The Mike Lentz Team - Keller Williams -"

## WordPress Response
```json
{
  "id": 42412,
  "title": "Why Your South Jersey Home Equity Still Puts You Way Ahead",
  "meta": {
    "cybocfi_hide_featured_image": "",
    "footnotes": "",
    "_elementor_edit_mode": "",
    // ... other meta fields, but NO Yoast fields
  }
}
```

## Current Setup
- WordPress REST API endpoint: `/wp-json/wp/v2/posts`
- Method: POST
- Auth: HTTP Basic Auth
- Yoast SEO Plugin: v26.3

## What Works
- Title, content, excerpt, slug, categories, tags all update correctly
- Post is created successfully as draft

## What Doesn't Work
- Focus keyphrase (_yoast_wpseo_focuskw)
- Meta description (_yoast_wpseo_metadesc)
- SEO title (_yoast_wpseo_title)
- Featured image (sent as `featured_media: 42409` but WordPress returns `featured_media: 0`)

## Research Questions
1. Does WordPress REST API support updating Yoast meta fields directly?
2. Do we need a custom WordPress endpoint or plugin to update Yoast fields?
3. Is there a Yoast REST API extension available?
4. Do we need to use `update_post_meta()` PHP function via a custom endpoint?
5. Are there permission/capability requirements for updating Yoast meta via REST API?

## Attempted Solutions
- Tried sending as `meta[_yoast_wpseo_focuskw]` - didn't work
- Tried sending as `yoast_focus_keyword` - didn't work
- Tried sending as nested `yoast_meta` object - didn't work

## Additional Context
- This is for automated blog publishing workflow
- Posts are created as drafts for review before publishing
- n8n handles the webhook and sends to WordPress REST API
- All other post data (categories, tags, content) works perfectly

#!/usr/bin/env python3
"""
Test the Yoast Premium REST API payload format
Shows the correct meta structure for HTTP Request node → WordPress REST API
"""

import sys
import json
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

from wordpress_taxonomy_ids import build_webhook_payload

def test_yoast_premium_format():
    """Test payload format for Yoast Premium REST API"""

    print("=" * 70)
    print("YOAST PREMIUM REST API PAYLOAD FORMAT")
    print("=" * 70)
    print()

    # Build payload with Yoast meta
    payload = build_webhook_payload(
        title="Why Your South Jersey Home Equity Still Puts You Way Ahead",
        content="<p>South Jersey homeowners have built substantial equity...</p>",
        excerpt="",
        categories=['For Buyers', 'Housing Market Updates'],
        tags=['Home Equity', 'Home Value', 'Real Estate Market'],
        featured_media_id=12345,
        yoast_meta={
            'yoast_wpseo_focuskw': 'South Jersey home equity value',
            'yoast_wpseo_title': 'Home Equity Guide | South Jersey',
            'yoast_wpseo_metadesc': 'Despite market shifts, South Jersey homeowners maintain strong equity positions. Learn why your equity still gives you an advantage.'
        }
    )

    # Wrap in 'body' for n8n
    wrapped_payload = {'body': payload}

    print("PAYLOAD SENT TO N8N WEBHOOK:")
    print("-" * 70)

    # Show full payload (abbreviated content)
    display_payload = wrapped_payload.copy()
    display_payload['body'] = {**payload}
    display_payload['body']['content'] = f"<{len(payload['content'])} chars of HTML>"

    print(json.dumps(display_payload, indent=2))
    print()

    print("=" * 70)
    print("YOAST META STRUCTURE (the important part):")
    print("=" * 70)
    print()
    print(json.dumps(payload.get('meta', {}), indent=2))
    print()

    print("=" * 70)
    print("WHAT N8N HTTP REQUEST NODE WILL SEND TO WORDPRESS:")
    print("=" * 70)
    print()
    print("Endpoint: POST /wp-json/wp/v2/posts")
    print()
    print("Body:")
    print(json.dumps({
        'title': payload['title'],
        'content': '<HTML content>',
        'categories': payload['categories'],
        'tags': payload['tags'],
        'featured_media': payload.get('featured_media'),
        'status': 'draft',
        'meta': payload.get('meta', {})
    }, indent=2))
    print()

    print("=" * 70)
    print("YOAST PREMIUM REST API FIELDS:")
    print("=" * 70)
    print()
    print("✅ _yoast_wpseo_focuskw:   Focus keyphrase for SEO")
    print("✅ _yoast_wpseo_title:     Custom SEO title (50-60 chars)")
    print("✅ _yoast_wpseo_metadesc:  Meta description (140-160 chars)")
    print()
    print("These fields are only available with Yoast Premium!")
    print("They must be sent in the 'meta' object as shown above.")
    print()

    print("=" * 70)
    print("VERIFICATION:")
    print("=" * 70)
    print()

    if 'meta' in payload:
        meta = payload['meta']
        print(f"✅ Meta object exists: {bool(meta)}")
        print(f"✅ Focus keyphrase: '{meta.get('_yoast_wpseo_focuskw', 'MISSING')}'")
        print(f"✅ SEO title: '{meta.get('_yoast_wpseo_title', 'MISSING')}'")
        print(f"✅ Meta description: '{meta.get('_yoast_wpseo_metadesc', 'MISSING')[:60]}...'")
    else:
        print("❌ Meta object missing - Yoast fields won't be saved!")

    print()

if __name__ == '__main__':
    test_yoast_premium_format()

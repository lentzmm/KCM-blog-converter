#!/usr/bin/env python3
"""
Test script to show the NEW payload format after fixing n8n compatibility issue.

The fix: Send category/tag NAMES (strings) instead of IDs (integers).
n8n's WordPress node handles the conversion from names to IDs internally.
"""

import sys
import json
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

from wordpress_taxonomy_ids import build_webhook_payload

def test_new_format():
    """Test the new payload format with category/tag names"""

    print("=" * 60)
    print("NEW PAYLOAD FORMAT (FIXED FOR N8N)")
    print("=" * 60)
    print()

    # Test data with category/tag NAMES
    categories = ['For Buyers', 'Housing Market Updates']
    tags = ['First Time Home Buyers', 'Buying Tips', 'Home Prices']

    print(f"Input categories (NAMES): {categories}")
    print(f"Input tags (NAMES): {tags}")
    print()

    # Build payload
    payload = build_webhook_payload(
        title="South Jersey First-Time Buyer Guide",
        content="<p>Test content for first-time buyers...</p>",
        excerpt="",
        categories=categories,
        tags=tags,
        featured_media_id=12345,
        yoast_meta={
            'yoast_wpseo_focuskw': 'South Jersey first time buyers',
            'yoast_wpseo_title': 'First-Time Buyers Guide | South Jersey',
            'yoast_wpseo_metadesc': 'Complete guide for first-time home buyers in South Jersey.'
        }
    )

    print("=" * 60)
    print("PAYLOAD STRUCTURE:")
    print("=" * 60)
    print(json.dumps(payload, indent=2))
    print()

    print("=" * 60)
    print("VALIDATION:")
    print("=" * 60)
    print(f"✓ Categories type: {type(payload['categories']).__name__}")
    print(f"✓ Categories value: {payload['categories']}")
    print(f"✓ Tags type: {type(payload['tags']).__name__}")
    print(f"✓ Tags value: {payload['tags']}")
    print()

    # Verify categories/tags are STRING arrays, not INTEGER arrays
    if payload['categories'] and isinstance(payload['categories'][0], str):
        print("✅ Categories are STRINGS (names) - n8n can handle this")
    elif payload['categories'] and isinstance(payload['categories'][0], int):
        print("❌ Categories are INTEGERS (IDs) - this causes n8n error")
    else:
        print("⚠️  Categories are empty")

    if payload['tags'] and isinstance(payload['tags'][0], str):
        print("✅ Tags are STRINGS (names) - n8n can handle this")
    elif payload['tags'] and isinstance(payload['tags'][0], int):
        print("❌ Tags are INTEGERS (IDs) - this causes n8n error")
    else:
        print("⚠️  Tags are empty")
    print()

    print("=" * 60)
    print("EXPLANATION:")
    print("=" * 60)
    print("BEFORE FIX: Payload had categories: [881, 884] (integer IDs)")
    print("            This caused n8n error: 'Cannot read properties of undefined (reading tags)'")
    print()
    print("AFTER FIX:  Payload has categories: ['For Buyers', 'Housing Market Updates'] (string names)")
    print("            n8n's WordPress node converts names to IDs internally")
    print("            This matches what n8n expects and should work correctly")
    print()

if __name__ == '__main__':
    test_new_format()

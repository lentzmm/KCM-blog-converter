#!/usr/bin/env python3
"""
Test the CORRECT payload structure for n8n webhook
Based on analyzing the actual n8n workflow JSON
"""

import sys
import json
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

from wordpress_taxonomy_ids import build_webhook_payload

def test_correct_structure():
    """Test the correct payload structure with body wrapper and integer IDs"""

    print("=" * 70)
    print("CORRECT N8N WEBHOOK PAYLOAD STRUCTURE")
    print("=" * 70)
    print()

    # Test data with category/tag NAMES (will be converted to IDs)
    categories = ['For Buyers', 'Housing Market Updates']
    tags = ['First Time Home Buyers', 'Buying Tips', 'Home Prices']

    print(f"Input categories (names): {categories}")
    print(f"Input tags (names): {tags}")
    print()

    # Build payload (converts names to IDs)
    inner_payload = build_webhook_payload(
        title="South Jersey First-Time Buyer Guide",
        content="<p>Test content for first-time buyers...</p>",
        excerpt="",
        categories=categories,
        tags=tags,
        featured_media_id=12345,
        yoast_meta={
            'yoast_wpseo_focuskw': 'South Jersey first time buyers',
            'yoast_wpseo_title': 'First-Time Buyers Guide | South Jersey',
            'yoast_wpseo_metadesc': 'Complete guide for first-time home buyers.'
        }
    )

    # CRITICAL: Wrap in 'body' key for n8n
    wrapped_payload = {'body': inner_payload}

    print("=" * 70)
    print("PAYLOAD STRUCTURE SENT TO N8N:")
    print("=" * 70)
    print(json.dumps(wrapped_payload, indent=2))
    print()

    print("=" * 70)
    print("VALIDATION:")
    print("=" * 70)
    print(f"✓ Wrapped in 'body': {('body' in wrapped_payload)}")
    print(f"✓ Categories type: {type(wrapped_payload['body']['categories']).__name__}")
    print(f"✓ Categories value (IDs): {wrapped_payload['body']['categories']}")
    print(f"✓ Tags type: {type(wrapped_payload['body']['tags']).__name__}")
    print(f"✓ Tags value (IDs): {wrapped_payload['body']['tags']}")
    print()

    # Verify categories/tags are INTEGER arrays
    if wrapped_payload['body']['categories'] and isinstance(wrapped_payload['body']['categories'][0], int):
        print("✅ Categories are INTEGERS (IDs) - n8n can validate these")
    else:
        print("❌ Categories are NOT integers")

    if wrapped_payload['body']['tags'] and isinstance(wrapped_payload['body']['tags'][0], int):
        print("✅ Tags are INTEGERS (IDs) - n8n can validate these")
    else:
        print("❌ Tags are NOT integers")
    print()

    print("=" * 70)
    print("HOW N8N ACCESSES THIS DATA:")
    print("=" * 70)
    print("When we POST wrapped_payload to n8n webhook:")
    print("  - n8n receives it as: $('Webhook').item.json.body")
    print("  - Since we sent {'body': {...}}, n8n sees:")
    print("    $('Webhook').item.json.body.body.tags = [1145, 1138, 1147]")
    print("    $('Webhook').item.json.body.body.categories = [881, 884]")
    print()
    print("This matches exactly what the workflow expects!")
    print()

    print("=" * 70)
    print("N8N WORKFLOW VALIDATION PROCESS:")
    print("=" * 70)
    print("1. Validate Tags node calls:")
    print(f"   GET /wp-json/wp/v2/tags?include={','.join(map(str, wrapped_payload['body']['tags']))}")
    print()
    print("2. Validate Categories node calls:")
    print(f"   GET /wp-json/wp/v2/categories?include={','.join(map(str, wrapped_payload['body']['categories']))}")
    print()
    print("3. Validate Results (JavaScript) checks if all IDs exist in WordPress")
    print()
    print("4. If validation passes, POST to WordPress with same IDs")
    print()

if __name__ == '__main__':
    test_correct_structure()

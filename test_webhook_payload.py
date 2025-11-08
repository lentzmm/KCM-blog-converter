"""
Test script to verify webhook payload structure
Run this to see exactly what would be sent to n8n
"""

import sys
from pathlib import Path

# Add shared folder to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))
from wordpress_taxonomy_ids import build_webhook_payload

# Test with sample data
test_title = "South Jersey First-Time Buyer Guide"
test_content = "<p>Test content</p>"
test_excerpt = ""
test_categories = ["For Buyers", "Camden County Real Estate"]
test_tags = ["First Time Home Buyers", "Buying Tips", "Home Prices"]
test_featured_media_id = 12345
test_yoast_meta = {
    'yoast_wpseo_focuskw': 'South Jersey first time buyers',
    'yoast_wpseo_title': 'First-Time Buyers Guide | South Jersey',
    'yoast_wpseo_metadesc': 'Complete guide for first-time home buyers in South Jersey.'
}

# Build payload
payload = build_webhook_payload(
    title=test_title,
    content=test_content,
    excerpt=test_excerpt,
    categories=test_categories,
    tags=test_tags,
    featured_media_id=test_featured_media_id,
    yoast_meta=test_yoast_meta
)

print("=" * 60)
print("WEBHOOK PAYLOAD TEST")
print("=" * 60)
print()
print("Input categories:", test_categories)
print("Input tags:", test_tags)
print()
print("=" * 60)
print("PAYLOAD STRUCTURE:")
print("=" * 60)
import json
print(json.dumps(payload, indent=2))
print()
print("=" * 60)
print("VALIDATION:")
print("=" * 60)
print(f"✓ Title: {payload.get('title')}")
print(f"✓ Status: {payload.get('status')}")
print(f"✓ Categories (IDs): {payload.get('categories')}")
print(f"✓ Tags (IDs): {payload.get('tags')}")
print(f"✓ Featured Media: {payload.get('featured_media')}")
print(f"✓ Yoast Meta: {payload.get('yoast_meta')}")
print()

if not payload.get('categories'):
    print("⚠️  WARNING: Categories list is EMPTY!")
if not payload.get('tags'):
    print("⚠️  WARNING: Tags list is EMPTY!")

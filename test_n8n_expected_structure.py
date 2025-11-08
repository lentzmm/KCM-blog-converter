#!/usr/bin/env python3
"""
Analyze what n8n expects based on the workflow JSON
"""

import json

# What n8n is accessing in the Validate Tags node:
# $('Webhook').item.json.body.body.tags.join(',')

# What n8n is accessing in the JavaScript validation (line 6):
# const requestedTags = $('Webhook').item.json.body.body.tags.length;

# This means the structure n8n expects is:
expected_structure = {
    "item": {
        "json": {
            "body": {
                "body": {  # <-- DOUBLE BODY!
                    "title": "Test Article",
                    "categories": [881, 884],  # INTEGER IDs
                    "tags": [1147, 1152],  # INTEGER IDs
                    "content": "<p>Test</p>",
                    "excerpt": "",
                    "status": "draft",
                    "featured_media": 12345,
                    "yoast_meta_description": "Test description",
                    "yoast_focus_keyword": "test keyword"
                }
            }
        }
    }
}

print("=" * 70)
print("WHAT N8N EXPECTS (from workflow analysis)")
print("=" * 70)
print()
print("n8n accesses: $('Webhook').item.json.body.body.tags")
print("             $('Webhook').item.json.body.body.categories")
print()
print("This means when we POST to the webhook, the JSON should be:")
print()

# When you POST to n8n webhook, the JSON body becomes item.json.body
# So if n8n accesses body.body.tags, we need to send:
payload_to_send = {
    "body": {
        "title": "Test Article",
        "categories": [881, 884],
        "tags": [1147, 1152],
        "content": "<p>Test</p>",
        "excerpt": "",
        "status": "draft",
        "featured_media": 12345,
        "yoast_meta_description": "Test description",
        "yoast_focus_keyword": "test keyword"
    }
}

print(json.dumps(payload_to_send, indent=2))
print()
print("=" * 70)
print("KEY FINDINGS:")
print("=" * 70)
print("1. n8n expects INTEGER IDs for categories/tags, not string names")
print("2. Payload must be wrapped in a 'body' key")
print("3. n8n validates IDs by calling WordPress API: /tags?include=ID1,ID2,ID3")
print("4. Error 'Cannot read properties of undefined (reading tags)' occurs")
print("   when payload structure is flat instead of wrapped")
print()
print("CURRENT BUG: We're sending payload directly, not wrapped in 'body'")
print("FIX: Wrap payload in {'body': payload} before sending to n8n")

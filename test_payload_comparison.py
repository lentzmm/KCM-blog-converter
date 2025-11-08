"""
Quick test: Create a payload with EMPTY categories/tags like the old buggy code
This will help us see if n8n expects empty arrays
"""

test_payload_old_style = {
    "title": "Test Article",
    "content": "<p>Test</p>",
    "excerpt": "",
    "status": "draft",
    "categories": [],  # EMPTY like old buggy code
    "tags": [],  # EMPTY like old buggy code
    "featured_media": None,
    "yoast_meta": {
        "yoast_wpseo_focuskw": "test keyphrase",
        "yoast_wpseo_title": "Test Title",
        "yoast_wpseo_metadesc": "Test description"
    }
}

test_payload_new_style = {
    "title": "Test Article",
    "content": "<p>Test</p>",
    "excerpt": "",
    "status": "draft",
    "categories": [881, 884],  # POPULATED with real IDs
    "tags": [1147, 1152],  # POPULATED with real IDs
    "featured_media": 12345,
    "yoast_meta": {
        "yoast_wpseo_focuskw": "test keyphrase",
        "yoast_wpseo_title": "Test Title",
        "yoast_wpseo_metadesc": "Test description"
    }
}

import json
print("OLD STYLE (empty arrays - was working):")
print(json.dumps(test_payload_old_style, indent=2))
print("\n" + "="*60 + "\n")
print("NEW STYLE (populated arrays - now failing):")
print(json.dumps(test_payload_new_style, indent=2))
print("\n" + "="*60 + "\n")
print("DIFFERENCE:")
print(f"Old categories: {test_payload_old_style['categories']}")
print(f"New categories: {test_payload_new_style['categories']}")
print(f"Old tags: {test_payload_old_style['tags']}")
print(f"New tags: {test_payload_new_style['tags']}")

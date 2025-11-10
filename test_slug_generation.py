#!/usr/bin/env python3
"""
Test slug generation for WordPress posts
"""
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

from wordpress_taxonomy_ids import build_webhook_payload

def test_slug_generation():
    """Test that slugs are generated correctly from titles"""

    test_cases = [
        {
            'title': 'Why Home Prices Are Rising in 2025',
            'expected_slug': 'why-home-prices-are-rising-in-2025'
        },
        {
            'title': 'First-Time Home Buyer\'s Guide',
            'expected_slug': 'first-time-home-buyer-s-guide'
        },
        {
            'title': 'How to Get Pre-Approved for a Mortgage!',
            'expected_slug': 'how-to-get-pre-approved-for-a-mortgage'
        },
        {
            'title': 'Market Update: Q1 2025',
            'expected_slug': 'market-update-q1-2025'
        }
    ]

    print("=" * 70)
    print("SLUG GENERATION TEST")
    print("=" * 70)
    print()

    all_passed = True

    for i, test in enumerate(test_cases, 1):
        title = test['title']
        expected = test['expected_slug']

        # Build payload (slug will be auto-generated)
        payload = build_webhook_payload(
            title=title,
            content='<p>Test content</p>',
            excerpt='Test excerpt',
            categories=['For Buyers'],
            tags=['Buying Tips']
        )

        actual_slug = payload.get('slug', '')
        passed = actual_slug == expected

        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"Test {i}: {status}")
        print(f"  Title:    {title}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual_slug}")
        print()

        if not passed:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("✅ All tests PASSED!")
    else:
        print("❌ Some tests FAILED")
    print("=" * 70)

    return all_passed

if __name__ == '__main__':
    success = test_slug_generation()
    sys.exit(0 if success else 1)

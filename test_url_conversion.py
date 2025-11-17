#!/usr/bin/env python3
"""
Test case for URL conversion issue

The converter should:
1. Extract slug from simplifyingthemarket.com URL
2. Look up the slug in Notion database
3. Find the corresponding WordPress post and use its final URL

Example:
- Original: https://www.simplifyingthemarket.com/en/2025/11/13/would-you-let-80-a-month-hold-you-back-from-buying-a-home/?a=211199-eed154519afbfe4c41f1265fedb5efcd
- Slug: would-you-let-80-a-month-hold-you-back-from-buying-a-home
- Notion shows this slug maps to WordPress Post ID: 42565
- Final WordPress URL: https://mikesellsnj.com/why-small-rate-changes-shouldn-t-stop-your-south-jersey-home-purchase/
"""

import re
from typing import Dict


def migrate_kcm_links(html: str, slug_mapping: Dict[str, str] = None) -> str:
    """
    Standalone version of migrate_kcm_links for testing
    Migrate KCM links to MSNJ format using Notion database lookups
    """
    if slug_mapping is None:
        slug_mapping = {}

    # Pattern to match KCM links
    kcm_pattern = r'https?://www\.simplifyingthemarket\.com/en/\d{4}/\d{2}/\d{2}/([^/?]+)/?(?:\?[^"]*)?'

    replaced_count = 0
    not_found_count = 0

    def replace_link(match):
        nonlocal replaced_count, not_found_count
        slug = match.group(1)

        # Look up slug in Notion database
        if slug in slug_mapping:
            wp_url = slug_mapping[slug]
            print(f"  ✅ Replaced: {slug} -> {wp_url}")
            replaced_count += 1
            return wp_url
        else:
            # Fallback to simple slug-based URL if not in database
            fallback_url = f'https://mikesellsnj.com/{slug}/'
            print(f"  ⚠️  Slug not found, using fallback: {fallback_url}")
            not_found_count += 1
            return fallback_url

    modified_html = re.sub(kcm_pattern, replace_link, html)

    # Log summary
    total_count = replaced_count + not_found_count
    if total_count > 0:
        print(f"\n  Total: {total_count} links ({replaced_count} from database, {not_found_count} fallback)")

    return modified_html


def test_simplifyingthemarket_url_conversion():
    """
    Test that simplifyingthemarket.com URLs are converted using Notion database lookups
    """
    html_with_link = """
    <p>Check out this article:
    <a href="https://www.simplifyingthemarket.com/en/2025/11/13/would-you-let-80-a-month-hold-you-back-from-buying-a-home/?a=211199-eed154519afbfe4c41f1265fedb5efcd">
    Home Buying Tips</a></p>
    """

    # Mock slug mapping from Notion database
    slug_mapping = {
        "would-you-let-80-a-month-hold-you-back-from-buying-a-home": "https://mikesellsnj.com/why-small-rate-changes-shouldn-t-stop-your-south-jersey-home-purchase/"
    }

    print("Test Case: simplifyingthemarket.com URL conversion with Notion slug lookup")
    print("=" * 70)
    print(f"Input HTML:\n{html_with_link}")
    print(f"\nSlug Mapping (from Notion):")
    for slug, url in slug_mapping.items():
        print(f"  {slug} -> {url}")

    # Test with slug mapping (should use the final WordPress URL)
    result_with_mapping = migrate_kcm_links(html_with_link, slug_mapping)
    expected_url = "https://mikesellsnj.com/why-small-rate-changes-shouldn-t-stop-your-south-jersey-home-purchase/"

    print(f"\n✅ TEST WITH SLUG MAPPING:")
    if expected_url in result_with_mapping:
        print(f"  PASS: URL correctly replaced with final WordPress URL")
        print(f"  Result: {expected_url}")
    else:
        print(f"  FAIL: URL not replaced correctly")
        print(f"  Expected: {expected_url}")
        print(f"  Got: {result_with_mapping}")

    # Test without slug mapping (should use fallback)
    result_without_mapping = migrate_kcm_links(html_with_link, {})
    fallback_url = "https://mikesellsnj.com/would-you-let-80-a-month-hold-you-back-from-buying-a-home/"

    print(f"\n⚠️  TEST WITHOUT SLUG MAPPING (fallback):")
    if fallback_url in result_without_mapping:
        print(f"  PASS: URL uses fallback slug-based URL")
        print(f"  Result: {fallback_url}")
    else:
        print(f"  FAIL: Fallback not working")
        print(f"  Expected: {fallback_url}")
        print(f"  Got: {result_without_mapping}")

    print("\n" + "=" * 70)
    print("Test complete!")


if __name__ == "__main__":
    test_simplifyingthemarket_url_conversion()

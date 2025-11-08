"""
Link Replacer
Replaces KCM internal links with WordPress links using Notion database mappings
"""

import re
import logging
from typing import Dict, Tuple, List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def extract_kcm_links(html: str) -> List[str]:
    """
    Extract all KCM internal links from HTML

    Args:
        html: HTML content

    Returns:
        List of unique KCM URLs found
    """
    # Pattern to find <a href="...keepingcurrentmatters.com...">
    pattern = r'<a[^>]+href=["\']([^"\']*keepingcurrentmatters\.com[^"\']*)["\']'
    matches = re.findall(pattern, html, re.IGNORECASE)

    # Normalize URLs (remove fragments, query params for matching)
    normalized = []
    for url in matches:
        parsed = urlparse(url)
        # Keep scheme, netloc, and path only
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        # Remove trailing slash for consistency
        normalized_url = normalized_url.rstrip('/')
        normalized.append(normalized_url)

    unique_links = list(set(normalized))
    logger.info(f"Found {len(unique_links)} unique KCM internal links")
    return unique_links


def replace_kcm_links(html: str, url_mapping: Dict[str, str]) -> Tuple[str, Dict]:
    """
    Replace KCM internal links with WordPress links

    Args:
        html: HTML content with potential KCM links
        url_mapping: Dictionary mapping KCM URLs to WordPress URLs

    Returns:
        Tuple of (updated_html, stats_dict)
        stats_dict contains:
            - replaced: number of links replaced
            - not_found: list of KCM URLs not in mapping
            - total_kcm_links: total KCM links found
    """
    if not url_mapping:
        logger.warning("No URL mapping provided - skipping link replacement")
        return html, {"replaced": 0, "not_found": [], "total_kcm_links": 0}

    # Extract all KCM links
    kcm_links = extract_kcm_links(html)

    if not kcm_links:
        logger.info("No KCM internal links found in content")
        return html, {"replaced": 0, "not_found": [], "total_kcm_links": 0}

    replaced_count = 0
    not_found = []

    # Normalize the mapping keys for matching
    normalized_mapping = {}
    for kcm_url, wp_url in url_mapping.items():
        parsed = urlparse(kcm_url)
        normalized_key = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
        normalized_mapping[normalized_key] = wp_url

    # Replace each KCM link
    updated_html = html

    for kcm_url in kcm_links:
        if kcm_url in normalized_mapping:
            wp_url = normalized_mapping[kcm_url]

            # Replace all variations of this URL (with/without trailing slash, http/https)
            # Pattern matches the URL in href attributes
            variations = [
                kcm_url,
                kcm_url + '/',
                kcm_url.replace('https://', 'http://'),
                kcm_url.replace('http://', 'https://'),
                kcm_url.replace('https://', 'http://') + '/',
                kcm_url.replace('http://', 'https://') + '/'
            ]

            for variation in variations:
                # Escape special regex characters in URL
                escaped_url = re.escape(variation)
                pattern = f'(<a[^>]+href=["\']){escaped_url}(["\'][^>]*>)'
                replacement = f'\\1{wp_url}\\2'
                new_html = re.sub(pattern, replacement, updated_html, flags=re.IGNORECASE)

                if new_html != updated_html:
                    logger.info(f"Replaced: {variation} -> {wp_url}")
                    replaced_count += 1
                    updated_html = new_html

        else:
            not_found.append(kcm_url)
            logger.warning(f"⚠️  No WordPress URL found for: {kcm_url}")

    stats = {
        "replaced": replaced_count,
        "not_found": not_found,
        "total_kcm_links": len(kcm_links)
    }

    if not_found:
        logger.warning(f"⚠️  {len(not_found)} KCM links could not be replaced (not yet converted)")

    logger.info(f"Link replacement complete: {replaced_count} replaced, {len(not_found)} not found")

    return updated_html, stats

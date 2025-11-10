"""
WordPress Taxonomy IDs for MikeSellsNJ.com
Maps category and tag names to their WordPress IDs
Used for WordPress REST API and n8n webhook payloads
"""

# Category Name → ID Mapping
CATEGORY_IDS = {
    'Burlington County Real Estate': 1042,
    'Camden County Real Estate': 1031,
    'Cumberland County Real Estate': 1036,
    'For Buyers': 881,
    'For Sellers': 882,
    'Gloucester County Real Estate': 1038,
    'Housing Market Updates': 884,
    'Salem County Real Estate': 1039,
    'Uncategorized': 1,
}

# Tag Name → ID Mapping
TAG_IDS = {
    'Affordability': 1134,
    'Agent Value': 1135,
    'Alloway': 1092,
    'Audubon': 1061,
    'Baby Boomers': 1136,
    'Barrington': 1114,
    'Bellmawr': 1115,
    'Berlin': 1116,
    'Bridgeton': 1077,
    'Brooklawn': 1118,
    'Burlington Twp': 1068,
    'Buying Myths': 1137,
    'Buying Tips': 1138,
    'Carneys Point': 1086,
    'Cherry Hill': 1054,
    'Cinnaminson': 1069,
    'Clayton': 1053,
    'Clementon': 1119,
    'Collingswood': 1057,
    'Commercial Twp': 1078,
    'Deerfield': 1076,
    'Delran': 1070,
    'Demographics': 1139,
    'Deptford': 1045,
    'Distressed Properties': 1140,
    'Down Payments': 1141,
    'Downsize': 1142,
    'East Greenwich': 1049,
    'Eastampton': 1101,
    'Economy': 1143,
    'Elk Twp': 1124,
    'Elmer': 1091,
    'Equity': 1144,
    'First Time Home Buyers': 1145,
    'For Sale by Owner': 1162,
    'Forecasts': 1146,
    'Home Prices': 1147,
    'Home Staging': 1148,
    'Home Value': 1149,
    'Haddonfield': 1055,
    'Haddon Heights': 1056,
    'Inflation': 1150,
    'Inspection': 1151,
    'Interest Rates': 1152,
    'Investment Properties': 1153,
    'Millennials': 1154,
    'Moorestown': 1059,
    'Mortgage': 1155,
    'Mount Laurel': 1060,
    'Move Up Buyers': 1156,
    'Pricing Strategy': 1157,
    'Real Estate Market': 1158,
    'Selling Tips': 1159,
    'Spring Market': 1160,
    'Summer Market': 1161,
    'Voorhees': 1051,
    'Washington Twp': 1052,
    'Wenonah': 1125,
    'West Deptford': 1046,
    'Westville': 1126,
    'Woodbury': 1127,
    'Woodbury Heights': 1128,
}

def get_category_ids(category_names):
    """
    Convert list of category names to list of WordPress IDs

    Args:
        category_names: List of category name strings

    Returns:
        List of WordPress category IDs
    """
    ids = []
    for name in category_names:
        cat_id = CATEGORY_IDS.get(name)
        if cat_id:
            ids.append(cat_id)
    return ids

def get_tag_ids(tag_names):
    """
    Convert list of tag names to list of WordPress IDs

    Args:
        tag_names: List of tag name strings

    Returns:
        List of WordPress tag IDs
    """
    ids = []
    for name in tag_names:
        tag_id = TAG_IDS.get(name)
        if tag_id:
            ids.append(tag_id)
    return ids

def get_category_name_by_id(category_id):
    """
    Get category name by WordPress ID
    """
    for name, cat_id in CATEGORY_IDS.items():
        if cat_id == category_id:
            return name
    return None

def get_tag_name_by_id(tag_id):
    """
    Get tag name by WordPress ID
    """
    for name, t_id in TAG_IDS.items():
        if t_id == tag_id:
            return name
    return None

def build_webhook_payload(title, content, excerpt, categories, tags, featured_media_id=None, yoast_meta=None, slug=None):
    """
    Build n8n webhook payload for WordPress post creation

    Args:
        title: Post title
        content: Post HTML content
        excerpt: Post excerpt
        categories: List of category names
        tags: List of tag names
        featured_media_id: WordPress media ID for featured image
        yoast_meta: Dict with Yoast SEO metadata (yoast_wpseo_focuskw, yoast_wpseo_title, yoast_wpseo_metadesc)
        slug: URL-friendly slug (auto-generated from title if not provided)

    Returns:
        Dict ready for n8n webhook POST
    """
    # Auto-generate slug from title if not provided
    if not slug:
        import re
        # Convert to lowercase, replace spaces/special chars with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    payload = {
        'title': title,
        'content': content,
        'excerpt': excerpt,
        'slug': slug,
        'status': 'draft',
        'categories': get_category_ids(categories),
        'tags': get_tag_ids(tags),
    }

    if featured_media_id:
        payload['featured_media'] = featured_media_id

    # CRITICAL FIX v2.1: Send Yoast fields in n8n-compatible format
    # n8n expects field names: yoast_meta_description, yoast_focus_keyword, yoast_seo_title
    # n8n then sends them to WordPress as: meta[_yoast_wpseo_metadesc], meta[_yoast_wpseo_focuskw]
    if yoast_meta:
        # Focus keyphrase - send with n8n-compatible name
        focuskw = yoast_meta.get('yoast_wpseo_focuskw', '').strip()
        if focuskw:
            payload['yoast_focus_keyword'] = focuskw

        # Meta description - send with n8n-compatible name (don't send if it's a template string)
        metadesc = yoast_meta.get('yoast_wpseo_metadesc', '').strip()
        if metadesc and not metadesc.startswith('%%'):
            payload['yoast_meta_description'] = metadesc

        # SEO title - send with n8n-compatible name
        seo_title = yoast_meta.get('yoast_wpseo_title', '').strip()
        if seo_title:
            payload['yoast_seo_title'] = seo_title

    return payload

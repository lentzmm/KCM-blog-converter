"""
KCM to WordPress Category and Tag Mapping
Maps KeepingCurrentMatters.com taxonomy to MikeSellsNJ.com taxonomy
"""

# KCM Category → WordPress Category Mapping
KCM_TO_WP_CATEGORIES = {
    # KCM buyer-focused content
    'Homebuyer Tips': 'For Buyers',
    'Home Buying': 'For Buyers',
    'Buyer Tips': 'For Buyers',
    'Buying a Home': 'For Buyers',

    # KCM seller-focused content
    'Home Seller Tips': 'For Sellers',
    'Home Selling': 'For Sellers',
    'Seller Tips': 'For Sellers',
    'Selling a Home': 'For Sellers',

    # KCM market data
    'Market Updates': 'Housing Market Updates',
    'Housing Market': 'Housing Market Updates',
    'Real Estate Market': 'Housing Market Updates',
    'Market News': 'Housing Market Updates',
    'Market Data': 'Housing Market Updates',

    # Default catch-all
    'General': 'Housing Market Updates',
    'Real Estate': 'Housing Market Updates',
}

# KCM Tag → WordPress Tag Mapping
KCM_TO_WP_TAGS = {
    # Economic terms
    'Affordability': 'Affordability',
    'Home Prices': 'Home Prices',
    'Inflation': 'Inflation',
    'Economy': 'Economy',
    'Interest Rates': 'Interest Rates',
    'Mortgage Rates': 'Interest Rates',
    'Mortgage': 'Mortgage',

    # Buyer-related
    'First-Time Buyers': 'First Time Home Buyers',
    'First Time Buyers': 'First Time Home Buyers',
    'Millennials': 'Millennials',
    'Baby Boomers': 'Baby Boomers',
    'Down Payment': 'Down Payments',
    'Buying Myths': 'Buying Myths',
    'Buying Tips': 'Buying Tips',
    'Move-Up Buyers': 'Move Up Buyers',

    # Seller-related
    'Home Staging': 'Home Staging',
    'Home Value': 'Home Value',
    'Pricing': 'Pricing Strategy',
    'Selling Tips': 'Selling Tips',
    'FSBO': 'For Sale by Owner',

    # Property types
    'Investment': 'Investment Properties',
    'Investment Properties': 'Investment Properties',

    # Market terms
    'Forecast': 'Forecasts',
    'Market Trends': 'Real Estate Market',
    'Housing Market': 'Real Estate Market',
    'Spring Market': 'Spring Market',
    'Summer Market': 'Summer Market',

    # Process terms
    'Home Inspection': 'Inspection',
    'Equity': 'Equity',
    'Downsizing': 'Downsize',
    'Demographics': 'Demographics',
    'Distressed Properties': 'Distressed Properties',

    # Agent-related
    'Real Estate Agent': 'Agent Value',
    'Agent Value': 'Agent Value',
}

def map_kcm_category(kcm_category):
    """
    Map a KCM category name to WordPress category name

    Args:
        kcm_category: KCM category name string

    Returns:
        WordPress category name or default 'Housing Market Updates'
    """
    return KCM_TO_WP_CATEGORIES.get(kcm_category, 'Housing Market Updates')

def map_kcm_categories(kcm_categories):
    """
    Map multiple KCM categories to WordPress categories

    Args:
        kcm_categories: List of KCM category names

    Returns:
        List of WordPress category names (deduplicated)
    """
    wp_categories = set()
    for kcm_cat in kcm_categories:
        wp_cat = map_kcm_category(kcm_cat)
        wp_categories.add(wp_cat)
    return list(wp_categories)

def map_kcm_tag(kcm_tag):
    """
    Map a KCM tag name to WordPress tag name

    Args:
        kcm_tag: KCM tag name string

    Returns:
        WordPress tag name or None if no mapping exists
    """
    return KCM_TO_WP_TAGS.get(kcm_tag)

def map_kcm_tags(kcm_tags):
    """
    Map multiple KCM tags to WordPress tags

    Args:
        kcm_tags: List of KCM tag names

    Returns:
        List of WordPress tag names (deduplicated, None values filtered out)
    """
    wp_tags = set()
    for kcm_tag in kcm_tags:
        wp_tag = map_kcm_tag(kcm_tag)
        if wp_tag:
            wp_tags.add(wp_tag)
    return list(wp_tags)

def get_default_category():
    """
    Returns the default WordPress category for unmapped content
    """
    return 'Housing Market Updates'

def get_default_tags():
    """
    Returns default WordPress tags for general real estate content
    """
    return ['Real Estate Market']

def parse_kcm_recommendations(text):
    """
    Parse category and tag recommendations from Claude's response

    Args:
        text: String containing category/tag recommendations

    Returns:
        dict with 'categories' and 'tags' lists
    """
    result = {'categories': [], 'tags': []}

    # Simple parsing - look for lines with categories/tags
    lines = text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if 'categor' in line.lower():
            current_section = 'categories'
        elif 'tag' in line.lower():
            current_section = 'tags'
        elif line.startswith('-') or line.startswith('*'):
            # Extract the item
            item = line.lstrip('-*').strip()
            if current_section and item:
                result[current_section].append(item)

    return result

def merge_taxonomy(categories1, tags1, categories2=None, tags2=None):
    """
    Merge two sets of categories and tags, removing duplicates

    Args:
        categories1: List of category names
        tags1: List of tag names
        categories2: Optional second list of categories
        tags2: Optional second list of tags

    Returns:
        dict with merged 'categories' and 'tags' lists
    """
    merged_categories = set(categories1 or [])
    merged_tags = set(tags1 or [])

    if categories2:
        merged_categories.update(categories2)
    if tags2:
        merged_tags.update(tags2)

    return {
        'categories': list(merged_categories),
        'tags': list(merged_tags)
    }

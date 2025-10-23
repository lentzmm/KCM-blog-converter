"""
WordPress Taxonomy Definitions for MikeSellsNJ.com
Contains categories and tags for blog post classification
"""

# WordPress Categories
CATEGORIES = {
    'Burlington County Real Estate': {'id': 1042, 'slug': 'burlington-county-real-estate'},
    'Camden County Real Estate': {'id': 1031, 'slug': 'camden-county-real-estate'},
    'Cumberland County Real Estate': {'id': 1036, 'slug': 'cumberland-county-real-estate'},
    'For Buyers': {'id': 881, 'slug': 'for-buyers'},
    'For Sellers': {'id': 882, 'slug': 'for-sellers'},
    'Gloucester County Real Estate': {'id': 1038, 'slug': 'gloucester-county-real-estate'},
    'Housing Market Updates': {'id': 884, 'slug': 'housing-market-updates'},
    'Salem County Real Estate': {'id': 1039, 'slug': 'salem-county-real-estate'},
    'Uncategorized': {'id': 1, 'slug': 'uncategorized'},
}

# WordPress Tags (subset of most commonly used)
TAGS = {
    'Affordability': {'id': 1134, 'slug': 'affordability'},
    'Agent Value': {'id': 1135, 'slug': 'agent-value'},
    'Baby Boomers': {'id': 1136, 'slug': 'baby-boomers'},
    'Buying Myths': {'id': 1137, 'slug': 'buying-myths'},
    'Buying Tips': {'id': 1138, 'slug': 'buying-tips'},
    'Cherry Hill': {'id': 1054, 'slug': 'cherry-hill'},
    'Collingswood': {'id': 1057, 'slug': 'collingswood'},
    'Demographics': {'id': 1139, 'slug': 'demographics'},
    'Distressed Properties': {'id': 1140, 'slug': 'distressed-properties'},
    'Down Payments': {'id': 1141, 'slug': 'down-payments'},
    'Downsize': {'id': 1142, 'slug': 'downsize'},
    'Economy': {'id': 1143, 'slug': 'economy'},
    'Equity': {'id': 1144, 'slug': 'equity'},
    'First Time Home Buyers': {'id': 1145, 'slug': 'first-time-home-buyers'},
    'For Sale by Owner': {'id': 1162, 'slug': 'for-sale-by-owner'},
    'Forecasts': {'id': 1146, 'slug': 'forecasts'},
    'Home Prices': {'id': 1147, 'slug': 'home-prices'},
    'Home Staging': {'id': 1148, 'slug': 'home-staging'},
    'Home Value': {'id': 1149, 'slug': 'home-value'},
    'Inflation': {'id': 1150, 'slug': 'inflation'},
    'Inspection': {'id': 1151, 'slug': 'inspection'},
    'Interest Rates': {'id': 1152, 'slug': 'interest-rates'},
    'Investment Properties': {'id': 1153, 'slug': 'investment-properties'},
    'Millennials': {'id': 1154, 'slug': 'millennials'},
    'Mortgage': {'id': 1155, 'slug': 'mortgage'},
    'Move Up Buyers': {'id': 1156, 'slug': 'move-up-buyers'},
    'Pricing Strategy': {'id': 1157, 'slug': 'pricing-strategy'},
    'Real Estate Market': {'id': 1158, 'slug': 'real-estate-market'},
    'Selling Tips': {'id': 1159, 'slug': 'selling-tips'},
    'Spring Market': {'id': 1160, 'slug': 'spring-market'},
    'Summer Market': {'id': 1161, 'slug': 'summer-market'},
}

def get_categories_prompt():
    """
    Returns a formatted string of categories for Claude AI prompt
    """
    categories_list = []
    for name, data in CATEGORIES.items():
        categories_list.append(f"- {name}")

    return "\n".join(categories_list)

def get_tags_prompt():
    """
    Returns a formatted string of tags for Claude AI prompt
    """
    tags_list = []
    for name, data in TAGS.items():
        tags_list.append(f"- {name}")

    return "\n".join(tags_list)

def get_category_id(category_name):
    """
    Get WordPress category ID by name
    """
    return CATEGORIES.get(category_name, {}).get('id')

def get_tag_id(tag_name):
    """
    Get WordPress tag ID by name
    """
    return TAGS.get(tag_name, {}).get('id')

def get_all_category_names():
    """
    Returns list of all category names
    """
    return list(CATEGORIES.keys())

def get_all_tag_names():
    """
    Returns list of all tag names
    """
    return list(TAGS.keys())

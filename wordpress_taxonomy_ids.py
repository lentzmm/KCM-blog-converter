"""
WordPress Taxonomy ID Mappings
Maps category/tag names to WordPress numeric IDs for webhook payload
Generated from CSV files
"""

# Category Name -> ID mapping
CATEGORY_NAME_TO_ID = {
    "Burlington County Real Estate": 1042,
    "Camden County Real Estate": 1031,
    "Cumberland County Real Estate": 1036,
    "For Buyers": 881,
    "For Sellers": 882,
    "Gloucester County Real Estate": 1038,
    "Housing Market Updates": 884,
    "Salem County Real Estate": 1039,
    "Uncategorized": 1,
}

# Tag Name -> ID mapping (from CSV)
TAG_NAME_TO_ID = {
    "Affordability": 1134,
    "Agent Value": 1135,
    "Alloway": 1092,
    "April 2026": 1187,
    "April 2027": 1172,
    "April 2028": 1175,
    "Audubon": 1061,
    "August 2025": 1032,
    "August 2026": 1191,
    "August 2027": 1167,
    "August 2028": 1179,
    "Baby Boomers": 1136,
    "Barrington": 1114,
    "Bellmawr": 1115,
    "Berlin": 1116,
    "Bridgeton": 1077,
    "Brooklawn": 1118,
    "Burlington Twp": 1068,
    "Buying Myths": 1137,
    "Buying Tips": 1138,
    "Carneys Point": 1086,
    "Cherry Hill": 1054,
    "Cinnaminson": 1069,
    "Clayton": 1053,
    "Clementon": 1119,
    "Collingswood": 1057,
    "Commercial Twp": 1078,
    "December 2025": 1182,
    "December 2026": 1195,
    "December 2027": 1171,
    "Deerfield": 1076,
    "Delran": 1070,
    "Demographics": 1139,
    "Deptford": 1045,
    "Distressed Properties": 1140,
    "Down Payments": 1141,
    "Downsize": 1142,
    "East Greenwich": 1049,
    "Eastampton": 1101,
    "economy": 1143,
    "Elk Twp": 1124,
    "Elmer": 1091,
    "Equity": 1144,
    "February 2026": 1185,
    "February 2027": 1197,
    "February 2028": 1173,
    "First Time Home Buyers": 1145,
    "For Sale by Owner": 1162,
    "Forecasts": 1146,
    "Foreclosures": 1147,
    "Franklinville": 1050,
    "FSBOs": 1148,
    "Gibbstown": 1125,
    "Glassboro": 385,
    "Gloucester City": 1120,
    "Gloucester Twp": 55,
    "Haddon Heights": 1060,
    "Haddon Twp": 1059,
    "Haddonfirled": 1058,
    "Hainesport": 1093,
    "Home Buying Advice": 1149,
    "Home Prices": 1150,
    "home sales": 1035,
    "Infographics": 891,
    "Interest Rates": 1151,
    "Inventory": 1152,
    "January 2026": 1184,
    "January 2027": 1196,
    "January 2028": 1163,
    "July 2026": 1181,
    "July 2027": 1166,
    "July 2028": 1178,
    "June 2026": 1189,
    "June 2027": 1165,
    "June 2028": 1177,
    "Laurel Springs": 1121,
    "Lawnside": 1113,
    "Lindenwold": 1112,
    "Logan": 1048,
    "Lower Alloways Creek": 1088,
    "Lumberton": 1100,
    "Luxury / Vacation": 1161,
    "Magnolia": 1111,
    "Mantua": 9,
    "Maple Shade": 1071,
    "March 2026": 1186,
    "March 2027": 1198,
    "March 2028": 1174,
    "Marlton": 1063,
    "Maurice River": 1089,
    "May 2026": 1188,
    "May 2027": 1164,
    "May 2028": 1176,
    "Medford": 1066,
    "Medford Lakes": 1072,
    "Merchantville": 1110,
    "Millennials": 1153,
    "Millville": 1075,
    "Moorestown": 1065,
    "Mortgage Rates": 1154,
    "Mount Ephraim": 1109,
    "Mount Laurel": 1064,
    "Move-up Buyers": 1155,
    "Mullica Hill / Harrison Twp": 7,
    "National Park": 1126,
    "New Construction": 1156,
    "New Jersey real estate": 1033,
    "Newfield": 1127,
    "November 2025": 1190,
    "November 2026": 1194,
    "November 2027": 1170,
    "Oaklyn": 1108,
    "October 2025": 1183,
    "October 2026": 1193,
    "October 2027": 1169,
    "Palmyra": 1099,
    "Paulsboro": 1052,
    "Penns Grove": 1090,
    "Pennsauken": 1056,
    "Pennsville": 1084,
    "Pilesgrove": 1082,
    "Pine Hill": 1106,
    "Pitman": 386,
    "Pittsgrove": 1080,
    "Pricing": 1157,
    "real estate market": 1034,
    "Rent vs Buy": 890,
    "Riverside": 1098,
    "Riverton": 1097,
    "Runnemede": 1105,
    "Salem City": 1085,
    "Selling Myths": 1158,
    "Selling Tips": 1159,
    "Senior Market": 1160,
    "September 2025": 1040,
    "September 2026": 1192,
    "September 2027": 1168,
    "September 2028": 1180,
    "Shamong": 1096,
    "Sicklerville": 1062,
    "Somerdale": 1104,
    "Stratford": 1103,
    "Swedesboro": 1051,
    "Tabernacle": 1095,
    "Upper Deerfield": 1079,
    "Upper Pittsgrove": 1081,
    "Vineland": 1074,
    "Voorhees": 1055,
    "washington": 53,
    "Washington Twp": 11,
    "Waterford / Atco": 1102,
    "Wenonah": 13,
    "West Berlin": 1117,
    "West Deptford": 1046,
    "Westampton": 1094,
    "Westville": 1123,
    "Williamstown (Monroe Twp)": 54,
    "Willingboro": 1067,
    "Woodbury Heights": 12,
    "Woodstown": 1083,
    "Woolwich": 1047,
}


def get_category_ids(category_names: list) -> list:
    """
    Convert category names to WordPress IDs

    Args:
        category_names: List of category name strings

    Returns:
        List of category IDs (integers)
        Logs warnings for unmapped categories
    """
    ids = []
    unmapped = []

    for name in category_names:
        if name in CATEGORY_NAME_TO_ID:
            ids.append(CATEGORY_NAME_TO_ID[name])
        else:
            unmapped.append(name)

    if unmapped:
        print(f"⚠️ Warning: Unmapped categories: {unmapped}")

    return ids


def get_tag_ids(tag_names: list) -> list:
    """
    Convert tag names to WordPress IDs

    Args:
        tag_names: List of tag name strings

    Returns:
        List of tag IDs (integers)
        Logs warnings for unmapped tags
    """
    ids = []
    unmapped = []

    for name in tag_names:
        if name in TAG_NAME_TO_ID:
            ids.append(TAG_NAME_TO_ID[name])
        else:
            unmapped.append(name)

    if unmapped:
        print(f"⚠️ Warning: Unmapped tags: {unmapped}")

    return ids


def build_webhook_payload(metadata: dict, converted_html: str, featured_image_id: int = None) -> dict:
    """
    Build n8n webhook payload from metadata and HTML

    Args:
        metadata: Dict with categories, tags, seo_title, focus_keyphrase, meta_description
        converted_html: The localized blog HTML content
        featured_image_id: WordPress media ID for featured image (optional)

    Returns:
        Dict formatted for n8n webhook
    """
    # Convert names to IDs
    category_ids = get_category_ids(metadata.get('categories', []))
    tag_ids = get_tag_ids(metadata.get('tags', []))

    # Generate slug from title
    title = metadata.get('article_title', 'Untitled')
    slug = title.lower().replace(' ', '-').replace('/', '-')
    # Remove special characters
    import re
    slug = re.sub(r'[^a-z0-9-]', '', slug)

    # Build excerpt from meta description or first 160 chars of content
    excerpt = metadata.get('meta_description', '')
    if excerpt == '%%title%% %%sep%% %%sitename%% %%sep%% %%primary_category%%':
        # Extract text from HTML for excerpt
        text_content = re.sub(r'<[^>]+>', ' ', converted_html)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        excerpt = text_content[:160] + '...' if len(text_content) > 160 else text_content

    payload = {
        "body": {
            "title": title,
            "slug": slug,
            "content": converted_html,
            "excerpt": excerpt,
            "categories": category_ids,
            "tags": tag_ids,
            "yoast_focus_keyword": metadata.get('focus_keyphrase', ''),
            "yoast_meta_description": metadata.get('meta_description', '')
        }
    }

    # Add featured image if provided
    if featured_image_id:
        payload["body"]["featured_media"] = featured_image_id

    return payload


# Test function
if __name__ == "__main__":
    # Test payload building
    test_metadata = {
        "article_title": "Why South Jersey Home Prices Aren't Actually Flat",
        "categories": ["Housing Market Updates", "For Buyers"],
        "tags": ["Home Prices", "Inventory", "Cherry Hill", "Voorhees"],
        "focus_keyphrase": "South Jersey home prices",
        "seo_title": "South Jersey Home Prices | Market Update",
        "meta_description": "Understanding home price trends in South Jersey's real estate market."
    }

    test_html = "<h3>Test Blog Post</h3><p>This is test content for South Jersey real estate.</p>"

    payload = build_webhook_payload(test_metadata, test_html)

    import json
    print("Test Webhook Payload:")
    print(json.dumps(payload, indent=2))

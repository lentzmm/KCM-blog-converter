"""
WordPress Taxonomy Configuration for MikeSellsNJ.com
Auto-generated from CSV exports
"""

# WordPress Categories - Primary classification
WORDPRESS_CATEGORIES = [
    "Burlington County Real Estate",
    "Camden County Real Estate",
    "Cumberland County Real Estate",
    "For Buyers",
    "For Sellers",
    "Gloucester County Real Estate",
    "Housing Market Updates",
    "Salem County Real Estate",
]

# WordPress Tags - Organized by type for easier AI classification
WORDPRESS_TAGS = {
    # Geographic Tags - South Jersey Towns
    "geographic": [
        "Alloway", "Audubon", "Barrington", "Bellmawr", "Berlin", "Bridgeton",
        "Brooklawn", "Burlington Twp", "Carneys Point", "Cherry Hill", "Cinnaminson",
        "Clayton", "Clementon", "Collingswood", "Commercial Twp", "Deerfield",
        "Delran", "Deptford", "East Greenwich", "Eastampton", "Elk Twp", "Elmer",
        "Franklinville", "Gibbstown", "Glassboro", "Gloucester City", "Gloucester Twp",
        "Haddon Heights", "Haddon Twp", "Haddonfirled", "Hainesport", "Laurel Springs",
        "Lawnside", "Lindenwold", "Logan", "Lower Alloways Creek", "Lumberton",
        "Magnolia", "Mantua", "Maple Shade", "Marlton", "Maurice River", "Medford",
        "Medford Lakes", "Merchantville", "Millville", "Moorestown", "Mount Ephraim",
        "Mount Laurel", "Mullica Hill / Harrison Twp", "National Park", "Newfield",
        "Oaklyn", "Palmyra", "Paulsboro", "Penns Grove", "Pennsauken", "Pennsville",
        "Pilesgrove", "Pine Hill", "Pitman", "Pittsgrove", "Riverside", "Riverton",
        "Runnemede", "Salem City", "Shamong", "Sicklerville", "Somerdale", "Stratford",
        "Swedesboro", "Tabernacle", "Upper Deerfield", "Upper Pittsgrove", "Vineland",
        "Voorhees", "washington", "Washington Twp", "Waterford / Atco", "Wenonah",
        "West Berlin", "West Deptford", "Westampton", "Westville",
        "Williamstown (Monroe Twp)", "Willingboro", "Woodbury Heights", "Woodstown",
        "Woolwich",
    ],

    # Topic Tags - Real Estate Concepts
    "topics": [
        "Affordability", "Agent Value", "Buying Myths", "Buying Tips", "Demographics",
        "Distressed Properties", "Down Payments", "Downsize", "economy", "Equity",
        "First Time Home Buyers", "For Sale by Owner", "Forecasts", "Foreclosures",
        "FSBOs", "Home Buying Advice", "Home Prices", "home sales", "Infographics",
        "Interest Rates", "Inventory", "Luxury / Vacation", "Millennials",
        "Mortgage Rates", "Move-up Buyers", "New Construction", "New Jersey real estate",
        "Pricing", "real estate market", "Rent vs Buy", "Selling Myths", "Selling Tips",
        "Senior Market",
    ],

    # Demographic Tags
    "demographics": [
        "Baby Boomers", "Millennials", "First Time Home Buyers", "Move-up Buyers",
        "Senior Market",
    ],

    # Date Tags - Will be auto-generated based on publish date
    "dates": [
        "August 2025", "September 2025", "October 2025", "November 2025", "December 2025",
        "January 2026", "February 2026", "March 2026", "April 2026", "May 2026",
        "June 2026", "July 2026", "August 2026", "September 2026", "October 2026",
        "November 2026", "December 2026", "January 2027", "February 2027", "March 2027",
        "April 2027", "May 2027", "June 2027", "July 2027", "August 2027",
        "September 2027", "October 2027", "November 2027", "December 2027",
        "January 2028", "February 2028", "March 2028", "April 2028", "May 2028",
        "June 2028", "July 2028", "August 2028", "September 2028",
    ],
}

# Flatten all tags for AI prompt
ALL_TAGS_FLAT = []
for tag_group in WORDPRESS_TAGS.values():
    ALL_TAGS_FLAT.extend(tag_group)


def get_categories_prompt():
    """Return formatted list of categories for AI prompt"""
    return "\n".join([f"   - {cat}" for cat in WORDPRESS_CATEGORIES])


def get_tags_prompt():
    """Return formatted list of tags for AI prompt (organized by type)"""
    prompt = ""

    # Topic tags (most commonly used)
    prompt += "\n   Topic Tags:\n"
    prompt += "\n".join([f"     - {tag}" for tag in WORDPRESS_TAGS["topics"]])

    # Demographic tags
    prompt += "\n\n   Demographic Tags:\n"
    prompt += "\n".join([f"     - {tag}" for tag in WORDPRESS_TAGS["demographics"]])

    # Geographic tags (show a sample, not all 100+)
    prompt += "\n\n   Geographic Tags (towns - use when specific town is mentioned):\n"
    prompt += "     - Cherry Hill, Glassboro, Pitman, Washington Twp, Mullica Hill / Harrison Twp,\n"
    prompt += "     - Voorhees, Deptford, Mantua, Woolwich, and 80+ other South Jersey towns\n"

    return prompt


def get_all_tags_list():
    """Return complete flat list of all available tags"""
    return ALL_TAGS_FLAT


def get_all_categories_list():
    """Return complete list of all available categories"""
    return WORDPRESS_CATEGORIES


# County to Category mapping helper
COUNTY_CATEGORY_MAP = {
    "burlington": "Burlington County Real Estate",
    "camden": "Camden County Real Estate",
    "cumberland": "Cumberland County Real Estate",
    "gloucester": "Gloucester County Real Estate",
    "salem": "Salem County Real Estate",
}

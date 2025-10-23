"""
KCM to WordPress Taxonomy Mapping
Maps KeepingCurrentMatters.com categories/tags to MikeSellsNJ.com WordPress taxonomy
"""

# KCM Category/Tag -> WordPress Category mapping
KCM_CATEGORY_MAP = {
    # KCM term (lowercase) -> WordPress Category
    "for sellers": "For Sellers",
    "sellers": "For Sellers",
    "for buyers": "For Buyers",
    "buyers": "For Buyers",
    "first-time buyers": "For Buyers",
    "first time buyers": "For Buyers",
    "market updates": "Housing Market Updates",
    "housing market": "Housing Market Updates",
    "market data": "Housing Market Updates",
}

# KCM Tag -> WordPress Tag mapping
KCM_TAG_MAP = {
    # KCM term (lowercase) -> WordPress Tag
    "first-time buyers": "First Time Home Buyers",
    "first time buyers": "First Time Home Buyers",
    "mortgage rates": "Mortgage Rates",
    "interest rates": "Interest Rates",
    "move-up": "Move-up Buyers",
    "move up": "Move-up Buyers",
    "moveup": "Move-up Buyers",
    "affordability": "Affordability",
    "buying tips": "Buying Tips",
    "selling tips": "Selling Tips",
    "home prices": "Home Prices",
    "pricing": "Pricing",
    "inventory": "Inventory",
    "equity": "Equity",
    "down payments": "Down Payments",
    "down payment": "Down Payments",
    "forecasts": "Forecasts",
    "foreclosures": "Foreclosures",
    "millennials": "Millennials",
    "baby boomers": "Baby Boomers",
    "boomers": "Baby Boomers",
    "demographics": "Demographics",
    "economy": "economy",
    "new construction": "New Construction",
    "infographics": "Infographics",
    "fsbo": "FSBOs",
    "fsbos": "FSBOs",
    "for sale by owner": "For Sale by Owner",
    "downsize": "Downsize",
    "downsizing": "Downsize",
    "senior market": "Senior Market",
    "seniors": "Senior Market",
    "home buying advice": "Home Buying Advice",
    "buyer advice": "Home Buying Advice",
    "rent vs buy": "Rent vs Buy",
    "renting": "Rent vs Buy",
    "selling myths": "Selling Myths",
    "buying myths": "Buying Myths",
    "distressed properties": "Distressed Properties",
    "luxury": "Luxury / Vacation",
    "vacation": "Luxury / Vacation",
    "agent value": "Agent Value",
}


def parse_kcm_recommendations(text: str) -> dict:
    """
    Parse KCM recommended categories/tags from pasted text

    Args:
        text: Raw text pasted from KCM (e.g., "For SellersFirst-Time BuyersMortgage Rates")
              Can be plain text or HTML with links

    Returns:
        dict with 'categories' and 'tags' lists mapped to WordPress taxonomy
    """
    if not text or not text.strip():
        return {"categories": [], "tags": []}

    import re

    # If HTML, extract text from links
    if '<a' in text.lower():
        # Extract text from anchor tags
        link_texts = re.findall(r'<a[^>]*>(.*?)</a>', text, re.IGNORECASE)
        if link_texts:
            text = ''.join(link_texts)

    # Clean up the text - remove extra whitespace/newlines
    text = re.sub(r'\s+', '', text.strip())

    # Known KCM terms (order matters - check longer terms first!)
    KCM_KNOWN_TERMS = [
        "First-Time Buyers",  # Will match: First-TimeBuyers, FirstTimeBuyers, First-Time Buyers
        "Move-Up Buyers",     # Will match: Move-UpBuyers, MoveUpBuyers, Move-Up, MoveUp
        "For Sellers",        # Will match: ForSellers, For Sellers
        "For Buyers",         # Will match: ForBuyers, For Buyers
        "Mortgage Rates",     # Will match: MortgageRates, Mortgage Rates
        "Interest Rates",     # Will match: InterestRates, Interest Rates
        "Buying Tips",        # Will match: BuyingTips, Buying Tips
        "Selling Tips",       # Will match: SellingTips, Selling Tips
        "Home Prices",        # Will match: HomePrices, Home Prices
        "Down Payments",      # Will match: DownPayments, DownPayment
        "Baby Boomers",       # Will match: BabyBoomers, Baby Boomers
        "New Construction",   # Will match: NewConstruction, New Construction
        "Senior Market",      # Will match: SeniorMarket, Senior Market
        "Agent Value",        # Will match: AgentValue, Agent Value
        "Market Updates",     # Will match: MarketUpdates, Market Updates
        "Home Buying",        # Will match: HomeBuying, Home Buying
        "Move-Up",            # Shorter version of Move-Up Buyers
        "Affordability",
        "Forecasts",
        "Foreclosures",
        "Millennials",
        "Demographics",
        "Economy",
        "Inventory",
        "Equity",
        "FSBOs",
        "Downsize",
        "Downsizing",
        "Infographics",
        "Pricing",
    ]

    # Extract all matching terms from the concatenated string
    found_terms = []
    remaining = text

    # Keep trying to match terms until we can't find any more
    while remaining:
        matched = False
        for term in KCM_KNOWN_TERMS:
            # Create pattern by removing spaces and hyphens
            pattern = term.replace(' ', '').replace('-', '')
            # Also remove hyphens from remaining text for comparison
            remaining_normalized = remaining.replace('-', '')

            if remaining_normalized.lower().startswith(pattern.lower()):
                # Calculate how many characters to consume from original text
                # We need to account for hyphens in the original
                chars_to_consume = len(pattern)
                consumed = 0
                for i, char in enumerate(remaining):
                    if char not in ['-', ' ']:
                        consumed += 1
                    if consumed >= chars_to_consume:
                        chars_to_consume = i + 1
                        break

                found_terms.append(term)
                remaining = remaining[chars_to_consume:]
                matched = True
                break

        if not matched:
            # Skip one character and try again
            if remaining:
                remaining = remaining[1:]
            else:
                break

    # Map to WordPress taxonomy
    wordpress_categories = []
    wordpress_tags = []

    for item in found_terms:
        item_lower = item.lower()

        # Check if it's a category
        if item_lower in KCM_CATEGORY_MAP:
            wp_cat = KCM_CATEGORY_MAP[item_lower]
            if wp_cat not in wordpress_categories:
                wordpress_categories.append(wp_cat)

        # Check if it's a tag
        if item_lower in KCM_TAG_MAP:
            wp_tag = KCM_TAG_MAP[item_lower]
            if wp_tag not in wordpress_tags:
                wordpress_tags.append(wp_tag)

    return {
        "categories": wordpress_categories,
        "tags": wordpress_tags,
        "kcm_original": found_terms  # For debugging
    }


def merge_taxonomy(kcm_parsed: dict, ai_generated: dict) -> dict:
    """
    Merge KCM recommendations with AI-generated taxonomy
    KCM recommendations take priority but are supplemented by AI suggestions

    Args:
        kcm_parsed: Result from parse_kcm_recommendations()
        ai_generated: Categories/tags from Claude AI

    Returns:
        Merged taxonomy dict
    """
    # Start with KCM categories
    categories = list(kcm_parsed.get("categories", []))

    # Add AI categories if not already present (max 3 total)
    for cat in ai_generated.get("categories", []):
        if cat not in categories and len(categories) < 3:
            categories.append(cat)

    # Start with KCM tags
    tags = list(kcm_parsed.get("tags", []))

    # Add AI tags if not already present (max 10 total)
    for tag in ai_generated.get("tags", []):
        if tag not in tags and len(tags) < 10:
            tags.append(tag)

    return {
        "categories": categories,
        "tags": tags,
        "source": {
            "kcm_count": len(kcm_parsed.get("categories", [])) + len(kcm_parsed.get("tags", [])),
            "ai_count": len([c for c in ai_generated.get("categories", []) if c not in categories]) +
                        len([t for t in ai_generated.get("tags", []) if t not in tags])
        }
    }


# Test examples
if __name__ == "__main__":
    # Test case 1: Your original example
    test1 = "For SellersFirst-Time BuyersMortgage RatesMove-UpAffordabilityBuying Tips"
    result1 = parse_kcm_recommendations(test1)
    print("Test 1:", test1)
    print("Result:", result1)
    print()

    # Test case 2: Example 2 from user
    test2 = "For BuyersFor SellersHome PricesMortgage RatesForecasts"
    result2 = parse_kcm_recommendations(test2)
    print("Test 2:", test2)
    print("Result:", result2)
    print()

    # Test case 3: Example 3 from user
    test3 = "For BuyersNew ConstructionAffordabilityBuying Tips"
    result3 = parse_kcm_recommendations(test3)
    print("Test 3:", test3)
    print("Result:", result3)
    print()

    # Test case 4: With HTML links (simulated)
    test4 = '<a href="#">For Buyers</a><a href="#">First-Time Buyers</a><a href="#">Mortgage Rates</a>'
    result4 = parse_kcm_recommendations(test4)
    print("Test 4 (HTML):", test4)
    print("Result:", result4)
    print()

    # Test merge
    ai_suggestions = {
        "categories": ["Housing Market Updates"],
        "tags": ["Home Prices", "Inventory", "Cherry Hill"]
    }
    merged = merge_taxonomy(result1, ai_suggestions)
    print("Merged with AI suggestions:")
    print(merged)

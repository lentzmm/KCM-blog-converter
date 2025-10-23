# Technical Requirements Guide

## PURPOSE
This guide ensures all content maintains proper HTML structure, preserves critical elements, and follows strict data integrity rules. These are non-negotiable technical requirements.

---

## 🔴 CRITICAL: HTML PRESERVATION RULES

### Rule 1: Preserve ALL Existing Internal Links
**NEVER modify, remove, or change ANY existing links**

✅ **CORRECT:**
Keep this exactly as-is:
```html
<a href="https://www.keepingcurrentmatters.com/original-article/">Learn more</a>
```

❌ **WRONG:**
DO NOT change to:
```html
<a href="https://yoursite.com/new-link/">Learn more</a>
```

**Why This Matters:**
- Breaks user experience
- Violates content agreement
- Can break tracking/analytics
- May violate attribution requirements

### Rule 2: Maintain Exact HTML Structure
Preserve all HTML elements exactly:
- Heading tags (h1, h2, h3, etc.)
- Paragraph tags (p)
- List structures (ul, ol, li)
- Image tags (img)
- Emphasis tags (strong, em)
- Link tags (a)

✅ **CORRECT:**
```html
<h2>Market Trends</h2>
<p>Home prices continue to rise.</p>
<ul>
  <li>Inventory remains low</li>
  <li>Demand stays high</li>
</ul>
```

❌ **WRONG:**
```html
**Market Trends**
Home prices continue to rise.
* Inventory remains low
* Demand stays high
```

### Rule 3: Keep WordPress-Compatible Formatting
All HTML must work in WordPress editor:
- No custom CSS inline (unless already present)
- No JavaScript
- Standard HTML tags only
- Proper nesting maintained

### Rule 4: Preserve All Image Tags and Attributes
Keep every image exactly as provided:

✅ **CORRECT:**
```html
<img src="https://kcm-cdn.com/image123.jpg" alt="Market graph" width="800" height="600" />
```

❌ **WRONG:**
- Removing images
- Changing src URLs
- Removing width/height attributes
- Removing existing alt text

**Note:** You CAN update alt text to include keyphrases if original alt text exists and updating it improves SEO.

---

## ⚡ CHARACTER REPLACEMENTS (MANDATORY)

### Em Dashes Must Be Replaced
Replace ALL variations of em dashes with regular hyphens.

**Find and Replace:**

| Character | Replace With |
|-----------|-------------|
| — (em dash) | - (hyphen) |
| &mdash; | - (hyphen) |
| – (en dash) | - (hyphen) |
| &ndash; | - (hyphen) |

**Examples:**

❌ **BEFORE:**
"Prices rose — up 12% from last year — and show no signs of slowing."

✅ **AFTER:**
"Prices rose - up 12% from last year - and show no signs of slowing."

❌ **BEFORE:**
"The market&mdash;especially in South Jersey&mdash;remains strong."

✅ **AFTER:**
"The market - especially in South Jersey - remains strong."

**Why This Matters:**
- Em dashes don't always render correctly in WordPress
- Can cause encoding issues
- Creates inconsistent formatting
- May break on mobile devices

### Other Character Considerations

**Smart Quotes (Generally Fine):**
- " and " (curly quotes) → Usually okay
- ' and ' (curly apostrophes) → Usually okay

**Special Characters (Keep As-Is):**
- © (copyright symbol)
- ® (registered trademark)
- ™ (trademark)
- $ (dollar sign)
- % (percent sign)

**Ampersands:**
- & in body text → Usually okay
- &amp; in HTML → Keep as-is

---

## 📊 DATA INTEGRITY REQUIREMENTS

### Rule 1: Price Points Must Be Accurate
**South Jersey Typical Range:** $300K - $600K

**Adjust based on specific town:**

| Town Tier | Typical Range |
|-----------|--------------|
| Luxury (Moorestown, Haddonfield) | $450K - $850K |
| Mid-Range (Cherry Hill, Voorhees) | $350K - $550K |
| Entry-Level (Williamstown, Sewell) | $250K - $400K |
| Rural (Franklinville, Elmer) | $200K - $350K |

**When Using Price Examples:**
- Must align with town mentioned
- Must align with context documents
- Never make up specific prices
- Use ranges when exact data unavailable

✅ **CORRECT:**
"A typical Moorestown colonial ranges from $500K to $700K."

❌ **WRONG:**
"That Moorestown colonial sold for $892,450." (too specific without verification)

### Rule 2: Statistics Must Be Verified
**ONLY use statistics from:**
1. Context documents provided
2. Official MLS data
3. NAR/CAR reports (if cited in context)
4. Government sources (if cited in context)

**NEVER:**
- Make up percentages
- Estimate growth rates
- Invent market statistics
- Extrapolate beyond data

✅ **CORRECT:**
"Camden County median prices rose 4.2% year-over-year, according to MLS data."
(Only if this stat is in context documents)

❌ **WRONG:**
"Experts predict 8% growth next year."
(Unless this prediction is in context documents)

### Rule 3: Geographic References Must Be Real
**Every location must be:**
- A real South Jersey municipality
- Named correctly per Town Naming Guide
- Actually in the region mentioned
- Consistent throughout article

✅ **CORRECT:**
"Homes in Washington Twp sell quickly."
"That Kresson Road property sold in three days."

❌ **WRONG:**
"Homes in Springfield Township sell quickly."
(There are multiple Springfield Townships in NJ - which one?)

"That property on Main Street sold fast."
(Every town has a Main Street - be specific)

### Rule 4: No Fabricated Examples
**Never create fictional scenarios without clear signals:**

❌ **WRONG:**
"Last Tuesday, a Voorhees split-level sold for $487,000 in two days with three offers."
(Too specific to be made up)

✅ **CORRECT:**
"Split-levels in Voorhees typically sell within a week when priced right."
(General statement, not specific fabrication)

✅ **ALSO CORRECT:**
"Imagine this: You list your Voorhees split-level Friday morning. By Monday, you have three offers."
(Clearly hypothetical with 'imagine')

---

## 🏗️ HTML STRUCTURE BEST PRACTICES

### Heading Hierarchy
Must follow logical order:

```html
<h1>Article Title</h1>
  <h2>Main Section</h2>
    <h3>Subsection</h3>
    <h3>Another Subsection</h3>
  <h2>Another Main Section</h2>
    <h3>Subsection</h3>
```

❌ **WRONG:**
```html
<h1>Title</h1>
<h3>Section</h3>  <!-- Skipped h2 -->
<h2>Later Section</h2>  <!-- Goes backward -->
```

### Paragraph Structure
Each paragraph should be wrapped in `<p>` tags:

✅ **CORRECT:**
```html
<p>First paragraph here.</p>
<p>Second paragraph here.</p>
```

❌ **WRONG:**
```html
First paragraph here.
<br><br>
Second paragraph here.
```

### List Structure
Use proper list markup:

✅ **CORRECT:**
```html
<ul>
  <li>First point</li>
  <li>Second point</li>
  <li>Third point</li>
</ul>
```

❌ **WRONG:**
```html
<p>- First point<br>
- Second point<br>
- Third point</p>
```

### Link Structure
Always include href and meaningful anchor text:

✅ **CORRECT:**
```html
<a href="https://example.com/article/">Read the complete guide</a>
```

❌ **WRONG:**
```html
<a href="https://example.com/article/">Click here</a>
<a href="#">Learn more</a>  <!-- Empty href -->
```

---

## 🔗 LINK HANDLING RULES

### Internal Links (Preserve)
**Definition:** Links to keepingcurrentmatters.com or the original content source

**Action:** Keep exactly as provided
- Do not modify URL
- Do not change anchor text (unless improving for local relevance)
- Do not remove

### External Links (Preserve)
**Definition:** Links to third-party websites

**Action:** Keep exactly as provided
- Do not modify URL
- Do not remove
- Do not change anchor text

### Adding New Links (Allowed)
You MAY add new internal links to YOUR website:
- Link to related articles on your blog
- Link to service pages
- Link to contact page
- Use descriptive anchor text

✅ **ALLOWED:**
```html
<p>Looking to <a href="https://yoursite.com/sell/">sell your home in South Jersey</a>?</p>
```

### Link Attribution (Required)
If original article includes attribution links, preserve them:

✅ **REQUIRED:**
```html
<p>Source: <a href="https://www.nar.realtor/research">National Association of Realtors</a></p>
```

---

## 📸 IMAGE HANDLING

### Preserve Existing Images
Keep all original images:
- Same src URL
- Same dimensions
- Same file names

### Update Alt Text (Allowed)
You MAY update alt text for SEO:

**BEFORE:**
```html
<img src="image.jpg" alt="Graph" />
```

**AFTER:**
```html
<img src="image.jpg" alt="South Jersey home prices graph showing 2020-2025 trends" />
```

### Add New Images (Allowed)
You MAY add new locally relevant images:
- Local market graphs
- Area photos
- Team photos
- Infographics

**Format:**
```html
<img src="your-image.jpg" alt="Description including keyphrase" width="800" height="600" />
```

---

## ⚠️ WORDPRESS-SPECIFIC REQUIREMENTS

### No Shortcodes (Unless Already Present)
Don't add WordPress shortcodes:
- [gallery]
- [caption]
- [embed]

Unless they already exist in the original.

### No Custom HTML
Avoid:
- `<div>` with custom classes
- `<span>` with inline styles
- `<script>` tags
- `<style>` tags
- `<iframe>` (unless already present)

### Standard Tags Only
Stick to:
- `<p>`, `<h1>`-`<h6>`
- `<ul>`, `<ol>`, `<li>`
- `<strong>`, `<em>`
- `<a>`, `<img>`
- `<blockquote>`

---

## 📋 QUALITY CONTROL CHECKLIST

Before finalizing any article:

### HTML Structure
- [ ] All original links preserved exactly
- [ ] HTML structure maintained (headings, paragraphs, lists)
- [ ] All image tags preserved
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] All paragraphs in `<p>` tags
- [ ] All lists use `<ul>` or `<ol>` tags

### Character Requirements
- [ ] ALL em dashes replaced with hyphens
- [ ] No &mdash; or &ndash; remaining
- [ ] Smart quotes preserved (they're okay)
- [ ] No encoding errors (like Ã©)

### Data Integrity
- [ ] All prices verified or use typical ranges
- [ ] All statistics from context documents
- [ ] All locations verified in Town Naming Guide
- [ ] No fabricated specific examples
- [ ] Price ranges match mentioned towns

### WordPress Compatibility
- [ ] No custom CSS inline
- [ ] No JavaScript
- [ ] Standard HTML tags only
- [ ] Proper list markup
- [ ] No shortcodes added

---

## 🚫 ABSOLUTE VIOLATIONS

**These will BREAK the article:**

1. Modifying ANY existing link
2. Removing original HTML structure
3. Using em dashes (— or &mdash;) anywhere
4. Making up statistics
5. Naming fake locations
6. Using non-existent street names
7. Creating specific price examples without verification
8. Breaking HTML with unclosed tags
9. Adding custom CSS/JavaScript
10. Removing attribution links

**These will KILL credibility:**

1. Wrong price ranges for mentioned towns
2. Statistics that don't match context docs
3. Locations that don't exist
4. Made-up street names
5. Fake specific examples
6. Inconsistent data
7. Unverified claims

---

## 🔍 VALIDATION PROCESS

### Step 1: HTML Validation
Run through basic checks:
- All opening tags have closing tags
- Attributes in quotes
- No broken links
- Images load properly

### Step 2: Character Check
Search for:
- "—" (em dash)
- "&mdash;"
- "–" (en dash)
- "&ndash;"

Replace ALL with "-"

### Step 3: Data Verification
Cross-reference:
- All statistics with context docs
- All price points with typical ranges
- All locations with Town Naming Guide
- All specific examples for accuracy

### Step 4: Link Audit
Verify:
- All original links present
- No modified URLs
- All new links are to YOUR site only
- Proper anchor text used

---

## 📐 FORMATTING STANDARDS

### Spacing
- Single space after periods
- No double spaces anywhere
- One blank line between paragraphs (handled by `<p>` tags)

### Capitalization
- Sentence case for headings (not TITLE CASE)
- Proper nouns capitalized
- Don't capitalize "real estate" or "home prices"

### Numbers
- Spell out one through nine
- Use numerals for 10+
- Always use numerals with % or $
- Use commas in numbers 1,000+

**Examples:**
- "Three bedrooms" (not "3 bedrooms")
- "Prices rose 12%" (not "twelve percent")
- "$450,000" (not "$450000")

### Lists
- Capitalize first word of each list item
- End with period only if complete sentences
- Be consistent within each list

---

## ✅ FINAL TECHNICAL CHECKLIST

Before delivery:

**HTML Requirements:**
- [ ] All original links exactly preserved
- [ ] HTML structure maintained
- [ ] All images preserved
- [ ] WordPress-compatible formatting
- [ ] Proper heading hierarchy
- [ ] No broken tags

**Character Requirements:**
- [ ] ALL em dashes replaced with hyphens
- [ ] No encoding errors
- [ ] Proper spacing (single space after periods)

**Data Requirements:**
- [ ] Price points accurate for mentioned towns
- [ ] All statistics from context documents
- [ ] All locations verified real and properly named
- [ ] No fabricated specific examples without clear signals

**Link Requirements:**
- [ ] All original links unchanged
- [ ] Any new links go to YOUR site only
- [ ] Attribution links preserved
- [ ] Descriptive anchor text used

---

## 🚀 REMEMBER

Technical requirements are non-negotiable. They ensure:
- Content displays properly
- Links work correctly
- Data is accurate
- Attribution is maintained
- WordPress compatibility

When in doubt, preserve the original. Don't modify unless explicitly allowed in this guide.

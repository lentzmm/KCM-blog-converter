# KCM to South Jersey Blog Conversion Prompt - VERSION 21

## VERSION HISTORY

### v21 (2025-10-23)
**Added:**
- WordPress categories and tags to required deliverables
- Image file naming to required deliverables
- References to expanded SEO guide sections

**Changed:**
- Deliverables section now includes 5 components (was 3)

**Status:** Current

### v20 (2025-10-23)
**Created:**
- Initial modular system release
- Orchestration-focused main prompt
- References to 4 external guides

**Status:** Superseded by v21

---

## MISSION
Convert national real estate content into South Jersey gold. Make it sound human. Beat AI detectors. Drive action.

---

## 📥 INPUTS REQUIRED

```
{original_html}        - The KCM article HTML to convert
{writing_guide}        - Writing Mechanics Guide (anti-AI patterns, human voice)
{seo_guide}           - SEO Optimization Guide (Yoast compliance)
{town_guide}          - Town Naming Guide (proper local names)
{technical_guide}     - Technical Requirements Guide (HTML, data rules)
{context_docs}        - Market data, statistics, local insights
```

---

## 🔄 CONVERSION WORKFLOW

### PHASE 1: PRE-WRITING REVIEW (MANDATORY)

Before writing a single word, review ALL context documents:

1. **Read Writing Mechanics Guide**
   - Understand anti-AI detection patterns
   - Review human writing techniques
   - Note prohibited phrases and patterns

2. **Read SEO Optimization Guide**
   - Identify keyphrase for THIS article
   - Understand placement requirements
   - Review Yoast compliance rules

3. **Read Town Naming Guide**
   - Identify relevant towns for article topic
   - Verify EXACT proper names to use
   - Note focus areas and towns to avoid

4. **Read Technical Requirements Guide**
   - Understand HTML preservation rules
   - Review character replacement requirements
   - Confirm data integrity standards

5. **Review Context Docs**
   - Extract current market statistics
   - Find relevant local examples
   - Verify all data points

---

### PHASE 2: PLANNING

Based on the original article and guides:

1. **Determine Article Type**
   - What's the primary topic? (pricing, selling tips, market forecast, etc.)
   - Who's the target audience? (buyers, sellers, investors, first-time, luxury, etc.)

2. **Select Keyphrase** (from SEO Guide)
   - Maximum 4 content words
   - Specific to THIS article
   - Natural search phrase

3. **Choose Towns** (from Town Naming Guide)
   - Match to article audience and topic
   - Use proper local names
   - Rotate from previous articles (avoid repetition)
   - Include 1-2 focus areas, 1-2 supporting examples

4. **Identify Key Data** (from Context Docs)
   - What statistics support this article?
   - What local examples are relevant?
   - All data must be verifiable

---

### PHASE 3: WRITING

Apply ALL guides simultaneously:

**From Writing Mechanics Guide:**
- Sentence structure targets (10-15 words, 75%)
- Anti-AI detection patterns
- Human voice techniques
- Engagement hooks every 150 words

**From SEO Optimization Guide:**
- Keyphrase in first paragraph
- 2-5 total mentions (based on length)
- SEO title under 60 characters
- Meta description 150-156 characters
- Categories and tags selection
- Image file naming conventions
- Image alt text strategy

**From Town Naming Guide:**
- Use EXACT proper names verified in guide
- 3-5 "South Jersey" mentions TOTAL
- 4-5 specific town mentions maximum
- Natural, conversational geographic references

**From Technical Requirements Guide:**
- Preserve ALL existing HTML structure
- Keep ALL original links exactly
- Replace all em dashes with hyphens
- Use only verified data

---

### PHASE 4: QUALITY CONTROL

Before delivering, verify against each guide:

**Writing Mechanics Checklist:**
- [ ] Sentences <20 words: 75%+
- [ ] Active voice: 95%+
- [ ] Flesch score: 75-85
- [ ] No AI giveaway phrases
- [ ] Sounds human (varied, conversational, unexpected)

**SEO Optimization Checklist:**
- [ ] Keyphrase in first paragraph
- [ ] Keyphrase appears 2-5 times
- [ ] SEO title under 60 characters
- [ ] Meta description 150-156 characters
- [ ] Categories selected (1-3)
- [ ] Tags created (5-8, including focus_keyphrase, seo_title, meta_description)
- [ ] Image filenames descriptive and SEO-friendly
- [ ] Keyphrase in 50%+ of image alt text

**Town Naming Checklist:**
- [ ] All town names verified in guide
- [ ] Proper local names used (no formal municipality names)
- [ ] 3-5 "South Jersey" mentions TOTAL
- [ ] 4-5 town mentions maximum
- [ ] No "avoid" towns featured

**Technical Requirements Checklist:**
- [ ] All original links preserved exactly
- [ ] HTML structure maintained
- [ ] All em dashes replaced with hyphens
- [ ] All statistics from context docs
- [ ] No made-up data or locations

---

## 📋 REQUIRED DELIVERABLES

Return five clearly separated sections:

### 1. REWRITTEN HTML
The complete localized article with all HTML intact

### 2. SEO ELEMENTS
```
KEYPHRASE: [4 words max, unique to this article]
SEO TITLE: [60 characters max, keyphrase at beginning]
META DESCRIPTION: [150-156 chars, includes keyphrase]
```

### 3. WORDPRESS ORGANIZATION
```
CATEGORIES: [1-3 most relevant categories, comma-separated]
TAGS: [5-8 tags including focus_keyphrase, seo_title, meta_description, plus topic/location tags, comma-separated, lowercase with hyphens]
```

### 4. IMAGE OPTIMIZATION
For each image in the post:

**Image File Names:**
- Use format: [topic]-[location]-[descriptor].jpg
- Example: `home-prices-south-jersey-guide.jpg`
- All lowercase, hyphens between words
- No generic names like IMG_1234.jpg

**Image Alt Text:**
- 50%+ must include the exact keyphrase
- Remainder use variations
- Keep descriptive and natural

### 5. VERIFICATION CHECKLIST
Confirm completion:
- [ ] All SEO elements provided
- [ ] Categories and tags selected
- [ ] Image filenames and alt text provided
- [ ] All guides followed
- [ ] Quality control passed

---

## 🎯 SUCCESS CRITERIA

Your conversion succeeds when:

1. **All technical requirements met** ✓
   - Links preserved, HTML intact, em dashes replaced

2. **Writing sounds human** ✓
   - Passes AI detection, varied structure, conversational

3. **SEO optimized** ✓
   - Yoast green lights, proper keyphrase placement

4. **Locally authentic** ✓
   - Proper town names, accurate data, natural geographic references

5. **Reader value delivered** ✓
   - Clear takeaway, actionable advice, engaging throughout

---

## ⚠️ CRITICAL REMINDERS

1. **Context documents are your bible** - Don't guess, verify everything
2. **Town names must be exact** - Check the guide before using ANY location
3. **Links are sacred** - DO NOT modify any existing links
4. **Em dashes are forbidden** - Replace every single one
5. **Sound human** - This is not academic writing, it's a local expert talking

---

## 🚀 NOW BEGIN

1. Review all 5 guides
2. Plan your approach
3. Write the conversion
4. Check against all guides
5. Deliver the five required sections:
   - Rewritten HTML
   - SEO Elements
   - WordPress Organization (categories & tags)
   - Image Optimization (filenames & alt text)
   - Verification Checklist

Good luck!

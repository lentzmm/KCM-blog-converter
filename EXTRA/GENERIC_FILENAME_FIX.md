# Generic Filename Fix - October 21, 2025

## Problem
Image filenames were showing as generic "article-south-jersey-1.png" instead of SEO-optimized names like "market-south-jersey-guide.png"

## Root Causes Identified

### 1. Claude Adding Extra Content
The ACTIVE prompt was asking Claude to return THREE sections:
1. Rewritten HTML
2. SEO Elements (keyphrase, title, meta description)
3. Image Alt Text Suggestions

This caused Claude to add markdown sections at the beginning and end:
- Beginning: `## OUTPUT` and `### 1. Rewritten HTML`
- End: `### 2. SEO Elements`, `### 3. Image Alt Text`, etc.

### 2. No H1 Tag in Converted HTML
The converted HTML didn't have an H1 tag, so `extract_article_slug()` couldn't extract the title, falling back to "article" as the slug.

### 3. Generic Slug → Generic Filenames
With slug = "article", the filename generation created:
- `article-south-jersey-guide.png`
- `article-south-jersey-2.png`
- `article-south-jersey-3.png`

## Fixes Applied

### Fix 1: Updated ACTIVE Prompt (lines 280-294)
Changed the "REQUIRED DELIVERABLES" section to explicitly tell Claude:

**OLD:**
```markdown
## OUTPUT
1. **Rewritten HTML** (the full localized post)
2. **SEO Elements** (keyphrase, title, meta description)
3. **Image Alt Text** (for all images)

Return these three sections clearly separated.
```

**NEW:**
```markdown
## OUTPUT REQUIREMENTS

**CRITICAL:** Return ONLY the rewritten HTML. No preamble, no explanation, no SEO sections, no code fences.

**DO NOT INCLUDE:**
- SEO elements (these are generated separately by the system)
- Image alt text suggestions (these are generated separately)
- Markdown headers like "## OUTPUT" or "### 1. Rewritten HTML"
- Code fences (```)
- Explanations or comments

**WHAT TO RETURN:**
Just the complete HTML content, starting with the first HTML tag and ending with the last HTML tag.
```

### Fix 2: Aggressive Markdown Cleanup (lines 846-873)

**Added cleanup for markdown headers at the BEGINNING:**
```python
# Remove any markdown headers at the beginning (# or ##)
while rewritten_html.strip().startswith('#'):
    lines = rewritten_html.strip().split('\n')
    # Find first line that doesn't start with #
    for i, line in enumerate(lines):
        if not line.strip().startswith('#'):
            rewritten_html = '\n'.join(lines[i:])
            break
```

**Added cleanup for markdown sections at the END:**
```python
end_section_patterns = [
    r'\n#+\s*(OUTPUT|SEO|IMAGE|KEYPHRASE|DELIVERABLE).*',
    r'\n###\s*\d+\..*',  # Numbered sections like "### 1. Rewritten HTML"
    r'\n##\s*\d+\..*'   # Numbered sections like "## 1. HTML"
]

for pattern in end_section_patterns:
    match = re.search(pattern, rewritten_html, re.IGNORECASE | re.DOTALL)
    if match:
        rewritten_html = rewritten_html[:match.start()]
        logger.info(f"Removed markdown section from converted HTML")
        break
```

### Fix 3: Improved Slug Extraction (lines 369-410)

**Now tries multiple sources in order:**
1. H1 tag (if present)
2. **H2 tag** (FIRST one found - catches article titles)
3. `<title>` tag
4. Fallback to "article"

**Added detailed logging:**
```python
logger.info(f"Extracted title from H2: {title[:60]}...")
logger.info(f"Final slug: {final_slug}")
```

## Expected Results

### For Article: "Is the South Jersey Housing Market Going To Crash?"

**Previous (broken):**
- Extracted slug: `article`
- Filenames:
  - `article-south-jersey-guide.png` ❌
  - `article-south-jersey-2.png` ❌
  - `article-south-jersey-3.png` ❌

**Now (fixed):**
- Extracted from H2: "Is the South Jersey Housing Market Going To Crash? Here's What Experts Say"
- Slug: `is-the-south-jersey-housing-market-going-to-c` (50 char limit)
- Keyword found: `market`
- Filenames:
  - `market-south-jersey-guide.png` ✅
  - `market-south-jersey-2.png` ✅
  - `market-south-jersey-3.png` ✅

## Testing Checklist

- [ ] Run conversion and check console logs for slug extraction
- [ ] Verify no markdown headers at beginning of converted HTML
- [ ] Verify no SEO sections at end of converted HTML
- [ ] Check image preview shows SEO-optimized filenames (not "article-south-jersey")
- [ ] Verify filenames match topic keywords from title

## Files Modified

1. **refined_kcm_prompt_ACTIVE.md** (lines 280-294)
   - Changed output requirements to ONLY return HTML
   - Explicitly told Claude NOT to include SEO sections

2. **kcm_converter_server.py**
   - `rewrite_blog_post()` (lines 846-873): Aggressive markdown cleanup
   - `extract_article_slug()` (lines 369-410): H2 tag support + detailed logging

## Next Steps

1. **Test the conversion** - Run a new blog post through the system
2. **Check console logs** - Look for messages like:
   ```
   Extracted title from H2: Is the South Jersey Housing Market...
   Final slug: is-the-south-jersey-housing-market-going-to-c
   Topic term for images: market, Geo term: south-jersey
   ```
3. **Verify preview** - Image filenames should show as `market-south-jersey-guide.png`, etc.
4. **If still broken** - The issue is that Claude is STILL ignoring the prompt instructions. We may need to add a post-processing step to extract ONLY HTML content between first `<` and last `>` tags.

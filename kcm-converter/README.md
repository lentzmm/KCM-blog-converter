# KCM Blog Conversion System v20 - README

## Overview

This is a modular prompt system for converting national KCM real estate articles into localized South Jersey content. The system is designed for use with Claude Code or similar tools that can reference multiple context documents.

---

## File Structure

### 1. **kcm_prompt_v20.md** (Main Orchestrator)
- **Purpose:** Main workflow and coordination
- **Size:** ~150 lines
- **Role:** Directs the AI to reference other guides at appropriate times
- **When to Update:** Only when workflow changes

### 2. **town_naming_guide.md** (Location Reference)
- **Purpose:** Complete South Jersey municipality naming conventions
- **Size:** ~400 lines
- **Role:** Ensures proper local names, prevents "Washington Township" errors
- **When to Update:** When service areas change or town preferences shift

### 3. **writing_mechanics_guide.md** (Voice & Style)
- **Purpose:** Anti-AI detection patterns, sentence structure, human voice
- **Size:** ~350 lines
- **Role:** Makes content sound like a local expert, not a robot
- **When to Update:** When new AI patterns emerge or voice preferences change

### 4. **seo_optimization_guide.md** (Yoast Compliance)
- **Purpose:** Keyphrase placement, title/meta requirements, image alt text
- **Size:** ~350 lines
- **Role:** Ensures Yoast green lights across all metrics
- **When to Update:** When SEO requirements or Yoast rules change

### 5. **technical_requirements_guide.md** (HTML & Data)
- **Purpose:** HTML preservation, character replacements, data integrity
- **Size:** ~300 lines
- **Role:** Maintains technical standards and prevents breaking changes
- **When to Update:** Rarely - only if WordPress or technical requirements change

---

## How It Works

### Single Prompt Call Structure

```
INPUT VARIABLES:
{original_html}        - The KCM article HTML
{writing_guide}        - Contents of writing_mechanics_guide.md
{seo_guide}           - Contents of seo_optimization_guide.md
{town_guide}          - Contents of town_naming_guide.md
{technical_guide}     - Contents of technical_requirements_guide.md
{context_docs}        - Current market data, MLS stats, etc.

PROMPT:
Contents of kcm_prompt_v20.md

OUTPUT:
1. Rewritten HTML
2. SEO Elements (keyphrase, title, meta description)
3. Image Alt Text suggestions
```

### Workflow

The main prompt (v20) instructs the AI to:

1. **Phase 1: Pre-Writing Review**
   - Read ALL guides
   - Understand requirements
   - Identify relevant sections

2. **Phase 2: Planning**
   - Determine article type
   - Select keyphrase
   - Choose appropriate towns
   - Identify supporting data

3. **Phase 3: Writing**
   - Apply all guides simultaneously
   - Maintain technical standards
   - Optimize for SEO
   - Sound human

4. **Phase 4: Quality Control**
   - Verify against each guide
   - Check all requirements
   - Confirm deliverables

---

## Advantages of Modular System

### 1. Maintainability
- Update one guide without touching others
- Version control individual components
- Easy to see what changed and why

### 2. Clarity
- Each guide has single responsibility
- No 600-line mega-prompt to wade through
- Find what you need quickly

### 3. Reusability
- Use writing guide for other content types
- Share SEO guide across projects
- Town guide useful for multiple purposes

### 4. Scalability
- Add new guides easily (e.g., neighborhood guide, school district guide)
- Remove guides not needed for specific use cases
- Mix and match as needed

### 5. Testing
- Test changes to one guide in isolation
- Roll back specific guide versions
- A/B test different approaches

---

## Using with Claude Code

### Basic Setup

```bash
# Store all guides in a project directory
/kcm-conversion/
  ├── kcm_prompt_v20.md
  ├── town_naming_guide.md
  ├── writing_mechanics_guide.md
  ├── seo_optimization_guide.md
  ├── technical_requirements_guide.md
  └── context_docs/
      ├── camden_county_2025_09.md
      ├── gloucester_county_2025_09.md
      └── market_stats_current.md
```

### Example Claude Code Command

```bash
claude-code convert-kcm \
  --prompt kcm_prompt_v20.md \
  --writing writing_mechanics_guide.md \
  --seo seo_optimization_guide.md \
  --towns town_naming_guide.md \
  --technical technical_requirements_guide.md \
  --context context_docs/*.md \
  --input original_article.html \
  --output converted_article.html
```

### Programmatic Usage

```python
# Example Python script structure
from claude_code import ClaudeAPI

def convert_kcm_article(original_html, context_files):
    # Load all guides
    main_prompt = load_file('kcm_prompt_v20.md')
    writing_guide = load_file('writing_mechanics_guide.md')
    seo_guide = load_file('seo_optimization_guide.md')
    town_guide = load_file('town_naming_guide.md')
    technical_guide = load_file('technical_requirements_guide.md')
    
    # Load context docs
    context_docs = '\n\n'.join([load_file(f) for f in context_files])
    
    # Build prompt with all context
    full_prompt = f"""
{main_prompt}

---

## WRITING MECHANICS GUIDE
{writing_guide}

---

## SEO OPTIMIZATION GUIDE
{seo_guide}

---

## TOWN NAMING GUIDE
{town_guide}

---

## TECHNICAL REQUIREMENTS GUIDE
{technical_guide}

---

## CONTEXT DOCUMENTS
{context_docs}

---

## ORIGINAL HTML TO CONVERT
{original_html}
"""
    
    # Send to Claude
    response = claude.complete(full_prompt)
    
    return response
```

---

## Update Workflow

### When to Update Each Guide

**Town Naming Guide:**
- New service areas added
- Town preferences change
- Focus areas shift
- Update frequency: Quarterly

**Writing Mechanics Guide:**
- New AI patterns detected
- Voice/tone preferences evolve
- Client feedback on style
- Update frequency: Semi-annually

**SEO Optimization Guide:**
- Yoast updates rules
- Google algorithm changes
- New ranking factors
- Update frequency: Annually or as needed

**Technical Requirements Guide:**
- WordPress version changes
- HTML standards evolve
- Platform changes
- Update frequency: Rarely

**Main Prompt (v20):**
- Workflow changes
- New guides added
- Process improvements
- Update frequency: As needed

### Version Control Best Practices

```bash
# Use semantic versioning for guides
town_naming_guide_v2.1.md  # Minor update: Added 2 towns
town_naming_guide_v3.0.md  # Major update: Restructured entire guide

# Date stamp main prompt versions
kcm_prompt_v20_2025-10-23.md
kcm_prompt_v21_2025-11-15.md

# Keep changelog
CHANGELOG.md
```

---

## Testing Checklist

Before deploying changes:

- [ ] Test with 3 different article types
- [ ] Verify all towns use proper names
- [ ] Check Yoast metrics achieve green lights
- [ ] Confirm HTML preserves all links
- [ ] Validate character replacements work
- [ ] Test readability scores hit 75-85
- [ ] Verify no AI detection flags
- [ ] Check keyphrase placement correct
- [ ] Confirm price ranges match towns
- [ ] Test with minimum (500 word) and maximum (2000 word) articles

---

## Troubleshooting

### Problem: Wrong town names being used
**Solution:** Verify `town_naming_guide.md` is being passed correctly and check for updates needed

### Problem: Content sounds robotic
**Solution:** Review `writing_mechanics_guide.md` - may need to add new AI patterns to avoid

### Problem: Yoast metrics not green
**Solution:** Check `seo_optimization_guide.md` requirements are being met, particularly keyphrase placement

### Problem: HTML structure broken
**Solution:** Review `technical_requirements_guide.md` - likely a preservation issue

### Problem: Made-up statistics appearing
**Solution:** Ensure `context_docs` are being passed and `technical_requirements_guide.md` data integrity rules are enforced

---

## Migration from v17/v18/v19

### Key Changes in v20

1. **Main Prompt:**
   - Reduced from 400+ lines to ~150 lines
   - Now orchestration-focused
   - References external guides

2. **Content Distribution:**
   - Writing rules → `writing_mechanics_guide.md`
   - SEO rules → `seo_optimization_guide.md`
   - Town names → `town_naming_guide.md`
   - HTML rules → `technical_requirements_guide.md`

3. **Benefits:**
   - Easier to update specific aspects
   - Better organization
   - Reduced cognitive load
   - Improved version control

### Migration Steps

1. **Backup old prompts:**
   ```bash
   cp kcm_prompt_v19.md archive/kcm_prompt_v19_backup.md
   ```

2. **Test v20 in parallel:**
   - Convert same article with v19 and v20
   - Compare outputs
   - Verify quality maintained or improved

3. **Deploy gradually:**
   - Start with low-stakes articles
   - Monitor quality metrics
   - Adjust guides as needed

4. **Document changes:**
   - Note any behavior differences
   - Update guides based on learnings
   - Share feedback with team

---

## Support & Feedback

### Common Questions

**Q: Can I use just some guides, not all?**
A: Yes, but quality may suffer. Minimum recommended: main prompt + town guide + technical guide.

**Q: Can I create additional guides?**
A: Absolutely! Consider adding:
- Neighborhood-specific guide
- School district guide
- Seasonal content guide
- Buyer persona guide

**Q: Do I need to pass all guides every time?**
A: Yes, for best results. The main prompt references all guides throughout the workflow.

**Q: Can I merge guides back into one file?**
A: You can, but you lose the maintainability benefits. Only do this if your tooling can't handle multiple files.

---

## Success Metrics

Track these to measure system performance:

### Quality Metrics
- [ ] AI detection pass rate: >95%
- [ ] Yoast green light rate: 100%
- [ ] Town name accuracy: 100%
- [ ] Link preservation: 100%
- [ ] Readability score: 75-85 range

### Efficiency Metrics
- [ ] Conversion time: <5 minutes per article
- [ ] Revisions needed: <1 per article
- [ ] Manual corrections: Minimal

### Output Metrics
- [ ] Articles published per week: [Your target]
- [ ] SEO ranking improvements: [Track over time]
- [ ] User engagement: [Track over time]

---

## Future Enhancements

### Planned
- [ ] Neighborhood-specific content guide
- [ ] School district reference guide
- [ ] Seasonal content adjustments guide
- [ ] Client persona targeting guide

### Under Consideration
- [ ] Automated quality checking script
- [ ] A/B testing framework for guide variations
- [ ] Integration with WordPress API for direct publishing
- [ ] Automated keyphrase suggestion based on article content

---

## Changelog

### v20 (2025-10-23)
- Initial modular system release
- Split monolithic prompt into 5 focused guides
- Added comprehensive town naming reference
- Enhanced anti-AI detection patterns
- Improved SEO optimization structure

### v19 (Previous)
- Added dynamic town selection strategy
- Fixed Washington Township → Washington Twp
- Attempted rotation rules

### v18 (Previous)
- Added anti-AI detection patterns
- Expanded geographic optimization

### v17 (Previous)
- Base working version
- Simple tier-based town selection

---

## Contact

For questions, suggestions, or issues with this system, consult your Claude Code documentation or refer to Anthropic's API documentation for implementation details.

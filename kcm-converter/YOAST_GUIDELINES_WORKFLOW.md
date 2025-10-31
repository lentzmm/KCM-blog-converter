# Yoast SEO Guidelines - Error Reporting & Update Workflow

**Purpose**: Clear workflow for reporting Yoast SEO errors and having Claude update the guidelines automatically.

---

## How This Works

**You provide** → **Claude analyzes** → **Claude updates** → **Claude tests**

1. **You encounter an error** in WordPress/Yoast SEO
2. **You report it to Claude** using the template below
3. **Claude determines the root cause** and which guideline needs updating
4. **Claude updates** `yoast_seo_guidelines.md` with the fix
5. **Claude commits & pushes** to GitHub
6. **Claude restarts** the Flask server
7. **You sync** via GitHub Desktop and test again

---

## Error Reporting Template

When you encounter a Yoast SEO error, copy and paste this template to Claude:

```
YOAST ERROR REPORT

1. WHAT HAPPENED:
[Describe what went wrong - e.g., "Focus keyphrase wasn't in WordPress draft"]

2. WHERE IT HAPPENED:
[WordPress post editor, Yoast SEO panel, draft preview, etc.]

3. WHAT YOU EXPECTED:
[What should have happened - e.g., "Focus keyphrase should appear in Yoast SEO panel"]

4. WHAT YOU SAW INSTEAD:
[Actual result - e.g., "Yoast SEO focus keyphrase field was empty"]

5. EXAMPLE (if applicable):
[The actual keyphrase generated, or screenshot description]

6. ADDITIONAL CONTEXT (optional):
[Any other relevant information]
```

---

## Example Error Reports

### Example 1: Missing Focus Keyphrase

```
YOAST ERROR REPORT

1. WHAT HAPPENED:
Focus keyphrase was generated but not inserted to WordPress post draft

2. WHERE IT HAPPENED:
WordPress post editor, Yoast SEO panel

3. WHAT YOU EXPECTED:
The focus keyphrase "South Jersey home equity" should appear in the Yoast SEO focus keyphrase field

4. WHAT YOU SAW INSTEAD:
Yoast SEO focus keyphrase field was empty/blank

5. EXAMPLE:
Generated keyphrase: "South Jersey home equity"
WordPress draft: keyphrase field was empty

6. ADDITIONAL CONTEXT:
The keyphrase showed up in the conversion results, but didn't make it to WordPress
```

**Claude's Response:**
- Analyzes the webhook payload code
- Identifies the missing `yoast_wpseo_focuskw` field
- Updates `yoast_seo_guidelines.md` with technical implementation details
- Fixes the server code
- Commits, pushes, and restarts

---

### Example 2: SEO Title Too Long

```
YOAST ERROR REPORT

1. WHAT HAPPENED:
SEO title is too long and shows orange/red light in Yoast

2. WHERE IT HAPPENED:
WordPress post editor, Yoast SEO panel title field

3. WHAT YOU EXPECTED:
SEO title should be 50-60 characters (green light in Yoast)

4. WHAT YOU SAW INSTEAD:
SEO title was 75 characters, Yoast showed orange warning

5. EXAMPLE:
Generated title: "Understanding Home Equity Options for South Jersey Homeowners in 2025" (75 chars)
Should be: "Home Equity Guide | South Jersey" (35 chars)

6. ADDITIONAL CONTEXT:
This happened on 3 out of 5 articles today
```

**Claude's Response:**
- Updates `yoast_seo_guidelines.md` with stricter character limits
- Updates prompt to emphasize 50-60 character maximum
- Adds examples of good vs bad titles
- May adjust the AI generation prompt for SEO titles

---

### Example 3: Town Tags Incorrect

```
YOAST ERROR REPORT

1. WHAT HAPPENED:
Article tagged "Cherry Hill" but Cherry Hill was never mentioned in the content

2. WHERE IT HAPPENED:
WordPress tags section

3. WHAT YOU EXPECTED:
Only towns mentioned 2+ times in content should be tagged

4. WHAT YOU SAW INSTEAD:
Cherry Hill tag was added, but "Cherry Hill" only appears 0 times in article

5. EXAMPLE:
Article mentions: Haddonfield (3x), Voorhees (2x), Moorestown (1x)
Tags applied: Cherry Hill, Haddonfield, Voorhees, Moorestown

6. ADDITIONAL CONTEXT:
Cherry Hill appears in almost every article even when not mentioned
```

**Claude's Response:**
- Updates `yoast_seo_guidelines.md` Section 6 (Town Randomization Rules)
- Strengthens the "ONLY tag towns mentioned 2+ times" rule
- Updates prompt with explicit counting logic
- May add validation code to check tag accuracy

---

## What Claude Will Update

Based on your error report, Claude will update one or more sections:

| Error Type | Guidelines Section | Likely Updates |
|-----------|-------------------|----------------|
| Focus Keyphrase Issues | Section 1 + Section 9 | Requirements, technical implementation |
| SEO Title Problems | Section 2 | Character limits, format examples |
| Meta Description Issues | Section 3 | Length requirements, template usage |
| Category Selection Wrong | Section 4 | Selection guidelines, examples |
| Tag Problems | Section 5 | Tag requirements, available tags |
| Town Randomization | Section 6 | Randomization rules, tagging logic |
| Image Alt Text Issues | Section 7 | Keyphrase requirements, format |
| Content Optimization | Section 8 | Checklist items, verification steps |
| Technical Errors | Section 9 | WordPress REST API fields, code |

---

## After Claude Updates

**Claude will automatically:**
1. ✅ Update the relevant section in `yoast_seo_guidelines.md`
2. ✅ Update the prompt (`kcm_prompt_ACTIVE.md`) if needed
3. ✅ Fix any server code (`kcm_converter_server.py`) if needed
4. ✅ Commit all changes with clear message
5. ✅ Push to GitHub
6. ✅ Restart Flask server
7. ✅ Tell you: "Changes pushed to GitHub - open GitHub Desktop and pull"

**You do:**
1. Open GitHub Desktop
2. Make sure you're on the `claude/fix-focus-keyphrase-test-011CUcVm931ioTvS9uigNZhf` branch
3. Click "Pull origin" (or "Fetch origin" then "Pull")
4. Test the fix with a new article

---

## Quick Reference

**To report an error:**
```
Hey Claude - YOAST ERROR REPORT:
[paste the template above with your details]
```

**To check if guidelines were updated:**
```
Did you update yoast_seo_guidelines.md? Show me what changed.
```

**To verify server restart:**
```
Is the Flask server running with the latest code?
```

---

## Common Scenarios

### Scenario 1: "It's still broken after the update"

**You say:**
```
Claude - I pulled from GitHub and the error is still happening.
[paste the error report again with new details]
```

**Claude will:**
- Re-analyze the issue
- Check if there's another layer to the problem
- Update different sections if needed
- May ask for server logs or more details

---

### Scenario 2: "I have multiple errors to report"

**You say:**
```
Claude - I have 3 Yoast errors to report:

ERROR 1:
[use template]

ERROR 2:
[use template]

ERROR 3:
[use template]
```

**Claude will:**
- Address each error systematically
- Update all relevant guideline sections
- Prioritize based on severity
- Make all changes in one commit

---

### Scenario 3: "I want to add a new guideline"

**You say:**
```
Claude - I want to add a new rule to the Yoast guidelines:
[describe the rule and why]
```

**Claude will:**
- Determine the appropriate section
- Draft the new guideline
- Show you the proposed change
- Add it if you approve
- Update prompt to reference the new rule

---

## Tips for Better Error Reports

**✅ DO:**
- Be specific about what went wrong
- Include the exact text/values that were incorrect
- Mention if this is a recurring issue
- Note which article type it happened on

**❌ DON'T:**
- Just say "it's broken" without details
- Assume Claude knows which article you're testing
- Skip the example - real examples help!
- Report old errors that have been fixed

---

## Workflow Diagram

```
YOU                           CLAUDE                         RESULT
┌─────────────┐              ┌──────────────┐              ┌─────────────┐
│ Find Error  │─────────────>│ Analyze      │─────────────>│ Updated     │
│ in WordPress│              │ Root Cause   │              │ Guidelines  │
└─────────────┘              └──────────────┘              └─────────────┘
                                     │                              │
                                     v                              v
                             ┌──────────────┐              ┌─────────────┐
                             │ Update Files │─────────────>│ Commit &    │
                             │ (md/py)      │              │ Push to Git │
                             └──────────────┘              └─────────────┘
                                     │                              │
                                     v                              v
                             ┌──────────────┐              ┌─────────────┐
                             │ Restart      │              │ YOU: Pull   │
                             │ Flask Server │              │ from GitHub │
                             └──────────────┘              └─────────────┘
                                                                   │
                                                                   v
                                                           ┌─────────────┐
                                                           │ Test Fix    │
                                                           └─────────────┘
```

---

## Questions?

**Ask Claude:**
- "Show me the current Yoast guidelines for [section]"
- "What was the last change made to the guidelines?"
- "Which guideline covers [specific issue]?"

---

**Last Updated**: 2025-10-30
**Version**: 1.0 (Initial Workflow)

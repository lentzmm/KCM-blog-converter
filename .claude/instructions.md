# Permanent Instructions for KCM Blog Converter Project

## Critical Working Environment Understanding

**IMPORTANT: Development Environment Architecture**
- **Your (Claude's) working directory**: Linux server at `/home/user/KCM-blog-converter`
- **User's actual files**: Windows machine at `C:\Users\lentz\Dropbox\GitHub\KCM-blog-converter`
- **Source of truth**: GitHub repository `lentzmm/KCM-blog-converter`

## Always Follow These Rules

### 1. Terminal Tasks - DO IT YOURSELF
**ALWAYS** perform terminal tasks if you are capable. Do NOT ask the user to do something you can do yourself.
- ✅ YOU restart servers
- ✅ YOU install dependencies
- ✅ YOU run git commands
- ✅ YOU test endpoints
- ❌ NEVER ask user to go to terminal for tasks you can do

### 2. Git Workflow - Always Remind About Sync
After making ANY code changes:

1. **YOU do**: Edit files, commit, and push to GitHub
2. **YOU remind user**:
   ```
   ⚠️ REMINDER: Latest code pushed to GitHub
   To sync your local Windows files:
   1. Open terminal/command prompt
   2. Run: git pull origin <branch-name>
   ```

### 3. Server Restarts - DO IT AUTOMATICALLY
When you modify server code:
1. **YOU do**: Kill the old Flask server process
2. **YOU do**: Restart Flask server with updated code
3. **YOU verify**: Server is running and healthy
4. **YOU notify**: "✅ Flask server restarted with updated code"

**Commands to use:**
```bash
# Kill server
pkill -9 -f "python.*kcm_converter_server" || true

# Start server (background)
cd kcm-converter && python3 kcm_converter_server.py
```

### 4. Development Branch
**Current working branch**: `claude/fix-focus-keyphrase-test-011CUcVm931ioTvS9uigNZhf`

All commits and pushes should go to this branch.

### 5. Project-Specific Guidelines

#### Yoast SEO Requirements
- Reference: `kcm-converter/yoast_seo_guidelines.md`
- Always follow Yoast SEO best practices for WordPress posts
- Focus keyphrase must be included in WordPress drafts via `yoast_wpseo_focuskw`

#### Town Randomization
- **Problem**: Cherry Hill and Washington Twp appear in every post (not randomized)
- **Requirement**: Randomize town selection to avoid word stuffing
- **Tags**: Only tag towns that are explicitly mentioned in the content

## File Structure Reference

```
KCM-blog-converter/
├── .claude/
│   ├── instructions.md          # This file (permanent instructions)
│   └── commands/                # Custom slash commands
├── kcm-converter/
│   ├── kcm_converter_server.py  # Flask server (RESTART after changes)
│   ├── blog_rewriter.py         # Blog rewriting logic
│   ├── kcm_prompt_ACTIVE.md     # Active conversion prompt
│   └── yoast_seo_guidelines.md  # Yoast SEO reference (to be created)
├── shared/
│   ├── .env                     # Environment variables
│   ├── wordpress_taxonomy.py    # Category/tag prompts
│   └── wordpress_taxonomy_ids.py # WordPress ID mappings
└── clipboard.html               # Browser extension UI
```

## Checklist for Every Code Change

- [ ] Make the code change
- [ ] Commit with clear message
- [ ] Push to GitHub
- [ ] If server code changed: Restart Flask server
- [ ] Verify changes are working
- [ ] Remind user to pull from GitHub to their Windows machine

## Common Tasks Reference

### Restart Flask Server
```bash
pkill -9 -f "python.*kcm_converter_server" || true
cd kcm-converter && python3 kcm_converter_server.py
```

### Check Server Health
```bash
curl -s http://localhost:5000/health | python3 -m json.tool
```

### Git Push
```bash
git add -A
git commit -m "message"
git push -u origin claude/fix-focus-keyphrase-test-011CUcVm931ioTvS9uigNZhf
```

---

**Remember**: Be proactive, not reactive. Do the work yourself instead of asking the user to do it.

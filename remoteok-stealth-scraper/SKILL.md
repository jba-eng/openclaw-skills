---
name: RemoteOK Stealth Scraper
slug: remoteok-stealth-scraper
version: 1.0.0
homepage: https://github.com/openclaw/openclaw/tree/main/skills/remoteok-stealth-scraper
description: Stealth scrape AI Engineer jobs from RemoteOK using bot detection evasion techniques
metadata: {"clawdbot":{"emoji":"🕵️","requires":{"bins":["nodejs","playwright"]}}}
---

## When to Use

Use when you need to:
- Scrape job listings from RemoteOK without triggering bot detection
- Extract AI/ML engineer positions with stealth browsing
- Collect job data for analysis while appearing as a human user
- Test anti-bot evasion techniques for web scraping

## Core Rules

1. **Always enable stealth by default** - Default `enableStealth: true` ensures bot detection evasion
2. **Use relative imports only** - All module imports must be relative (`./context`, `./fingerprinting`)
3. **Maintain human-like behavior** - Include random delays, scrolling, and mouse movements
4. **Extract AI jobs with keyword filtering** - Filter for AI/ML related positions using predefined keywords
5. **Save results to JSON with metadata** - Include stealth techniques used and timestamp
6. **Respect rate limits** - Add delays between requests to avoid IP blocking
7. **Validate browser fingerprinting** - Verify `navigator.webdriver === false` before extraction

## File Structure

```
remoteok-stealth-scraper/
├── SKILL.md              # This file
├── README.md             # Detailed documentation
├── src/
│   ├── context.ts        # Stealth browser initialization
│   ├── fingerprinting.ts # Navigator spoofing & WebGL protection
│   ├── navigation.ts     # Human-like behavior simulation
│   ├── extractor.ts      # Job extraction with AI filtering
│   └── scraper.ts        # Main orchestration and API
└── package.json          # Dependencies (Playwright, TypeScript)
```

## Quick Reference

| Task | Command |
|------|---------|
| Scrape jobs | `node src/scraper.ts --targetUrl "https://remoteok.com/remote-engineer-jobs"` |
| Test stealth | `node src/scraper.ts --enableStealth true --verbose true` |
| Filter AI jobs | `node src/scraper.ts --targetUrl "https://remoteok.com/search?q=ai+engineer"` |

## Auxiliary Files

- `README.md` - Full implementation details and stealth techniques
- `src/` - TypeScript source code with modular architecture

## Stealth Techniques

This skill implements:
- Chrome flags to hide automation (`--disable-blink-features=AutomationControlled`)
- Navigator property spoofing (platform, vendor, webdriver)
- WebGL and canvas fingerprinting protection
- Human-like scrolling and mouse movements
- Random delays between actions (1000-3000ms)

## Notes

- Requires Node.js 18+ and Playwright installed
- Respect RemoteOK's terms of service and robots.txt
- Use for legitimate job search and research purposes only

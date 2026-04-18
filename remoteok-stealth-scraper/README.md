# Stealth Scraping Module

A comprehensive stealth scraping solution for RemoteOK AI Engineer job extraction using Playwright with advanced bot detection evasion.

## Files

- **context.ts** - Browser initialization with stealth flags
- **fingerprinting.ts** - Navigator property spoofing and WebGL/canvas protection
- **navigation.ts** - Human-like browsing behavior (scrolling, delays, mouse movements)
- **extractor.ts** - Job data extraction and AI filtering
- **scraper.ts** - Main orchestration and workflow management
- **tests/test_stealth.ts** - Unit and integration tests
- **run_tests.js** - Test runner script

## Features

### Stealth Techniques

1. **Browser Fingerprinting**
   - Chrome flags to hide automation
   - Realistic User-Agent (Windows 10 Chrome)
   - Viewport 1920x1080
   - Locale en-US

2. **Navigator Spoofing**
   - Removes webdriver property
   - Spoofs platform, vendor, languages
   - Mocks hardwareConcurrency, deviceMemory
   - Simulates 4G connection

3. **Plugin & MIME Type Mocking**
   - Chrome PDF Viewer, PDF Plugin
   - Native Client
   - Realistic MIME types

4. **WebGL Protection**
   - Spoofs UNMASKED_VENDOR_WEBGL
   - Spoofs UNMASKED_RENDERER_WEBGL
   - Returns Intel UHD Graphics 630

5. **Canvas Fingerprinting**
   - Adds noise to canvas output
   - Disables toDataURL fingerprinting

6. **Human Behavior Simulation**
   - Random delays between actions
   - Human-like scrolling (multi-step)
   - Mouse movements and hovers
   - Page loading patterns

## Usage

```typescript
import { scrapeWithStealth } from './stealth/scraper';

// Basic usage
const result = await scrapeWithStealth({
  targetUrl: 'https://remoteok.com/remote-engineer-jobs',
  savePath: './results.json',
  maxJobs: 100,
  timeout: 45000,
  delayBetweenActions: 1000,
  enableStealth: true,
  verbose: true,
});

console.log(result);
// { success: true, jobs: [...], aiJobsCount: 12 }
```

## Running Tests

```bash
node stealth/run_tests.js
```

Or using Playwright directly:

```bash
npx playwright test stealth/tests/test_stealth.ts
```

## Architecture

```
scraper.ts (orchestration)
├── createStealthBrowser()
├── createStealthContext()
└── applyFingerprintingSpoofing()

fingerprinting.ts
├── spoofNavigatorProperties()
├── mockNavigatorPlugins()
├── spoofWebGL()
└── spoofCanvasFingerprinting()

navigation.ts
├── randomDelay()
├── humanScroll()
├── simulateMouseMovement()
└── simulateReading()

extractor.ts
├── isAIJob()
├── extractJobData()
└── extractJobsFromPage()
```

## Stealth Level

This implementation matches the techniques used in `remoteok-ai-engineer-stealth.mjs` with the following enhancements:

- Structured TypeScript code
- Type safety
- Comprehensive error handling
- Modular architecture
- Test coverage
- Extensibility

## Limitations

- Requires Playwright and Node.js
- May need browser binaries (chromium)
- Rate limiting on target sites
- Respect robots.txt and terms of service

/**
 * stealth/scraper.ts - Main orchestration for stealth scraping
 */

import { Browser, BrowserContext, Page } from 'playwright';
import { createStealthBrowser, createStealthContext } from './context';
import { applyFingerprintingSpoofing } from './fingerprinting';
import { humanScroll, randomDelay, simulateMouseMovement } from './navigation';
import { extractJobsFromPage } from './extractor';

export interface ScrapingOptions {
  targetUrl: string;
  savePath?: string;
  maxJobs?: number;
  timeout?: number;
  delayBetweenActions?: number;
  enableStealth?: boolean;
  verbose?: boolean;
}

export interface ScrapingResult {
  success: boolean;
  jobs: any[];
  aiJobsCount: number;
  error?: string;
}

/**
 * Main stealth scraper function
 */
export async function scrapeWithStealth(
  options: ScrapingOptions
): Promise<ScrapingResult> {
  const {
    targetUrl,
    savePath = './stealth_scraping_results.json',
    maxJobs = Infinity,
    timeout = 45000,
    delayBetweenActions = 1000,
    enableStealth = true,
    verbose = true,
  } = options;

  if (verbose) {
    console.log('🚀 Starting Stealth Scraper');
    console.log('📊 Target:', targetUrl);
    console.log('💾 Output:', savePath);
    console.log('🛡️  Stealth:', enableStealth ? 'ENABLED' : 'DISABLED');
  }

  // Create stealth browser
  const browser = await createStealthBrowser();

  try {
    // Create stealth context
    const context = await createStealthContext(browser, {
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      locale: 'en-US',
      timezoneId: 'America/New_York',
      enableStealth,
    });

    const page = await context.newPage();

    // Apply stealth configurations
    if (enableStealth) {
      await applyFingerprintingSpoofing();
      await page.setViewportSize({ width: 1920, height: 1080 });
    }

    // Navigate to target page
    if (verbose) {
      console.log('\n🌐 Navigating to page...');
    }

    await page.goto(targetUrl, {
      waitUntil: 'networkidle',
      timeout: timeout,
    });

    // Wait for page to fully load
    if (verbose) {
      console.log('⏳ Waiting for page content...');
    }
    await randomDelay(delayBetweenActions, delayBetweenActions * 2);

    // Simulate human interaction
    if (verbose) {
      console.log('🖱️  Simulating human interaction...');
    }

    // Scroll and hover to trigger lazy loading
    await humanScroll(page);
    await simulateMouseMovement(page);
    await randomDelay(delayBetweenActions, delayBetweenActions * 2);

    // Extract job data
    if (verbose) {
      console.log('📋 Extracting job data...');
    }

    const jobsData = await extractJobsFromPage(page);

    // Save results
    if (verbose) {
      console.log('\n📄 Saving results...');
    }

    const outputPath = savePath;
    const output = {
      metadata: {
        source: 'RemoteOK.com',
        url: targetUrl,
        scrapedAt: new Date().toISOString(),
        totalJobs: jobsData.total,
        aiJobsCount: jobsData.aiCount,
        stealthTechniques: {
          enabled: enableStealth,
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          navigatorPlatform: 'Win32',
          navigatorVendor: 'Google Inc.',
          hardwareConcurrency: 16,
          deviceMemory: 8,
          navigatorLanguages: ['en-US', 'en'],
          pluginsInjected: true,
          canvasFingerprintingDisabled: true,
          webglSpoofed: true,
          webdriverDetectionBlocked: true,
        },
      },
      allJobs: jobsData.allJobs,
      aiJobs: jobsData.aiJobs,
    };

    await import('fs').then((fs) =>
      fs.writeFile(outputPath, JSON.stringify(output, null, 2), {
        encoding: 'utf8',
      })
    );

    console.log(`\n✅ Results saved to ${outputPath}`);
    console.log(`📊 Total jobs: ${jobsData.total}`);
    console.log(`🤖 AI-related jobs: ${jobsData.aiCount}`);

    // Print sample AI jobs if available
    if (jobsData.aiCount > 0 && verbose) {
      console.log('\n=== SAMPLE AI JOBS ===');
      jobsData.aiJobs.slice(0, 3).forEach((job, i) => {
        console.log(`${i + 1}. ${job.title} at ${job.company}`);
        console.log(`   Location: ${job.location}`);
        console.log(`   Tags: ${(job as any).tags?.slice(0, 5).join(', ') || 'N/A'}`);
        if ((job as any).salary) {
          console.log(`   Salary: ${(job as any).salary}`);
        }
        console.log('');
      });
    }

    return {
      success: true,
      jobs: jobsData.allJobs,
      aiJobsCount: jobsData.aiCount,
    };
  } catch (error) {
    console.error('❌ Error during scraping:', error.message);
    console.error('Stack trace:', error.stack);
    return {
      success: false,
      error: error.message,
      jobs: [],
      aiJobsCount: 0,
    };
  } finally {
    // Close browser resources
    if (verbose) {
      console.log('\n🔒 Closing browser...');
    }
    await browser.close();

    if (verbose) {
      console.log('✅ Scraping completed successfully!');
    }
  }
}

/**
 * Quick scraper - minimal configuration
 */
export async function quickScrape(url: string): Promise<any> {
  return scrapeWithStealth({
    targetUrl: url,
    maxJobs: 50,
    delayBetweenActions: 500,
    verbose: false,
  });
}

/**
 * Test stealth capabilities
 */
export async function testStealthCapabilities(): Promise<{
  userAgent: string;
  viewport: { width: number; height: number };
  locale: string;
}> {
  const browser = await createStealthBrowser();
  const context = await createStealthContext(browser);
  const page = await context.newPage();

  const capabilities = await page.evaluate(() => ({
    userAgent: navigator.userAgent,
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
    },
    locale: navigator.language,
  }));

  await browser.close();
  return capabilities;
}

/**
 * Batch scrape multiple pages
 */
export async function batchScrape(
  urls: string[],
  options: Partial<ScrapingOptions> = {}
): Promise<{ results: any[]; totalScraped: number }> {
  const results: any[] = [];
  const { maxJobs = 100, timeout = 60000 } = options;

  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    console.log(`\n[${i + 1}/${urls.length}] Scraping: ${url}`);

    const result = await scrapeWithStealth({
      targetUrl: url,
      maxJobs,
      timeout,
    });

    if (result.success) {
      results.push(result);
    }

    // Rate limiting between requests
    await randomDelay(2000, 5000);
  }

  return {
    results,
    totalScraped: results.length,
  };
}

export { ScrapingOptions, ScrapingResult };
/**
 * stealth/navigation.ts - Human-like browsing behavior
 */

import { Page } from 'playwright';

/**
 * Generate random delay between actions to simulate human behavior
 */
export function randomDelay(minMs: number = 500, maxMs: number = 1500): Promise<void> {
  const delay = Math.floor(Math.random() * (maxMs - minMs + 1) + minMs);
  return new Promise((resolve) => setTimeout(resolve, delay));
}

/**
 * Human-like scrolling behavior
 */
export async function humanScroll(page: Page): Promise<void> {
  // Scroll in steps to simulate human reading
  const scrollHeight = page.viewport()?.height || 1080;

  // Scroll down in chunks with pauses
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => {
      window.scrollBy(0, scrollHeight / 2);
    });

    // Wait randomly between 300-800ms
    await randomDelay(300, 800);

    // Scroll to bottom of viewport
    await page.evaluate(() => {
      window.scrollBy(0, scrollHeight);
    });

    // Random pause between 200-600ms
    await randomDelay(200, 600);

    // Scroll back up occasionally
    if (i % 2 === 0) {
      await page.evaluate(() => {
        window.scrollBy(0, -scrollHeight / 2);
      });
      await randomDelay(100, 300);
    }
  }

  // Final scroll to bottom
  await page.evaluate(() => {
    window.scrollBy(0, scrollHeight);
  });
}

/**
 * Simulate human mouse movements
 */
export async function simulateMouseMovement(page: Page): Promise<void> {
  const viewport = page.viewport();
  if (!viewport) return;

  const width = viewport.width;
  const height = viewport.height;

  // Move mouse around naturally
  const moves = [
    { x: width * 0.1, y: height * 0.2 },
    { x: width * 0.4, y: height * 0.6 },
    { x: width * 0.7, y: height * 0.3 },
    { x: width * 0.2, y: height * 0.8 },
  ];

  for (const { x, y } of moves) {
    // Convert to pixel coordinates
    const px = x * width;
    const py = y * height;

    await page.mouse.move(px, py, {
      steps: Math.floor(Math.random() * 10) + 5,
      duration: Math.random() * 1000 + 500,
    });

    // Random click or hover
    if (Math.random() > 0.5) {
      await page.mouse.click(px, py, {
        delay: Math.random() * 100 + 50,
      });
    }

    // Random delay
    await randomDelay(100, 300);
  }
}

/**
 * Simulate human page loading behavior
 */
export async function humanPageLoad(
  page: Page,
  options: {
    maxWait?: number;
    waitUntil?: string;
  } = {}
): Promise<void> {
  const { maxWait = 30000, waitUntil = 'networkidle' } = options;

  // Navigate with timeout
  await page.goto('about:blank', {
    waitUntil,
    timeout: maxWait,
  });

  // Wait for content to render with randomness
  await randomDelay(500, 1000);

  // Simulate checking various elements
  try {
    await page.waitForSelector('body', { state: 'visible' });
  } catch (e) {
    // Ignore if selector not found
  }
}

/**
 * Avoid rapid-fire navigation patterns
 */
export function getNavigationDelay(): number {
  // Return random delay between 500-1500ms
  return Math.floor(Math.random() * 1000) + 500;
}

/**
 * Check if page is fully loaded with timeout
 */
export async function isPageLoaded(
  page: Page,
  timeout: number = 10000
): Promise<boolean> {
  try {
    await page.waitForLoadState('domcontentloaded', { timeout });
    await randomDelay(200, 500); // Add human-like pause
    return true;
  } catch {
    return false;
  }
}

/**
 * Simulate reading behavior - hover over elements and pause
 */
export async function simulateReading(page: Page, selectors: string[] = []): Promise<void> {
  const elementsToCheck = selectors.length
    ? selectors
    : ['h1', 'h2', 'h3', 'h4', 'a', 'img'];

  for (const selector of elementsToCheck) {
    try {
      // Wait for element to be visible
      await page.waitForSelector(selector, { state: 'visible' });

      // Hover over it (if visible)
      const elements = await page.locator(selector).all();
      for (const element of elements.slice(0, 3)) {
        await page.hover(selector, {
          force: true,
          timeout: 1000,
        });
        await randomDelay(100, 300);
      }
    } catch (e) {
      // Element not found, continue
    }
  }

  await randomDelay(200, 500);
}

/**
 * Backtrack navigation - go back occasionally
 */
export async function backtrackNavigation(page: Page, maxBacks: number = 1): Promise<void> {
  const backs = Math.floor(Math.random() * maxBacks) + 1;

  for (let i = 0; i < backs; i++) {
    try {
      await page.goBack({ waitUntil: 'networkidle' });
      await randomDelay(500, 1000);
    } catch {
      // Navigation blocked
    }
  }
}

/**
 * Simulate tab switching behavior
 */
export async function simulateTabSwitching(page: Page): Promise<void> {
  // Simulate switching focus (like Alt+Tab)
  await page.evaluate(() => {
    window.focus();
  });
  await randomDelay(200, 500);
  await page.evaluate(() => {
    window.focus();
  });
}
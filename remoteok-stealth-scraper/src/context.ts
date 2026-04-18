/**
 * stealth/context.ts - Browser initialization with stealth flags
 */

import { chromium, BrowserContext, Browser } from 'playwright';

export interface StealthContextOptions {
  viewport?: { width: number; height: number };
  userAgent?: string;
  locale?: string;
  timezoneId?: string;
  enableStealth?: boolean;
}

/**
 * Create a stealthy Playwright browser instance
 */
export async function createStealthBrowser(
  options: StealthContextOptions = {}
): Promise<Browser> {
  const { viewport = { width: 1920, height: 1080 }, enableStealth = true } = options;

  const chromeFlags: string[] = [
    // Chrome flags to hide automation
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-component-update',
    '--disable-default-apps',
    '--disable-extensions',
    '--disable-sync',
    '--metrics-recording-only',
    '--disable-client-side-phishing-detection',
    '--disable-popup-blocking',
    '--disable-prompt-on-repost',
    '--disable-domain-reliability',
    '--no-first-run',
    '--no-default-browser-check',
    '--mute-audio',
    '--hide-scrollbars'
  ];

  return await chromium.launch({
    headless: true,
    args: chromeFlags
  });
}

/**
 * Create a stealthy browser context with realistic settings
 */
export async function createStealthContext(
  browser: Browser,
  options: StealthContextOptions = {}
): Promise<BrowserContext> {
  const { viewport, userAgent, locale, timezoneId, enableStealth = true } = options;

  const contextOptions: any = {
    viewport: viewport,
    locale: locale || 'en-US',
    timezoneId: timezoneId || 'America/New_York',
  };

  if (enableStealth) {
    contextOptions.userAgent =
      userAgent ||
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
  }

  return await browser.newContext(contextOptions);
}

/**
 * Apply stealth configurations to a page
 */
export async function applyPageStealth(page: any): Promise<void> {
  if (!process.env.STEALTH_ENABLED) return;

  // Set viewport
  await page.setViewportSize({ width: 1920, height: 1080 });

  // Override navigator properties
  await page.addInitScript(() => {
    // Remove webdriver property
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });

    // Override languages
    Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en'],
    });

    // Override platform
    Object.defineProperty(navigator, 'platform', {
      get: () => 'Win32',
    });

    // Override vendor
    Object.defineProperty(navigator, 'vendor', {
      get: () => 'Google Inc.',
    });

    // Override hardwareConcurrency
    Object.defineProperty(navigator, 'hardwareConcurrency', {
      get: () => 16,
    });

    // Override deviceMemory
    Object.defineProperty(navigator, 'deviceMemory', {
      get: () => 8,
    });

    // Override connection
    Object.defineProperty(navigator, 'connection', {
      get: () => ({
        downlink: 10,
        effectiveType: '4g',
        rtt: 50,
      }),
    });

    // Mock plugins
    const originalPlugins = navigator.plugins;
    Object.defineProperty(navigator, 'plugins', {
      get: () => {
        const plugins: any[] = [];

        // Add Chrome PDF Viewer
        plugins.push({
          name: 'Chrome PDF Viewer',
          filename: 'internal-pdf-viewer',
          description: 'Portable Document Format',
          __mimeTypes: [
            {
              type: 'application/pdf',
              suffixes: 'pdf',
              description: 'Portable Document Format',
            },
          ],
        });

        // Add Chrome PDF Plugin
        plugins.push({
          name: 'Chrome PDF Plugin',
          filename: 'internal-pdf-plugin',
          description: 'Portable Document Format',
          __mimeTypes: [
            {
              type: 'application/x-google-chrome-pdf',
              suffixes: 'pdf',
              description: 'Portable Document Format',
            },
          ],
        });

        // Add Native Client
        plugins.push({
          name: 'Native Client',
          filename: 'internal-nacl-plugin',
          description: '',
          __mimeTypes: [],
        });

        return plugins;
      },
    });

    // Mock mimeTypes
    Object.defineProperty(navigator, 'mimeTypes', {
      get: () => [
        {
          type: 'application/pdf',
          suffixes: 'pdf',
          description: 'Portable Document Format',
          enabledPlugin: navigator.plugins[0],
        },
      ],
    });

    // Disable canvas fingerprinting
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function (type: string, quality?: number) {
      const canvas = this;
      const context = canvas.getContext('2d');

      // Add slight noise to make fingerprinting harder
      if (context) {
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < imageData.data.length; i += 4) {
          // Add minimal random noise (less than 1% variance)
          imageData.data[i] += Math.random() > 0.5 ? 1 : -1;
        }
        context.putImageData(imageData, 0, 0);
      }

      return originalToDataURL.call(this, type, quality);
    };

    // Mock WebGL
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function (parameter: number) {
      // Return plausible values for fingerprinting parameters
      if (parameter === 37445) {
        // UNMASKED_VENDOR_WEBGL
        return 'Google Inc.';
      }
      if (parameter === 37446) {
        // UNMASKED_RENDERER_WEBGL
        return 'ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)';
      }
      return getParameter.call(this, parameter);
    };
  });
}

export { StealthContextOptions };
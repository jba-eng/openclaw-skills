/**
 * stealth/fingerprinting.ts - Browser fingerprinting spoofing
 */

/**
 * Configure navigator properties to spoof a real Chrome browser
 */
export function spoofNavigatorProperties(): void {
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
}

/**
 * Mock navigator.plugins with realistic browser plugins
 */
export function mockNavigatorPlugins(): any[] {
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
}

/**
 * Mock navigator.mimeTypes
 */
export function mockNavigatorMimeTypes(plugins: any[]): any[] {
  return [
    {
      type: 'application/pdf',
      suffixes: 'pdf',
      description: 'Portable Document Format',
      enabledPlugin: plugins[0],
    },
  ];
}

/**
 * Spoof WebGL vendor and renderer for fingerprinting protection
 */
export function spoofWebGL(): void {
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
}

/**
 * Spoof canvas fingerprinting to avoid detection
 */
export function spoofCanvasFingerprinting(): void {
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
}

/**
 * Apply all fingerprinting protections
 */
export function applyFingerprintingSpoofing(): void {
  spoofNavigatorProperties();
  const plugins = mockNavigatorPlugins();
  mockNavigatorMimeTypes(plugins);
  spoofWebGL();
  spoofCanvasFingerprinting();
}

/**
 * Test if bot detection is evading successfully
 */
export function testFingerprinting(): {
  webdriverDetected: boolean;
  vendorDetected: boolean;
  hardwareDetected: boolean;
} {
  const webdriverDetected = navigator.webdriver !== undefined;
  const vendorDetected = navigator.vendor !== 'Google Inc.';
  const hardwareDetected = navigator.hardwareConcurrency === undefined;

  return {
    webdriverDetected,
    vendorDetected,
    hardwareDetected,
  };
}
import { createStealthBrowser, createStealthContext } from './context';
import { applyFingerprintingSpoofing } from './fingerprinting';
import { randomDelay } from './navigation';

async function main() {
    console.log('🚀 Testing stealth pipeline with ts-node...');
    let browser;
    try {
        // Launch stealth browser
        console.log('🔧 Launching stealth browser...');
        browser = await createStealthBrowser();
        
        // Create stealth context
        console.log('🔧 Creating stealth context...');
        const context = await createStealthContext(browser, {
            viewport: { width: 1920, height: 1080 },
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale: 'en-US',
            timezoneId: 'America/New_York',
            enableStealth: true,
        });
        
        const page = await context.newPage();
        
        // Apply fingerprinting spoofing
        console.log('🔧 Applying fingerprinting spoofing...');
        await applyFingerprintingSpoofing();
        
        // Test navigator properties
        console.log('🧪 Checking navigator...');
        const nav = await page.evaluate(() => ({
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            webdriver: navigator.webdriver,
        }));
        console.log('📊 Navigator:', nav);
        
        // Navigate to example.com to test
        console.log('🌐 Navigating to example.com...');
        await page.goto('https://example.com', { waitUntil: 'networkidle', timeout: 10000 });
        await randomDelay(1000, 2000);
        
        console.log('✅ Basic stealth pipeline works!');
    } catch (error) {
        console.error('❌ Error:', error);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
            console.log('🔒 Browser closed.');
        }
    }
}

main();

import { defineConfig } from '@playwright/test';

export default defineConfig({ 
    testDir: './tests',
    reporter: 'html', // generates report viewable with: npx playwright show-report
    use: { baseURL: 'http://localhost:3000',
        headless: false, // set true to run without visible browser
    screenshot: 'only-on-failure',
    },
});
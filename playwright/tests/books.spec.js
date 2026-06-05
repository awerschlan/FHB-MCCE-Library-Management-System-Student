import { test, expect } from '@playwright/test'; 
 
test('books list displays seeded data', async ({ page }) => { 
  await page.goto('/'); 
  await page.waitForSelector('table tbody tr'); 
 
  const rows = page.locator('table tbody tr'); 
  const count = await rows.count(); 
  expect(count).toBeGreaterThan(50);  // seed loads 61 books 
});
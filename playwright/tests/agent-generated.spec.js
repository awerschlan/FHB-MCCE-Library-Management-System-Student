import { test, expect } from '@playwright/test';

test('opening the first member shows the member detail page', async ({ page }) => {
  await page.goto('/');

  // Navigate to the Members tab
  await page.getByRole('button', { name: 'Members' }).click();

  // Wait for the members list table to load, then open the first member row
  await page.waitForSelector('table tbody tr');
  await page.locator('table tbody tr').first().locator('td').first().click();

  // The detail page renders a breadcrumb once loaded
  await page.waitForSelector('.breadcrumb');

  // The breadcrumb links back to the Members list
  await expect(page.locator('.breadcrumb')).toContainText('Members');

  // The page heading identifies the member detail view
  await expect(page.locator('h2').first()).toContainText('Member Details');

  // The statistics section is rendered and visible
  await expect(page.getByRole('heading', { name: 'Statistics' })).toBeVisible();
});

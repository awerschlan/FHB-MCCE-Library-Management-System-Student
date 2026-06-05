import { test, expect } from '@playwright/test';

test('books list displays seeded data', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('table tbody tr');

  const rows = page.locator('table tbody tr');
  const count = await rows.count();
  expect(count).toBeGreaterThan(50);  // seed loads 61 books 
});


test('add a book via the form and verify it appears in the list', async ({ page }) => {
  await page.goto('/');

  // Generate a unique ISBN so the test can run multiple times 
  const isbn = `97800${Date.now().toString().slice(-8)}`;

  await page.fill('input[placeholder="ISBN (10 or 13 digits)"]', isbn);
  await page.fill('input[placeholder="Title"]', 'My Playwright Book');
  await page.fill('input[placeholder="Author"]', 'Test Author');
  await page.fill('input[placeholder="Genre"]', 'Fiction');
  await page.fill('input[placeholder="Year"]', '2024');
  await page.fill('input[placeholder="Copies"]', '2');

  await page.getByRole('button', { name: 'Add Book' }).click();

  // Green success message should appear 
  await expect(page.locator('.msg.ok')).toBeVisible();

  // The new book should appear in the list 
  await expect(page.locator('table').last()).toContainText('My Playwright Book');
});

test('clicking a book row opens the detail page', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('table tbody tr'); 
  // Click the last cell of the first row (avoids the title/author links) 
  await page.locator('table tbody tr').first().locator('td').last().click();
  await page.waitForSelector('.breadcrumb');
  await expect(page.locator('.breadcrumb')).toContainText('Books');
  await expect(page.locator('h2').first()).toContainText('Book Details');
  await expect(page.locator('.dl')).toContainText('Available copies');
});
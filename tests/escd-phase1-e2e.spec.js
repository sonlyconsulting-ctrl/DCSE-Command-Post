const { test, expect } = require('@playwright/test');

async function installMocks(page) {
  await page.addInitScript(() => sessionStorage.setItem('escd_access_token', 'test-token'));
  await page.route('**/api/mvp/providers', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, providers: {
      openai: { enabled: true, configured: true, model: 'gpt-test', credential_source: 'vault' },
      gemini: { enabled: false, configured: false, model: 'gemini-test', credential_source: 'none' },
      openrouter: { enabled: true, configured: true, model: 'router-test', credential_source: 'vault' }
    }})
  }));
  await page.route('**/api/mvp/items', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, items: [] })
  }));
  await page.route('**/api/mvp/assets', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, assets: [] })
  }));
  await page.route('**/api/mvp/ddna', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, records: [] })
  }));
  await page.route('**/api/mvp/knowledge', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, knowledge: Array.from({length: 24}, (_, i) => ({
      id: 'K-' + (i + 1), title: 'Knowledge ' + (i + 1), content: 'Governed record ' + (i + 1),
      authority_classification: 'HISTORICAL_RECOVERED', status: 'staged', confidence: 0.95, provenance: {}
    })) })
  }));
}

test('desktop Phase 1 navigation exposes Knowledge and canonical records', async ({ page }) => {
  await installMocks(page);
  await page.goto('http://127.0.0.1:4173/mvp.html');
  await expect(page.getByText('ESCD', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Knowledge' }).first().click();
  await expect(page.locator('#knowledge')).toHaveClass(/active/);
  await expect(page.locator('#knowledgeList .row')).toHaveCount(24);
  await expect(page.getByPlaceholder('Search canonical knowledge...')).toBeVisible();
});

test.describe('mobile viewport', () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test('mobile navigation reaches Knowledge without horizontal desktop sidebar dependency', async ({ page }) => {
    await installMocks(page);
    await page.goto('http://127.0.0.1:4173/mvp.html');
    await expect(page.locator('#mobileNav')).toBeVisible();
    await page.locator('#mobileNav').getByRole('button', { name: 'Knowledge' }).click();
    await expect(page.locator('#knowledge')).toHaveClass(/active/);
    await expect(page.locator('#knowledgeList .row')).toHaveCount(24);
  });
});

const { test, expect } = require('@playwright/test');

async function loginAndOpenProfiles(page) {
  await page.goto('/');
  await page.getByTestId('username-input').fill('testuser');
  await page.getByTestId('password-input').fill('123456');
  await page.getByTestId('login-button').click();
}

test('login add-to-cart checkout flow', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('app-title')).toHaveText('E2E Benchmark Demo App');
  await page.getByTestId('username-input').fill('testuser');
  await page.getByTestId('password-input').fill('123456');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('product-card-1')).toBeVisible();
  await page.getByTestId('add-to-cart-1').click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
  await expect(page.getByTestId('cart-success')).toContainText('sepete eklendi');
  await page.getByTestId('fullname-input').fill('Huseyin Emecen');
  await page.getByTestId('address-input').fill('Ankara, Turkiye');
  await page.getByTestId('checkout-button').click();
  await expect(page.getByTestId('order-success')).toContainText('Sipariş başarıyla tamamlandı');
});

test('invalid login shows error', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username-input').fill('wronguser');
  await page.getByTestId('password-input').fill('wrongpass');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toContainText('Geçersiz kullanıcı adı veya parola');
});

test('checkout without cart shows error', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username-input').fill('testuser');
  await page.getByTestId('password-input').fill('123456');
  await page.getByTestId('login-button').click();
  await page.getByTestId('fullname-input').fill('Huseyin Emecen');
  await page.getByTestId('address-input').fill('Ankara, Turkiye');
  await page.getByTestId('checkout-button').click();
  await expect(page.getByTestId('checkout-error')).toContainText('önce sepete ürün ekleyiniz');
});

test.describe('ui-heavy benchmark', () => {
  test('ui-heavy profile starts, filters, and completes with visible UI output', async ({ page }) => {
    await loginAndOpenProfiles(page);
    await page.getByTestId('profile-tab-ui').click();
    await expect(page.getByTestId('profile-tab-ui')).toHaveClass(/active/);
    await expect(page.getByTestId('ui-heavy-profile')).toBeVisible();
    await expect(page.getByTestId('ui-heavy-summary')).toContainText('Gösterilen öğe sayısı: 36');
    await expect(page.getByTestId('ui-heavy-item')).toHaveCount(36);
    await page.getByTestId('ui-filter-input').fill('cart drawer 2');
    await expect(page.getByTestId('ui-heavy-summary')).toContainText('1');
    await expect(page.getByTestId('ui-heavy-item')).toHaveCount(1);
    await page.getByTestId('ui-sort-button').click();
    await expect(page.getByTestId('ui-heavy-list')).toContainText('Cart Drawer 2');
  });
});

test.describe('cpu-heavy benchmark', () => {
  test('cpu-heavy profile starts, runs computation, and shows deterministic result', async ({ page }) => {
    await loginAndOpenProfiles(page);
    await page.getByTestId('profile-tab-cpu').click();
    await expect(page.getByTestId('profile-tab-cpu')).toHaveClass(/active/);
    await expect(page.getByTestId('cpu-heavy-profile')).toBeVisible();
    await expect(page.getByTestId('cpu-heavy-status')).toContainText('Son sonuç hazır değil.');
    await page.getByTestId('cpu-run-button').click();
    await expect(page.getByTestId('cpu-heavy-status')).toHaveAttribute('data-cpu-result', /\d+/);
    await expect(page.getByTestId('cpu-heavy-status')).toContainText('Son sonuç: ');
  });
});

test.describe('ram-heavy benchmark', () => {
  test('ram-heavy profile starts, allocates memory, and releases it', async ({ page }) => {
    await loginAndOpenProfiles(page);
    await page.getByTestId('profile-tab-ram').click();
    await expect(page.getByTestId('profile-tab-ram')).toHaveClass(/active/);
    await expect(page.getByTestId('ram-heavy-profile')).toBeVisible();
    await expect(page.getByTestId('ram-heavy-status')).toContainText('Bellek yükü oluşturulmadı.');
    await page.getByTestId('ram-allocate-button').click();
    await expect(page.getByTestId('ram-heavy-status')).toHaveAttribute('data-ram-block-count', '48');
    await expect(page.getByTestId('ram-heavy-status')).toContainText('Blok sayısı: 48');
    await page.getByTestId('ram-release-button').click();
    await expect(page.getByTestId('ram-heavy-status')).toHaveAttribute('data-ram-block-count', '0');
    await expect(page.getByTestId('ram-heavy-status')).toContainText('Bellek yükü serbest bırakıldı.');
  });
});

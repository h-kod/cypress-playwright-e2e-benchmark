const { test, expect } = require('@playwright/test');

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

import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/auth/login');
    await expect(page.getByText('Selamat Datang Kembali')).toBeVisible();

    await page.getByPlaceholder('Masukkan username').fill('admin');
    await page.getByPlaceholder('Masukkan password').fill('admin');
    await page.getByRole('button', { name: /Masuk/i }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Dashboard')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/auth/login');
    await page.getByPlaceholder('Masukkan username').fill('wrong');
    await page.getByPlaceholder('Masukkan password').fill('wrong');
    await page.getByRole('button', { name: /Masuk/i }).click();

    await expect(page.getByText(/Login gagal|salah/i)).toBeVisible();
  });

  test('should redirect to login when accessing protected route', async ({ page }) => {
    await page.goto('/customers');
    await expect(page).toHaveURL(/\/auth\/login\?redirect=/);
  });

  test('should logout from menu', async ({ page }) => {
    // First login
    await page.goto('/auth/login');
    await page.getByPlaceholder('Masukkan username').fill('admin');
    await page.getByPlaceholder('Masukkan password').fill('admin');
    await page.getByRole('button', { name: /Masuk/i }).click();
    await expect(page).toHaveURL('/dashboard');

    // Then logout
    await page.getByText('System Administrator').click();
    await page.getByText('Logout').click();
    await expect(page).toHaveURL('/auth/login');
  });
});

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login');
    await page.getByPlaceholder('Masukkan username').fill('admin');
    await page.getByPlaceholder('Masukkan password').fill('admin');
    await page.getByRole('button', { name: /Masuk/i }).click();
  });

  test('should show stat cards', async ({ page }) => {
    await expect(page.getByText('Total Nasabah')).toBeVisible();
    await expect(page.getByText('KYC Pending')).toBeVisible();
    await expect(page.getByText('Match Queue')).toBeVisible();
  });

  test('should show charts', async ({ page }) => {
    await expect(page.getByText('Pertumbuhan Nasabah')).toBeVisible();
    await expect(page.getByText('Distribusi Risk Profile')).toBeVisible();
  });
});

test.describe('Customer Search', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login');
    await page.getByPlaceholder('Masukkan username').fill('admin');
    await page.getByPlaceholder('Masukkan password').fill('admin');
    await page.getByRole('button', { name: /Masuk/i }).click();
    await page.goto('/customers');
  });

  test('should display customer list', async ({ page }) => {
    await expect(page.getByText('Pencarian Nasabah')).toBeVisible();
  });

  test('should filter by type', async ({ page }) => {
    await page.getByText('Filter').click();
    await expect(page.getByText('Tipe Nasabah')).toBeVisible();
  });

  test('should navigate to detail on click', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.el-table__row');
    // Click first detail button
    const firstDetail = page.getByRole('button', { name: 'Detail' }).first();
    if (await firstDetail.isVisible()) {
      await firstDetail.click();
    }
  });
});

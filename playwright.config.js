module.exports = {
  testDir: './playwright-tests',
  timeout: 30000,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:5500',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'off',
    trace: 'off'
  }
};

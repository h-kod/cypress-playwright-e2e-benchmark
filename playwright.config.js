module.exports = {
  testDir: './playwright-tests',
  timeout: 30000,
  reporter: 'list',
  webServer: {
    command: 'node scripts/static-server.js',
    url: 'http://127.0.0.1:5500',
    reuseExistingServer: true,
    timeout: 120000
  },
  use: {
    baseURL: 'http://127.0.0.1:5500',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'off',
    trace: 'off'
  }
};

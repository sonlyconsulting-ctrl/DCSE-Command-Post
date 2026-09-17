const { defineConfig, devices } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

// Check if pre-installed chromium exists
const chromiumPath = '/opt/pw-browsers/chromium';
const usePreInstalledChromium = fs.existsSync(chromiumPath);

module.exports = defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.js',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 1,
  reporter: 'line',

  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },

    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 5'],
      },
    },
  ],

  ...(process.env.CI ? {} : {
    webServer: {
      command: 'python -m http.server 4173 --directory apps/escd/web',
      url: 'http://127.0.0.1:4173',
      reuseExistingServer: false,
    },
  }),

  ...(usePreInstalledChromium && {
    use: {
      baseURL: 'http://127.0.0.1:4173',
      trace: 'on-first-retry',
      launchArgs: ['--no-sandbox'],
    },
  }),
});

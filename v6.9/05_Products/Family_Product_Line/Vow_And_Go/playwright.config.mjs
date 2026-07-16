import { defineConfig } from "@playwright/test";

const hostedBaseURL = process.env.PLAYWRIGHT_BASE_URL;

export default defineConfig({
  testDir: "./tests",
  testMatch: "**/*.spec.mjs",
  timeout: 60_000,
  expect: { timeout: 8_000 },
  fullyParallel: false,
  workers: 1,
  forbidOnly: true,
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: hostedBaseURL || "http://127.0.0.1:4173",
    browserName: "chromium",
    colorScheme: "light",
    screenshot: "only-on-failure",
    trace: "retain-on-failure"
  },
  webServer: hostedBaseURL ? undefined : {
    command: "npm run serve:test",
    url: "http://127.0.0.1:4173",
    reuseExistingServer: false,
    timeout: 20_000
  },
  projects: [
    {
      name: "desktop",
      use: { viewport: { width: 1440, height: 1000 } }
    },
    {
      name: "tablet",
      testIgnore: "**/desktop-only.spec.mjs",
      use: { viewport: { width: 900, height: 1180 }, hasTouch: true }
    },
    {
      name: "mobile",
      testIgnore: "**/desktop-only.spec.mjs",
      use: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }
    }
  ]
});

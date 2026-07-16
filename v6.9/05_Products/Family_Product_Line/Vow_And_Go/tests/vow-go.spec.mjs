import { test, expect } from "@playwright/test";

const errorsFor = (page) => {
  const errors=[]; page.on("pageerror",(error)=>errors.push(error.message));
  page.on("console",(message)=>{ if(message.type()==="error" && !message.text().includes("Failed to load resource")) errors.push(message.text()); });
  return errors;
};

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.clear());
});

test("signed-out and guest views expose only approved experience modules", async ({ page, isMobile }) => {
  const errors=errorsFor(page); await page.goto("/?role=signed_out&mode=experience_only");
  await expect(page.getByRole("heading",{name:"Dashboard"})).toBeVisible();
  if(isMobile) await page.getByRole("button",{name:"Open navigation"}).click();
  for(const title of ["Our Story","Media & Gallery Portal","Schedule & Timeline","Travel & Hotel","Destination & Local Guide","Music & Playlists","Communications & Notifications","Feedback & Support"]) await expect(page.getByRole("button",{name:title,exact:true})).toBeVisible();
  await expect(page.getByRole("button",{name:"Budget & Payments",exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Media & Gallery Portal",exact:true}).click();
  await expect(page.getByText("Cabo engagement portrait")).toBeVisible();
  await expect(page.getByText("Guest upload awaiting review")).toHaveCount(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth)).toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
});

test("planner full-command-center navigation and CRUD are operational", async ({ page, isMobile }) => {
  await page.goto("/?role=planner&mode=full_command_center");
  if(isMobile) await page.getByRole("button",{name:"Open navigation"}).click();
  for(const title of ["Wedding Tasks & Checklist","Vendors & Contracts","Budget & Payments","Guests & Wedding Party","Wedding Party Hub","Settings & Access"]) await expect(page.getByRole("button",{name:title,exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true}).click();
  await page.getByRole("button",{name:"Add record",exact:true}).click();
  await page.getByLabel("Task").fill("Confirm keyboard-accessible itinerary");
  await page.getByLabel("Select Task").selectOption("Wedding Day");
  await page.getByLabel("Status").selectOption("in_progress");
  await page.getByRole("button",{name:"Save record"}).click();
  await expect(page.getByText("Confirm keyboard-accessible itinerary")).toBeVisible();
  const row=page.locator(".record-card",{hasText:"Confirm keyboard-accessible itinerary"});
  await row.getByRole("button",{name:"Archive"}).click();
  await page.getByText(/Archived records/).click();
  await expect(row).toHaveCount(0);
  await page.locator(".archive-drawer .record-card",{hasText:"Confirm keyboard-accessible itinerary"}).getByRole("button",{name:"Restore"}).click();
  await expect(page.getByText("Confirm keyboard-accessible itinerary")).toBeVisible();
});

test("engagement selector keeps records isolated", async ({ page }) => {
  await page.goto("/?role=planner&mode=full_command_center&engagement=akira-connor-2027&page=tasks");
  await page.getByRole("button",{name:"Add record"}).click(); await page.getByLabel("Task").fill("Akira-only task"); await page.getByRole("button",{name:"Save record"}).click();
  await expect(page.getByText("Akira-only task")).toBeVisible();
  await page.getByLabel("Wedding workspace").selectOption("hale-2028");
  await page.getByLabel("Product mode").selectOption("full_command_center");
  await page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true}).click();
  await expect(page.getByText("Akira-only task")).toHaveCount(0);
});

test("product mode hides planning modules and preserves their data", async ({ page }) => {
  await page.goto("/?role=planner&mode=full_command_center&page=settings");
  await page.getByLabel("Product mode").selectOption("experience_only");
  await expect(page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Settings & Access",exact:true}).click();
  await page.getByLabel("Product mode").selectOption("full_command_center");
  await page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true}).click();
  await expect(page.getByText("Confirm ceremony music")).toBeVisible();
});

test("wedding-party fitting records display private consent language", async ({ page }) => {
  await page.goto("/?role=couple_owner&mode=full_command_center&page=party");
  await expect(page.getByText("Upload only with the participant’s knowledge and permission. Fitting media remains private unless separately approved for publication.")).toBeVisible();
  await expect(page.getByRole("heading",{name:"Measurements & Fittings"})).toBeVisible();
});

test("guest participant uses token-scoped self service and cannot list guests", async ({ page }) => {
  await page.goto("/?role=guest_participant&mode=experience_only&page=guests");
  await expect(page.getByRole("heading",{name:"Your RSVP & party"})).toBeVisible();
  await expect(page.getByText("Jordan Rivera")).toHaveCount(0);
  await page.getByRole("button",{name:"Save my details"}).click();
  await expect(page.locator("#app-status")).toContainText("invitation only");
});

test("preview feedback is neither submitted nor stored", async ({ page }) => {
  await page.goto("/?role=couple_owner&mode=full_command_center&page=feedback");
  await page.getByRole("button",{name:"Add record"}).click();
  await page.getByLabel("Subject").fill("Mobile review feedback"); await page.getByLabel("Details").fill("Verify the guest navigation.");
  await page.getByRole("button",{name:"Save record"}).click();
  await expect(page.locator("#app-status")).toHaveText("Preview mode: your feedback was not submitted or stored.");
  await expect(page.getByText("Mobile review feedback")).toHaveCount(0);
});

test("unsafe external URL is rejected", async ({ page }) => {
  await page.goto("/?role=couple_owner&mode=full_command_center&page=music");
  await page.getByRole("button",{name:"Add record"}).click(); await page.getByLabel("Playlist title").fill("Unsafe test"); await page.getByLabel("Provider URL").fill("javascript:alert(1)");
  await page.getByRole("button",{name:"Save record"}).click(); await expect(page.locator("#app-status")).toContainText("safe HTTPS URL");
});

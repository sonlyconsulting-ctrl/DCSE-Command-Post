import { test, expect } from "@playwright/test";
import { createRequire } from "node:module";
const require=createRequire(import.meta.url); const axePath=require.resolve("axe-core/axe.min.js");

test.beforeEach(async({page})=>page.addInitScript(()=>localStorage.clear()));

test("keyboard focus is visible and navigation activates",async({page})=>{
  await page.goto("/?role=planner&mode=full_command_center"); const button=page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true}); await button.focus();
  const style=await button.evaluate((element)=>({outline:getComputedStyle(element).outlineStyle,width:getComputedStyle(element).outlineWidth})); expect(style.outline).not.toBe("none");expect(style.width).not.toBe("0px");
  await page.keyboard.press("Enter"); await expect(page.getByRole("heading",{name:"Wedding Tasks & Checklist"})).toBeVisible();
});

test("reduced motion eliminates meaningful duration",async({page})=>{
  await page.emulateMedia({reducedMotion:"reduce"});await page.goto("/?role=couple_owner");
  const duration=await page.locator(".hero").evaluate((element)=>getComputedStyle(element).transitionDuration); expect(["0s","0.00001s","1e-05s"]).toContain(duration);
});

test("role navigation denies forbidden surfaces",async({page})=>{
  await page.goto("/?role=trusted_contributor&mode=full_command_center");
  await expect(page.getByRole("button",{name:"Budget & Payments",exact:true})).toHaveCount(0); await expect(page.getByRole("button",{name:"Settings & Access",exact:true})).toHaveCount(0);
  await expect(page.getByRole("button",{name:"Media & Gallery Portal",exact:true})).toBeVisible();
});

test("page has no serious or critical automated accessibility findings",async({page})=>{
  await page.goto("/?role=couple_owner&mode=full_command_center");await page.addScriptTag({path:axePath});
  const results=await page.evaluate(async()=>window.axe.run(document,{resultTypes:["violations"]}));
  expect(results.violations.filter((item)=>["serious","critical"].includes(item.impact))).toEqual([]);
});

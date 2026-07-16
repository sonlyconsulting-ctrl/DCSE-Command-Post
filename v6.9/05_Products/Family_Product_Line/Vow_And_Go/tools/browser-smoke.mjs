import { chromium } from "@playwright/test";
import assert from "node:assert/strict";

const base = process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:4173";
const viewports = [{name:"desktop",width:1440,height:1000},{name:"tablet",width:900,height:1180},{name:"mobile",width:390,height:844}];
const browser = await chromium.launch({ headless: true, args: ["--disable-gpu", "--disable-dev-shm-usage"] });
let failures = 0;

for (const viewport of viewports) {
  const page = await browser.newPage({ viewport });
  const errors=[]; page.on("pageerror",(error)=>errors.push(error.message));
  try {
    await page.goto(`${base}/?role=planner&mode=full_command_center`,{waitUntil:"domcontentloaded",timeout:15000});
    await page.waitForSelector("h1",{timeout:8000});
    assert.equal(await page.locator("h1").textContent(),"Dashboard");
    if(viewport.name==="mobile") await page.getByRole("button",{name:"Open navigation"}).click();
    await page.getByRole("button",{name:"Wedding Tasks & Checklist",exact:true}).click();
    await page.getByRole("button",{name:"Add record",exact:true}).click();
    await page.getByLabel("Task").fill(`${viewport.name} smoke task`);
    await page.getByRole("button",{name:"Save record"}).click();
    await page.getByText(`${viewport.name} smoke task`).waitFor();
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    assert.ok(overflow<=1,`horizontal overflow ${overflow}`);
    assert.deepEqual(errors,[]);
    console.log(`PASS ${viewport.name}: navigation, CRUD, responsive overflow, console`);
  } catch(error) { failures+=1; console.error(`FAIL ${viewport.name}: ${error.message}`); }
  await page.close();
}

const guest = await browser.newPage({viewport:{width:390,height:844}});
try {
  await guest.goto(`${base}/?role=signed_out&mode=experience_only&page=media`,{waitUntil:"domcontentloaded"});
  assert.equal(await guest.getByText("Guest upload awaiting review").count(),0);
  assert.equal(await guest.getByRole("button",{name:"Budget & Payments",exact:true}).count(),0);
  console.log("PASS signed-out: private media and admin navigation hidden");
} catch(error) { failures+=1; console.error(`FAIL signed-out: ${error.message}`); }
await guest.close(); await browser.close();
console.log(`BROWSER_SMOKE failures=${failures}`);
process.exit(failures?1:0);

import test from "node:test";
import assert from "node:assert/strict";
import {
  buildFeedbackMailto,
  canAdmin,
  canContribute,
  escapeHtml,
  safeBackgroundImage,
  safeExternalUrl,
  safeFileName,
  weddingCountdown
} from "../vow-go-core.js";

test("role capabilities preserve admin and contributor boundaries", () => {
  assert.equal(canAdmin("owner"), true);
  assert.equal(canAdmin("planner"), true);
  assert.equal(canAdmin("contributor"), false);
  assert.equal(canContribute("contributor"), true);
  assert.equal(canContribute(null), false);
});

test("unsafe HTML is escaped before rendering", () => {
  assert.equal(escapeHtml("<img src=x onerror=alert(1)>"), "&lt;img src=x onerror=alert(1)&gt;");
});

test("external URL validation rejects unsafe or wrong-provider links", () => {
  assert.equal(safeExternalUrl("javascript:alert(1)", "https"), "");
  assert.equal(safeExternalUrl("http://drive.google.com/file", "drive"), "");
  assert.equal(safeExternalUrl("https://evil.example/file", "drive"), "");
  assert.match(safeExternalUrl("https://drive.google.com/file/d/123", "drive"), /^https:\/\/drive\.google\.com\//);
  assert.match(safeExternalUrl("https://www.dropbox.com/s/example", "dropbox"), /^https:\/\/www\.dropbox\.com\//);
});

test("background images accept HTTPS only", () => {
  assert.equal(safeBackgroundImage("data:text/html,unsafe"), "");
  assert.match(safeBackgroundImage("https://images.example/review.jpg"), /https:\/\/images\.example\/review\.jpg/);
});

test("upload file names are normalized", () => {
  assert.equal(safeFileName("../../wedding photo<script>.jpg"), "wedding_photo_script_.jpg");
});

test("feedback mailto encodes subject and details", () => {
  const mailto = buildFeedbackMailto({
    supportEmail: "sonlyconsulting@gmail.com",
    type: "bug",
    severity: "high",
    subject: "Review & test",
    details: "Line one\nLine two",
    saved: false
  });
  assert.match(mailto, /^mailto:/);
  assert.doesNotMatch(mailto, /\n/);
  assert.match(mailto, /Review%20%26%20test/);
});

test("countdown produces stable positive parts", () => {
  const result = weddingCountdown("2027-06-12T16:00:00-10:00", new Date("2026-06-12T16:00:00-10:00"));
  assert.equal(result.complete, false);
  assert.ok(result.days >= 364);
  assert.ok(result.days <= 366);
});

// Kiểm thử đầu-cuối tab Sách trên bản tự host (web/index.html) với sách thật trong books/.
// Chạy: node tests/web/book.e2e.mjs        (cần Playwright: npm i -g playwright, có Chromium)
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import assert from "node:assert/strict";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const BOOK = path.join(ROOT, "books/ielts_target_5_0");
const PORT = 8000 + Math.floor(Math.random() * 900);

function loadPlaywright(){
  for(const base of [import.meta.url, "file:///opt/node-tools/node_modules/", path.join(process.execPath, "../../lib/node_modules/")]){
    try{ return createRequire(base)("playwright"); }catch(e){ /* thử chỗ khác */ }
  }
  console.log("SKIP: chưa cài Playwright"); process.exit(0);
}
const { chromium } = loadPlaywright();

const server = spawn("python3", [path.join(ROOT, "web/serve.py"), "--port", String(PORT)], { stdio: "ignore" });
const stop = () => { try{ server.kill(); }catch(e){} };
process.on("exit", stop);
await new Promise(r => setTimeout(r, 800));

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
const page = await ctx.newPage();
const errors = [];
page.on("pageerror", e => errors.push(e.message));
let pdfBytes = 0;
page.on("response", r => { if(r.url().endsWith(".pdf") && r.status() < 300) pdfBytes += Number(r.headers()["content-length"] || 0); });

const step = async (name, fn) => { process.stdout.write("· " + name + " … "); await fn(); console.log("ok"); };
const URL0 = `http://localhost:${PORT}/web/index.html`;

try{
  await step("mở app, đặt tên học viên, các tab cũ vẫn chạy", async () => {
    await page.goto(URL0);
    await page.fill("#suName", "E2E Học Viên");
    await page.click("#suSave");
    for(const tab of ["road", "practice", "res", "docs", "prog", "today"]){
      await page.click(`nav button[data-go="${tab}"]`);
      assert.ok(await page.isVisible("#p-" + tab), tab);
    }
    assert.ok((await page.locator("#tBlocks .blk").count()) > 0);
  });

  await step("menu Sách: danh sách sách kèm trình độ và thời lượng", async () => {
    await page.click('nav button[data-go="book"]');
    await page.waitForSelector("#p-book .bk-lib");
    const lib = await page.textContent("#p-book");
    assert.match(lib, /IELTS Target 5\.0/);
    assert.match(lib, /Band 3\.5 → 5\.0/);
    assert.match(lib, /Khoảng 4–5,5 tháng/);
    assert.match(lib, /Cambridge IELTS 20 General Training/);          // sách trong lộ trình chưa nhập
    assert.match(lib, /Chưa nhập vào app/);
  });

  await step("chi tiết sách: đủ section, unit, 120 phiên và phiên kế tiếp", async () => {
    await page.click("#p-book .bk-lib .btn-primary");
    await page.waitForSelector("#p-book .bk-next");
    assert.match(await page.textContent("#p-book .bk-next"), /Unit 1 · Speaking & Vocabulary/);
    assert.equal(await page.locator("#p-book .bk-unit").count(), 21);  // 15 unit + 3 review + 3 test
    assert.equal(await page.locator("#p-book .bk-row").count(), 120);
    assert.equal(await page.locator("#p-book .phase-head").count(), 3);
  });

  await step("mở phiên, xem trang sách qua đoạn PDF nhỏ", async () => {
    await page.click("#p-book .bk-next .btn-primary");
    await page.click("#p-book .bk-act .btn-primary");
    await page.waitForFunction(() => {
      const c = document.querySelector(".bk-viewer canvas");
      const m = document.querySelector(".bk-viewer .bk-msg");
      return c && c.width > 100 && m && m.hidden;
    }, null, { timeout: 30000 });
    assert.match(await page.textContent(".bk-vfoot"), /Trang 10 trong sách/);
    await page.click(".bk-vfoot button:last-child");           // trang sau
    await page.waitForFunction(() => /Trang 11/.test(document.querySelector(".bk-vfoot").textContent));
    assert.ok(pdfBytes < 15e6, "tải quá nhiều PDF: " + pdfBytes);
    await page.click(".bk-vbar button:last-child");            // đóng
  });

  await step("hoàn thành phiên: cộng giờ học, chuyển sang phiên kế tiếp", async () => {
    await page.click("#p-book .card button.btn-primary >> text=Bắt đầu phiên");
    await page.fill("#bkMin", "60");
    await page.fill("#bkNote", "e2e");
    await page.click("text=Hoàn thành phiên");
    await page.waitForSelector("#p-book .bk-next");
    assert.match(await page.textContent("#p-book .bk-next"), /Unit 1 · Listening/);
    const hours = await page.evaluate(() => { const d = new Date(); const k = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); return S.hours[k]; });
    assert.equal(hours, 1);
  });

  await step("chọn học tự do Unit 7, rồi quay về theo lộ trình", async () => {
    await page.locator("#p-book .bk-unit", { hasText: "Unit 7 · Movement" }).locator("button.btn").first().click();
    await page.waitForSelector("#p-book .bk-act");
    assert.match(await page.textContent("#p-book .reader-title"), /Unit 7 · Speaking & Vocabulary/);
    await page.click("#p-book .reader-bar button");
    await page.waitForSelector("#p-book .bk-next");
    assert.match(await page.textContent("#p-book .bk-next"), /unit tự chọn[\s\S]*Unit 7 · Speaking/);
    await page.click("#p-book .bk-next >> text=Quay về theo lộ trình");
    await page.waitForFunction(() => /Unit 1 · Listening/.test(document.querySelector("#p-book .bk-next").textContent));
  });

  await step("phiên Listening phát được audio", async () => {
    await page.click("#p-book .bk-next .btn-primary");
    await page.waitForFunction(() => { const a = document.querySelector("#p-book audio"); return a && a.duration > 0; }, null, { timeout: 15000 });
    await page.click("#p-book .bk-ctl >> text=+5s");
    assert.ok(await page.evaluate(() => document.querySelector("#p-book audio").currentTime) >= 4.9);
    await page.click("#p-book .reader-bar button");
  });

  await step("tải lại trang, tiến độ sách vẫn còn", async () => {
    await page.reload();
    await page.click('nav button[data-go="book"]');
    await page.waitForSelector("#p-book .bk-lib");
    assert.match(await page.textContent("#p-book .bk-lib"), /Đã xong 1\/120 phiên/);
    await page.click("#p-book .bk-lib .btn-primary");
    await page.waitForSelector("#p-book .bk-stat");
    assert.match(await page.textContent("#p-book .bk-stat"), /1\/120/);
  });

  await step("nhập file từ máy vào IndexedDB", async () => {
    await page.click("#p-book summary >> text=Quản lý file sách");
    await page.setInputFiles('#p-book input[type="file"]', [
      path.join(BOOK, "Target5.0_Listening_R_audio/Unit1_listening_1c.mp3"),
      path.join(BOOK, "web/course-book-p0011-0022.pdf"),
      path.join(ROOT, "README.md"),
    ]);
    await page.waitForFunction(() => /Đã lưu 2 file/.test(document.querySelector("#p-book .bk-msg:last-of-type")?.textContent || "")
      || [...document.querySelectorAll("#p-book .bk-msg")].some(e => /Đã lưu 2 file/.test(e.textContent)), null, { timeout: 15000 });
  });

  await step("trình xem đọc trang từ đoạn PDF đã nhập (không qua máy chủ)", async () => {
    await page.route("**/books/**/web/course-book-p0011-0022.pdf", r => r.abort());   // máy chủ không còn file này
    await page.click("#p-book .bk-row >> nth=0");
    await page.click("#p-book .bk-act .btn-primary");
    await page.waitForFunction(() => {
      const c = document.querySelector(".bk-viewer canvas");
      const m = document.querySelector(".bk-viewer .bk-msg");
      return c && c.width > 100 && m && m.hidden;
    }, null, { timeout: 30000 });
    await page.click(".bk-vbar button:last-child");
  });

  await step("xem checklist triển khai ngay trong app", async () => {
    await page.click('nav button[data-go="book"]');
    assert.match(await page.textContent("#p-book"), /Đã xong\s*\d+\/\d+ task/);
    await page.click("#p-book >> text=Checklist triển khai");
    await page.waitForSelector("#docView:not([hidden])");
    assert.equal(await page.textContent("#docTitle"), "Checklist triển khai agent");
    assert.ok(await page.locator("#docBody .md-cb.on").count() > 10);
    await page.click("#docBody a[data-doc] >> text=05-lich-su-thay-doi.md");   // link tương đối giữa tài liệu
    await page.waitForFunction(() => document.getElementById("docTitle").textContent === "Lịch sử thay đổi");
  });

  assert.deepEqual(errors, [], "lỗi JS trên trang: " + errors.join(" | "));
  console.log("E2E OK");
}catch(e){
  console.error("\nE2E FAIL:", e.message);
  await page.screenshot({ path: path.join(ROOT, "e2e-fail.png"), fullPage: true }).catch(() => {});
  process.exitCode = 1;
}finally{
  await browser.close();
  stop();
}

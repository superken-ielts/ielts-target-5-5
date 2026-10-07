// Chạy: node --test "tests/web/*.test.mjs"
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync, existsSync } from "node:fs";

const require = createRequire(import.meta.url);
const C = require("../../web/src/book/core.js");

const plan = {
  startWeek: 6, sessionsPerWeek: 6,
  sessions: Array.from({ length: 14 }, (_, i) => ({
    id: "S1-U01-" + (i + 1), seq: i + 1, item: "U01", section: "S1",
    step: ["speaking-vocab", "listening", "reading", "writing-learn", "writing-review", "consolidation", "workbook"][i % 7],
    core: [0, 3, 4].includes(i % 7), title: "s" + (i + 1)
  }))
};

test("phiên kế tiếp là phiên chưa xong đầu tiên, bỏ qua phiên đã xong hoặc đã bỏ", () => {
  let p = C.emptyProgress("b");
  assert.equal(C.nextSession(plan, p).id, "S1-U01-1");
  p = C.setSession(p, "S1-U01-1", { st: "done" }, 1);
  p = C.setSession(p, "S1-U01-2", { st: "skipped" }, 2);
  p = C.setSession(p, "S1-U01-3", { st: "doing" }, 3);
  assert.equal(C.nextSession(plan, p).id, "S1-U01-3");
  const c = C.counts(plan, p);
  assert.deepEqual([c.done, c.skipped, c.doing, c.todo], [1, 1, 1, 11]);
});

test("tuần dự kiến theo cài đặt, và dự báo tuần xong theo số phiên còn lại", () => {
  let p = C.emptyProgress("b");
  assert.equal(C.plannedWeek(plan, p, plan.sessions[6]), 7);          // phiên 7, 6 phiên/tuần
  p = C.setSettings(p, { sessionsPerWeek: 7 }, 1);
  assert.equal(C.plannedWeek(plan, p, plan.sessions[6]), 6);
  assert.equal(C.projectFinishWeek(plan, p, 1), 7);                    // 14 phiên / 7 → tuần 6–7
  assert.equal(C.projectFinishWeek(plan, p, 10), 11);                  // đang trễ: tính từ tuần hiện tại
  plan.sessions.forEach(s => { p = C.setSession(p, s.id, { st: "done" }, 2); });
  assert.equal(C.projectFinishWeek(plan, p, 10), null);
});

test("phiên lõi không bao giờ được bỏ qua", () => {
  plan.sessions.forEach(s => assert.equal(C.canSkip(s), !s.core));
  assert.equal(C.canSkip({ core: true }), false);
});

test("hợp nhất theo từng phiên: bản ghi mới hơn thắng, không mất phiên của máy kia", () => {
  let a = C.emptyProgress("b"), b = C.emptyProgress("b");
  a = C.setSession(a, "x", { st: "done" }, 10);
  b = C.setSession(b, "x", { st: "todo" }, 20);       // máy B bỏ đánh dấu sau
  a = C.setSession(a, "y", { st: "done" }, 5);         // chỉ máy A có
  b = C.setSession(b, "z", { st: "doing" }, 7);        // chỉ máy B có
  b = C.setSettings(b, { sessionsPerWeek: 5 }, 30);
  const m = C.mergeProgress(a, b);
  assert.equal(m.sessions.x.st, "todo");
  assert.equal(m.sessions.y.st, "done");
  assert.equal(m.sessions.z.st, "doing");
  assert.equal(m.settings.sessionsPerWeek, 5);
  assert.deepEqual(C.mergeProgress(a, b), C.mergeProgress(b, a));
});

test("đồng hồ tính theo mốc thời gian", () => {
  assert.equal(C.elapsedSec({ acc: 60 }, 1e6), 60);
  assert.equal(C.elapsedSec({ acc: 60, run: 1_000_000 }, 1_090_000), 150);
  assert.equal(C.fmtClock(4500), "75:00");
  assert.equal(C.fmtClock(-65), "-1:05");
});

test("tìm đoạn PDF chứa trang, ưu tiên đoạn chứa trọn khoảng trang của phiên", () => {
  const f = { kind: "pdf", path: "a.pdf", pages: 40, chunks: [
    { path: "web/a-p0001-0012.pdf", from: 1, to: 12 },
    { path: "web/a-p0012-0020.pdf", from: 12, to: 20 }] };
  assert.equal(C.chunkFor(f, 12, [12, 13]).path, "web/a-p0012-0020.pdf");
  assert.equal(C.chunkFor(f, 12, null).path, "web/a-p0001-0012.pdf");
  assert.equal(C.chunkFor(f, 30, null), null);
  assert.equal(C.chunkFor({ path: "b.pdf" }, 1, null), null);
});

test("ghép file chọn từ máy với file gốc và các đoạn", () => {
  const book = { files: {
    "course-book": { kind: "pdf", path: "Book.pdf", chunks: [{ path: "web/course-book-p0001-0010.pdf", from: 1, to: 10 }] },
    "U01-L1C": { kind: "audio", path: "audio/Unit1_listening_1c.mp3" } } };
  const { hit, miss } = C.matchFiles(book, ["Unit1_listening_1c.mp3", "course-book-p0001-0010.pdf", "other.mp3"]);
  assert.deepEqual(hit.map(h => h.path), ["audio/Unit1_listening_1c.mp3", "web/course-book-p0001-0010.pdf"]);
  assert.deepEqual(miss, ["other.mp3"]);
  assert.deepEqual(C.requiredPaths(book), ["web/course-book-p0001-0010.pdf", "audio/Unit1_listening_1c.mp3"]);
});

const BOOK = new URL("../../books/ielts_target_5_0/", import.meta.url);
test("gói IELTS Target 5.0: mọi phiên trỏ tới hoạt động có thật, mọi trang nằm trong một đoạn", { skip: !existsSync(new URL("book.json", BOOK)) }, () => {
  const book = JSON.parse(readFileSync(new URL("book.json", BOOK)));
  const p = JSON.parse(readFileSync(new URL("plan.json", BOOK)));
  const acts = C.activitiesOf(book);
  assert.equal(p.sessions.length, 120);
  p.sessions.forEach(s => s.activityIds.forEach(id => assert.ok(acts[id], s.id + " → " + id)));
  Object.values(acts).forEach(a => {
    for(const r of [a, a.answer, a.script, a.vocab, ...(a.alt || [])].filter(r => r && r.pdf && r.pages)){
      const f = book.files[r.pdf];
      if(f.chunks && f.chunks.length) assert.ok(C.chunkFor(f, r.pages[0], r.pages), a.id + " " + r.pages);
    }
  });
  assert.equal(C.nextSession(p, C.emptyProgress(book.id)).id, "S1-U01-1");
});

test("học unit tự chọn: phiên kế tiếp đi theo unit đó tới khi xong rồi quay về lộ trình", () => {
  const p2 = { startWeek: 6, sessionsPerWeek: 6, minutesPerSession: 75, sessions: [
    ...["U01", "U02"].flatMap(u => [1, 2].map(n => ({ id: "S1-" + u + "-" + n, seq: 0, item: u, core: false }))) ] };
  p2.sessions.forEach((s, i) => { s.seq = i + 1; });
  let p = C.emptyProgress("b");
  assert.equal(C.nextSession(p2, p).id, "S1-U01-1");
  p = C.setSettings(p, { focus: "U02" }, 1);
  assert.equal(C.focusOf(p2, p), "U02");
  assert.equal(C.nextSession(p2, p).id, "S1-U02-1");
  assert.equal(C.entrySession(p2, p, "U02").id, "S1-U02-1");
  p = C.setSession(p, "S1-U02-1", { st: "done" }, 2);
  p = C.setSession(p, "S1-U02-2", { st: "done" }, 3);
  assert.equal(C.focusOf(p2, p), null);                       // unit tự chọn đã xong
  assert.equal(C.nextSession(p2, p).id, "S1-U01-1");          // quay về thứ tự lộ trình
  assert.equal(C.entrySession(p2, p, "U02").id, "S1-U02-1");  // ôn lại: mở phiên đầu
  assert.deepEqual(C.itemCounts(p2, p, "U02"), { total: 2, done: 2 });
});

test("thời lượng sách theo nhịp học", () => {
  const p120 = { minutesPerSession: 75, sessions: Array.from({ length: 120 }, () => ({})) };
  assert.deepEqual(C.duration(p120, 6), { sessions: 120, minutes: 9000, hours: 150, weeks: 20, months: 4.6 });
  assert.equal(C.duration(p120, 7).weeks, 18);
  assert.equal(C.duration(p120, 5).weeks, 24);
});

test("đếm task trong checklist theo giai đoạn", () => {
  const md = "- [x] **P0-01** a\n  - [x] con, không tính\n- [ ] **P0-02** b\n- [X] **P1-01** c\n- [ ] ghi chú không phải task";
  assert.deepEqual(C.checklistStats(md), { 0: { done: 1, total: 2 }, 1: { done: 1, total: 1 } });
});

test("video bài giảng: lọc theo hoạt động / unit, tìm phiên chứa video, chương đang phát", () => {
  const entry = { lessons: [
    { id: "U01-speaking-1", activity: "U01-speaking-vocab", item: "U01", chapters: [{ t: 0, title: "a" }, { t: 30, title: "b" }, { t: 90, title: "c" }] },
    { id: "U02-x", activity: "U02-listening", item: "U02", chapters: [] },
  ] };
  assert.deepEqual(C.lessonsOf(entry, { activity: "U01-speaking-vocab" }).map(l => l.id), ["U01-speaking-1"]);
  assert.deepEqual(C.lessonsOf(entry, { item: "U02" }).map(l => l.id), ["U02-x"]);
  assert.deepEqual(C.lessonsOf({}, { item: "U01" }), []);
  const pl = { sessions: [{ id: "A", activityIds: ["U01-listening"] }, { id: "B", activityIds: ["U01-speaking-vocab"] }] };
  assert.equal(C.lessonSession(pl, entry.lessons[0]).id, "B");
  assert.equal(C.lessonSession(pl, entry.lessons[1]), null);
  const l = entry.lessons[0];
  assert.deepEqual([C.chapterAt(l, 0), C.chapterAt(l, 29.9), C.chapterAt(l, 30), C.chapterAt(l, 500)], [0, 0, 1, 2]);
  assert.equal(C.chapterAt(entry.lessons[1], 10), -1);
  const groups = C.groupLessons([{ id: "x", activity: "A" }, { id: "y", activity: "B" }, { id: "z", activity: "A" }]);
  assert.deepEqual(groups.map(g => [g.activity, g.lessons.map(l => l.id)]), [["A", ["x", "z"]], ["B", ["y"]]]);
  assert.deepEqual(C.groupLessons(undefined), []);
  const ordered = C.groupLessons([{ id: "x", activity: "A" }, { id: "y", activity: "B" }, { id: "w", activity: "Q" }, { id: "z", activity: "A" }], ["B", "A"]);
  assert.deepEqual(ordered.map(g => g.activity), ["B", "A", "Q"]);
});

test("lặp khi nghe / xem: bài tiếp theo, hẹn giờ dừng, thời gian nghe trong ngày, lặp chương", () => {
  // phát 1 lần: hết thì dừng; lặp bài này: phát lại chính nó; lặp cả danh sách: sang bài sau, hết bài cuối quay về đầu
  assert.deepEqual([C.nextOnEnd("off", 0, 3), C.nextOnEnd("one", 1, 3), C.nextOnEnd("all", 1, 3), C.nextOnEnd("all", 2, 3)], [-1, 1, 2, 0]);
  assert.equal(C.nextOnEnd("all", 0, 1), 0);
  assert.equal(C.nextOnEnd("all", 0, 0), -1);
  assert.equal(C.nextOnEnd("lạ", 0, 3), -1);
  // hẹn giờ: null là không hẹn; không bao giờ âm
  assert.equal(C.sleepLeft(0, 500), null);
  assert.equal(C.sleepLeft(30, 600), 1200);
  assert.equal(C.sleepLeft(15, 5000), 0);
  // cộng dồn trong ngày, sang ngày mới đếm lại
  let day = C.addListen(null, "2026-10-07", 12.34);
  day = C.addListen(day, "2026-10-07", 60);
  assert.deepEqual(day, { d: "2026-10-07", sec: 72.3 });
  assert.deepEqual(C.addListen(day, "2026-10-08", 5), { d: "2026-10-08", sec: 5 });
  assert.deepEqual(C.addListen(day, "2026-10-07", -9), day);
  // lặp chương: chương cuối kéo tới hết video; chương ngoài phạm vi hoặc video không có độ dài thì không lặp được
  const l = { duration: 120, chapters: [{ t: 0, title: "a" }, { t: 30, title: "b" }, { t: 90, title: "c" }] };
  assert.deepEqual([C.chapterRange(l, 0), C.chapterRange(l, 1), C.chapterRange(l, 2)], [[0, 30], [30, 90], [90, 120]]);
  assert.equal(C.chapterRange(l, -1), null);
  assert.equal(C.chapterRange({ chapters: [{ t: 0 }] }, 0), null);
  // giờ:phút:giây khi từ một giờ trở lên
  assert.deepEqual([C.fmtHms(65), C.fmtHms(3725), C.fmtHms(7200), C.fmtHms(-3)], ["1:05", "1:02:05", "2:00:00", "0:00"]);
});

test("video bài giảng của IELTS Target 5.0: mỗi video trỏ tới hoạt động có thật và có file", { skip: !existsSync(new URL("lessons/lessons.json", BOOK)) }, () => {
  const book = JSON.parse(readFileSync(new URL("book.json", BOOK), "utf8"));
  const pl = JSON.parse(readFileSync(new URL("plan.json", BOOK), "utf8"));
  const { lessons } = JSON.parse(readFileSync(new URL("lessons/lessons.json", BOOK), "utf8"));
  const acts = C.activitiesOf(book);
  assert.ok(lessons.length >= 2);
  for(const l of lessons){
    assert.ok(acts[l.activity], l.activity);
    assert.ok(C.lessonSession(pl, l), "không phiên nào chứa " + l.activity);
    assert.ok(existsSync(new URL(l.file, BOOK)), l.file);
    assert.ok(l.duration > 60 && l.chapters.length > 0 && l.chapters[0].t === 0);
  }
  assert.deepEqual(C.lessonsOf({ lessons }, { item: "U01" }).map(l => l.id).sort(), ["U01-consolidation", "U01-exam-listening", "U01-exam-reading",
    "U01-listening-1", "U01-listening-2", "U01-reading-1", "U01-reading-2",
    "U01-speaking-1", "U01-speaking-2", "U01-vocabulary", "U01-writing-1", "U01-writing-2", "U01-writing-3"]);
  // mục lục theo thứ tự trong sách, không theo thứ tự chữ cái của lessons.json
  assert.deepEqual(C.groupLessons(C.lessonsOf({ lessons }, { item: "U01" }), Object.keys(acts)).map(g => [g.activity, g.lessons.map(l => l.id)]),
    [["U01-speaking-vocab", ["U01-speaking-1", "U01-speaking-2", "U01-vocabulary"]], ["U01-listening", ["U01-listening-1", "U01-listening-2"]],
     ["U01-reading", ["U01-reading-1", "U01-reading-2"]], ["U01-writing", ["U01-writing-1", "U01-writing-2", "U01-writing-3"]],
     ["U01-consolidation", ["U01-consolidation"]], ["U01-exam-practice", ["U01-exam-listening", "U01-exam-reading"]]]);
  assert.deepEqual(C.lessonsOf({ lessons }, { activity: "U01-writing" }).map(l => l.id), ["U01-writing-1", "U01-writing-2", "U01-writing-3"]);
  // Unit 2: đủ sáu phần có trang sách, theo thứ tự trong sách
  assert.deepEqual(C.groupLessons(C.lessonsOf({ lessons }, { item: "U02" }), Object.keys(acts)).map(g => [g.activity, g.lessons.map(l => l.id)]),
    [["U02-speaking-vocab", ["U02-speaking-1", "U02-speaking-2"]], ["U02-listening", ["U02-listening-1", "U02-listening-2", "U02-listening-3"]],
     ["U02-reading", ["U02-reading-1", "U02-reading-2"]], ["U02-writing", ["U02-writing-1", "U02-writing-2"]],
     ["U02-consolidation", ["U02-consolidation"]], ["U02-exam-practice", ["U02-exam-reading", "U02-exam-writing"]]]);
  // Unit 3: 11 video, đủ sáu phần
  assert.deepEqual(C.groupLessons(C.lessonsOf({ lessons }, { item: "U03" }), Object.keys(acts)).map(g => [g.activity, g.lessons.length]),
    [["U03-speaking-vocab", 2], ["U03-listening", 2], ["U03-reading", 2], ["U03-writing", 2], ["U03-consolidation", 1], ["U03-exam-practice", 2]]);
});

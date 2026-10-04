/* =========================================================
   SÁCH — HÀM THUẦN (web/src/book/core.js)
   Không đụng DOM, chạy được cả trong trang lẫn trong Node (tests/web).
   Dữ liệu: book.json + plan.json do agents/book_ingest sinh ra;
   tiến độ: { schema:"book-progress/1", bookId, settings:{...,t}, sessions:{id:{st,min,d,t,...}} }.
   ========================================================= */
const BookCore = (() => {
  const DONE = new Set(["done", "skipped"]);

  function emptyProgress(bookId){
    return { schema: "book-progress/1", bookId, settings: {}, sessions: {} };
  }

  function settingsOf(plan, progress){
    const s = (progress && progress.settings) || {};
    return {
      startWeek: Number(s.startWeek) || plan.startWeek,
      sessionsPerWeek: Number(s.sessionsPerWeek) || plan.sessionsPerWeek
    };
  }

  function statusOf(progress, id){
    const r = progress && progress.sessions && progress.sessions[id];
    return (r && r.st) || "todo";
  }

  function nextSession(plan, progress){
    return plan.sessions.find(s => !DONE.has(statusOf(progress, s.id))) || null;
  }

  function counts(plan, progress){
    const c = { total: plan.sessions.length, done: 0, skipped: 0, doing: 0, todo: 0, minutes: 0 };
    plan.sessions.forEach(s => {
      const st = statusOf(progress, s.id);
      c[st in c ? st : "todo"]++;
      const r = progress && progress.sessions && progress.sessions[s.id];
      if(r && r.min) c.minutes += Number(r.min) || 0;
    });
    return c;
  }

  /* Tuần dự kiến của một phiên theo cài đặt hiện tại (không theo ngày đã học). */
  function plannedWeek(plan, progress, session){
    const st = settingsOf(plan, progress);
    return st.startWeek + Math.floor((session.seq - 1) / st.sessionsPerWeek);
  }

  /* Tuần dự kiến học xong: tính từ tuần hiện tại và số phiên còn lại. */
  function projectFinishWeek(plan, progress, currentWeek){
    const st = settingsOf(plan, progress);
    const left = plan.sessions.filter(s => !DONE.has(statusOf(progress, s.id))).length;
    if(!left) return null;
    const from = Math.max(currentWeek, st.startWeek);
    return from + Math.ceil(left / st.sessionsPerWeek) - 1;
  }

  /* Phiên lõi (Speaking, Writing, bài Test) không bao giờ được bỏ qua. */
  function canSkip(session){ return !session.core; }

  function setSession(progress, id, patch, now){
    const out = JSON.parse(JSON.stringify(progress));
    const prev = out.sessions[id] || {};
    out.sessions[id] = Object.assign({}, prev, patch, { t: now });
    return out;
  }

  function setSettings(progress, patch, now){
    const out = JSON.parse(JSON.stringify(progress));
    out.settings = Object.assign({}, out.settings, patch, { t: now });
    return out;
  }

  /* Hợp nhất hai bản tiến độ theo từng phiên: bản ghi nào có t lớn hơn thì thắng.
     Không xóa vật lý — bỏ đánh dấu là ghi st:"todo" với t mới. */
  function mergeProgress(a, b){
    if(!a) return b; if(!b) return a;
    const out = emptyProgress(a.bookId || b.bookId);
    out.settings = ((b.settings && b.settings.t) || 0) > ((a.settings && a.settings.t) || 0)
      ? Object.assign({}, b.settings) : Object.assign({}, a.settings);
    const ids = new Set([...Object.keys(a.sessions || {}), ...Object.keys(b.sessions || {})]);
    ids.forEach(id => {
      const x = (a.sessions || {})[id], y = (b.sessions || {})[id];
      out.sessions[id] = !x ? y : !y ? x : ((y.t || 0) > (x.t || 0) ? y : x);
    });
    return out;
  }

  /* Đồng hồ phiên tính theo mốc thời gian, nên khóa màn hình hay đóng app vẫn đúng. */
  function elapsedSec(rec, now){
    if(!rec) return 0;
    const acc = Number(rec.acc) || 0;
    return rec.run ? acc + Math.max(0, Math.floor((now - rec.run) / 1000)) : acc;
  }

  function activitiesOf(book){
    const map = {};
    book.sections.forEach(sec => sec.items.forEach(item => item.activities.forEach(a => { map[a.id] = a; })));
    return map;
  }

  function itemsOf(book){
    const map = {};
    book.sections.forEach(sec => sec.items.forEach(item => { map[item.id] = Object.assign({ section: sec.id }, item); }));
    return map;
  }

  /* Trang PDF → số in trong sách (để hiện "trang 52 trong sách"). */
  function printedPage(book, fileId, pdfPage){
    const f = book.files[fileId];
    return f && f.kind === "pdf" ? pdfPage - (f.pageOffset || 0) : pdfPage;
  }

  function basename(p){ return String(p).split("/").pop(); }

  /* File cần có để học không cần máy chủ: PDF lớn thì là các đoạn (chunks), còn lại là file gốc. */
  function requiredPaths(book){
    const out = [];
    Object.values(book.files).forEach(f => {
      if(f.chunks && f.chunks.length) f.chunks.forEach(c => out.push(c.path));
      else out.push(f.path);
    });
    return out;
  }

  /* Ghép file người dùng chọn từ máy với file trong book.json theo tên file (file gốc hoặc đoạn). */
  function matchFiles(book, names){
    const byName = {};
    Object.entries(book.files).forEach(([id, f]) => {
      byName[basename(f.path)] = { id, path: f.path };
      (f.chunks || []).forEach(c => { byName[basename(c.path)] = { id, path: c.path, chunk: true }; });
    });
    const hit = [], miss = [];
    names.forEach(n => { (byName[basename(n)] ? hit : miss).push(n); });
    return { hit: hit.map(n => Object.assign({ name: n }, byName[basename(n)])), miss };
  }

  /* Đoạn PDF chứa trang (ưu tiên đoạn chứa trọn khoảng trang của phiên). */
  function chunkFor(file, page, range){
    if(!file || !file.chunks || !file.chunks.length) return null;
    if(range){
      const whole = file.chunks.find(c => c.from <= range[0] && range[1] <= c.to && c.from <= page && page <= c.to);
      if(whole) return whole;
    }
    return file.chunks.find(c => c.from <= page && page <= c.to) || null;
  }

  function fmtClock(sec){
    const s = Math.abs(Math.round(sec));
    return (sec < 0 ? "-" : "") + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
  }

  return {
    emptyProgress, settingsOf, statusOf, nextSession, counts, plannedWeek, projectFinishWeek,
    canSkip, setSession, setSettings, mergeProgress, elapsedSec, activitiesOf, itemsOf,
    printedPage, basename, matchFiles, requiredPaths, chunkFor, fmtClock
  };
})();
if(typeof module !== "undefined" && module.exports) module.exports = BookCore;

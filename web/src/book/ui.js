/* =========================================================
   SÁCH — GIAO DIỆN (web/src/book/ui.js)
   Tab Sách: menu học theo lộ trình từ book.json + plan.json (BOOKS do build.py nhúng),
   màn hình Phiên học, trình xem PDF (PDF.js), thanh audio, nhập file sách từ máy.
   Chỉ đọc biến chung của app (S, save, LS, rootSlug, PROFILE, DB, iso, today, weekNo,
   clampWeek, renderAll) — không sửa mã cũ. Tiến độ sách lưu riêng:
   localStorage <LS>:<slug>:book:<id> và db students/<slug>/books/<id>.
   ========================================================= */
const BookUI = (() => {
  const PDFJS_VER = "4.10.38";
  const PDFJS_LOCAL = "vendor/pdfjs/";
  const PDFJS_CDN = "https://cdn.jsdelivr.net/npm/pdfjs-dist@" + PDFJS_VER + "/legacy/build/";
  const BOOK_BASE = "../books/";
  const IDB_NAME = "ielts-books";
  const STEP_SKILL = {"speaking-vocab":"S", listening:"L", reading:"R", "writing-learn":"Wr", "writing-review":"Wr"};
  const SKILL_RAIL = {listening:"var(--sk-l)", reading:"var(--sk-r)", writing:"var(--sk-w)",
                      speaking:"var(--sk-s)", vocab:"var(--sk-v)", other:"var(--line-2)"};
  const STATUS_TXT = {todo:"chưa học", doing:"đang học", done:"đã xong", skipped:"bỏ qua"};

  let root = null;
  let view = {name:"home", bookId:null, sessionId:null};
  let PROG = {}, progSlug = null, pushTimer = null, tick = null, msg = "";
  const VPOS = {};  // vị trí đang xem của từng video bài giảng (trong phiên làm việc)
  const ACTS = {}, ITEMS = {};

  /* ---------- tiện ích DOM ---------- */
  function h(tag, cls, text){
    const e = document.createElement(tag);
    if(cls) e.className = cls;
    if(text != null) e.textContent = text;
    return e;
  }
  function btn(text, cls, onclick){
    const b = h("button", "btn " + (cls || "btn-sm"), text);
    b.type = "button"; b.onclick = onclick;
    return b;
  }
  function card(eyebrow){
    const c = h("div", "card");
    if(eyebrow) c.append(h("div", "eyebrow", eyebrow));
    return c;
  }
  function curWeek(){
    try{ return clampWeek(weekNo(today())); }catch(e){ return 1; }
  }
  function nowMs(){ return Date.now(); }

  /* ---------- tiến độ ---------- */
  function slug(){ try{ return rootSlug(); }catch(e){ return "mac-dinh"; } }
  function lsKey(id){ return LS + ":" + slug() + ":book:" + id; }
  function prog(id){
    if(progSlug !== slug()){ PROG = {}; progSlug = slug(); }
    if(!PROG[id]){
      let p = null;
      try{ p = JSON.parse(localStorage.getItem(lsKey(id)) || "null"); }catch(e){ p = null; }
      PROG[id] = p && p.sessions ? p : BookCore.emptyProgress(id);
    }
    return PROG[id];
  }
  function setProg(id, p){
    PROG[id] = p;
    try{ localStorage.setItem(lsKey(id), JSON.stringify(p)); }catch(e){ /* hết chỗ thì vẫn còn bản trên máy chủ */ }
    clearTimeout(pushTimer);
    pushTimer = setTimeout(() => push(id), 900);
  }
  function remote(id){
    if(typeof DB === "undefined" || !DB || !PROFILE || !PROFILE.slug) return null;
    return DB.doc("students/" + slug() + "/books/" + id);
  }
  function push(id){
    const doc = remote(id);
    if(doc) doc.set(JSON.parse(JSON.stringify(PROG[id]))).catch(() => {});
  }
  async function pull(id){
    const doc = remote(id);
    if(!doc) return;
    try{
      const snap = await doc.get();
      if(!snap.exists){ push(id); return; }
      const merged = BookCore.mergeProgress(prog(id), snap.data());
      if(JSON.stringify(merged) !== JSON.stringify(PROG[id])){
        PROG[id] = merged;
        try{ localStorage.setItem(lsKey(id), JSON.stringify(merged)); }catch(e){}
        render();
      }
      if(JSON.stringify(merged) !== JSON.stringify(snap.data())) push(id);
    }catch(e){ /* không có mạng thì dùng bản trên máy */ }
  }
  function update(id, sid, patch){
    setProg(id, BookCore.setSession(prog(id), sid, patch, nowMs()));
  }

  /* ---------- file sách: IndexedDB rồi tới máy chủ ---------- */
  function idb(){
    return new Promise((res, rej) => {
      if(!window.indexedDB){ rej(new Error("no-idb")); return; }
      const r = indexedDB.open(IDB_NAME, 1);
      r.onupgradeneeded = () => { if(!r.result.objectStoreNames.contains("blobs")) r.result.createObjectStore("blobs"); };
      r.onsuccess = () => res(r.result);
      r.onerror = () => rej(r.error);
    });
  }
  async function idbDo(mode, fn){
    const db = await idb();
    return new Promise((res, rej) => {
      const tx = db.transaction("blobs", mode);
      const out = fn(tx.objectStore("blobs"));
      tx.oncomplete = () => res(out && "result" in out ? out.result : undefined);
      tx.onerror = () => rej(tx.error);
    });
  }
  const idbGet = key => idbDo("readonly", st => st.get(key)).catch(() => null);
  const idbPut = (key, blob) => idbDo("readwrite", st => st.put(blob, key));
  const idbKeys = () => idbDo("readonly", st => st.getAllKeys()).catch(() => []);
  const idbDel = key => idbDo("readwrite", st => st.delete(key));

  function fileUrl(bookId, path){
    const rel = BOOK_BASE + BOOKS[bookId].dir + "/" + path.split("/").map(encodeURIComponent).join("/");
    try{ return new URL(rel, document.baseURI).href; }catch(e){ return rel; }
  }
  async function source(bookId, fileId){
    const f = BOOKS[bookId].book.files[fileId];
    const blob = await idbGet(bookId + ":" + f.path);
    return blob ? {blob, f} : {url: fileUrl(bookId, f.path), f};
  }
  /* Nguồn cho một trang PDF: đoạn đã nhập → file gốc đã nhập → đoạn trên máy chủ → file gốc trên máy chủ. */
  async function pdfSource(bookId, fileId, page, range){
    const f = BOOKS[bookId].book.files[fileId];
    const c = BookCore.chunkFor(f, page, range);
    if(c){
      const blob = await idbGet(bookId + ":" + c.path);
      if(blob) return {key: c.path, blob, first: c.from};
    }
    const whole = await idbGet(bookId + ":" + f.path);
    if(whole) return {key: f.path, blob: whole, first: 1};
    if(c) return {key: c.path, url: fileUrl(bookId, c.path), first: c.from};
    return {key: f.path, url: fileUrl(bookId, f.path), first: 1};
  }

  /* ---------- PDF.js: tải lười, ưu tiên bản vendor cạnh trang, dự phòng CDN ---------- */
  let pdfjsP = null;
  function pdfjs(){
    if(!pdfjsP){
      pdfjsP = (async () => {
        const bases = [];
        try{ bases.push(new URL(PDFJS_LOCAL, document.baseURI).href); }catch(e){}
        bases.push(PDFJS_CDN);
        for(const base of bases){
          try{
            const lib = await import(base + "pdf.min.mjs");
            lib.GlobalWorkerOptions.workerSrc = base + "pdf.worker.min.mjs";
            return lib;
          }catch(e){ /* thử nguồn kế tiếp */ }
        }
        throw new Error("Không tải được PDF.js");
      })();
      pdfjsP.catch(() => { pdfjsP = null; });
    }
    return pdfjsP;
  }
  const PDF_CACHE = {};
  function openPdf(bookId, src){
    const key = bookId + ":" + src.key + (src.blob ? ":blob" : ":url");
    if(!PDF_CACHE[key]){
      PDF_CACHE[key] = (async () => {
        const lib = await pdfjs();
        const opts = {isEvalSupported: false, rangeChunkSize: 262144, disableAutoFetch: true, disableStream: true};
        if(src.blob){
          // Đọc từng khoảng byte của Blob, không nạp nguyên file 100 MB vào bộ nhớ.
          class BlobRange extends lib.PDFDataRangeTransport {
            requestDataRange(begin, end){
              src.blob.slice(begin, end).arrayBuffer().then(buf => this.onDataRange(begin, new Uint8Array(buf)));
            }
          }
          opts.range = new BlobRange(src.blob.size, null);
        } else {
          opts.url = src.url;
        }
        return lib.getDocument(opts).promise;
      })();
      PDF_CACHE[key].catch(() => { delete PDF_CACHE[key]; });
    }
    return PDF_CACHE[key];
  }

  /* ---------- trình xem trang sách ---------- */
  function openViewer(bookId, ref, title){
    const book = BOOKS[bookId].book;
    const box = h("div", "bk-viewer");
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", title);
    const bar = h("div", "bk-vbar");
    const tt = h("div", "bk-vt", title);
    // Mức phóng: 100% = vừa bề ngang khung; thu nhỏ để xem trọn trang, phóng to tới 300%
    const ZOOMS = [0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3], FIT = 2;
    let zi = FIT, cssW = 0, cssH = 0;
    const zoomOut = btn("−", "btn-sm", () => setZoom(zi - 1));
    const zoomLbl = btn("100%", "btn-sm bk-zoom", () => setZoom(FIT));
    const zoomIn = btn("+", "btn-sm", () => setZoom(zi + 1));
    zoomOut.setAttribute("aria-label", "Thu nhỏ"); zoomIn.setAttribute("aria-label", "Phóng to");
    zoomLbl.setAttribute("aria-label", "Vừa khung"); zoomLbl.title = "Vừa khung (phím 0)";
    const close = btn("Đóng", "btn-sm", () => shut());
    bar.append(tt, zoomOut, zoomLbl, zoomIn, close);
    const body = h("div", "bk-vbody");
    let canvas = document.createElement("canvas");
    const status = h("p", "bk-msg", "Đang mở sách…");
    body.append(status, canvas);
    const foot = h("div", "bk-vfoot");
    const prev = btn("← Trang trước", "btn-sm", () => go(-1));
    const label = h("span", "small");
    const next = btn("Trang sau →", "btn-sm", () => go(1));
    foot.append(prev, label, next);
    box.append(bar, body, foot);
    document.body.append(box);
    document.body.style.overflow = "hidden";

    const total = book.files[ref.pdf].pages;
    let ready = false, page = ref.pages[0], renderTask = null, drawing = 0;
    const onKey = e => {
      if(e.key === "Escape") shut();
      if(e.key === "ArrowRight") go(1);
      if(e.key === "ArrowLeft") go(-1);
      if(e.key === "+" || e.key === "=") setZoom(zi + 1);
      if(e.key === "-") setZoom(zi - 1);
      if(e.key === "0") setZoom(FIT);
    };
    function paintZoom(){
      zoomLbl.textContent = Math.round(ZOOMS[zi] * 100) + "%";
      zoomOut.disabled = zi === 0;
      zoomIn.disabled = zi === ZOOMS.length - 1;
    }
    // Đổi cỡ ngay bằng CSS (thấy liền, giữ điểm giữa khung nhìn), rồi vẽ lại trang cho nét ở cỡ mới
    function setZoom(i){
      i = Math.max(0, Math.min(ZOOMS.length - 1, i));
      if(i === zi) return;
      const ratio = ZOOMS[i] / ZOOMS[zi];
      const cx = (body.scrollLeft + body.clientWidth / 2) / Math.max(1, body.scrollWidth);
      const cy = (body.scrollTop + body.clientHeight / 2) / Math.max(1, body.scrollHeight);
      zi = i;
      paintZoom();
      if(cssW){
        cssW *= ratio; cssH *= ratio;
        canvas.style.width = Math.floor(cssW) + "px";
        canvas.style.height = Math.floor(cssH) + "px";
        body.scrollLeft = cx * body.scrollWidth - body.clientWidth / 2;
        body.scrollTop = cy * body.scrollHeight - body.clientHeight / 2;
      }
      if(ready) draw(true);
    }
    paintZoom();
    document.addEventListener("keydown", onKey);

    function shut(){
      document.removeEventListener("keydown", onKey);
      if(renderTask) try{ renderTask.cancel(); }catch(e){}
      box.remove();
      document.body.style.overflow = "";
    }
    function go(d){
      if(!ready) return;
      page = Math.min(total, Math.max(1, page + d));
      draw();
    }
    async function draw(keepView){
      const my = ++drawing;
      const inRange = page >= ref.pages[0] && page <= ref.pages[1];
      label.textContent = "Trang " + BookCore.printedPage(book, ref.pdf, page) + " trong sách"
        + (inRange ? " · " + (page - ref.pages[0] + 1) + "/" + (ref.pages[1] - ref.pages[0] + 1) : " · ngoài phần của phiên");
      prev.disabled = page <= 1; next.disabled = page >= total;
      if(!keepView){ status.textContent = "Đang mở trang…"; status.hidden = false; status.className = "bk-msg"; }
      let src = null;
      try{
        src = await pdfSource(bookId, ref.pdf, page, inRange ? ref.pages : null);
        const doc = await openPdf(bookId, src);
        ready = true;
        if(my !== drawing) return;
        const p = await doc.getPage(page - src.first + 1);
        const base = p.getViewport({scale: 1});
        // cỡ hiển thị theo mức phóng; độ phân giải ảnh thì có trần (canvas của Safari iOS tối đa ~16 triệu điểm ảnh)
        const cssScale = Math.max(280, body.clientWidth - 20) * ZOOMS[zi] / base.width;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        let scale = cssScale * dpr;
        const maxPx = 16e6;
        if(base.width * base.height * scale * scale > maxPx) scale = Math.sqrt(maxPx / (base.width * base.height));
        const vp = p.getViewport({scale});
        // vẽ vào canvas mới rồi mới thay, để trang không chớp trắng khi phóng to / thu nhỏ
        const fresh = document.createElement("canvas");
        fresh.width = Math.floor(vp.width); fresh.height = Math.floor(vp.height);
        if(renderTask) try{ renderTask.cancel(); }catch(e){}
        renderTask = p.render({canvasContext: fresh.getContext("2d"), viewport: vp});
        await renderTask.promise;
        if(my !== drawing) return;
        cssW = base.width * cssScale; cssH = base.height * cssScale;
        fresh.style.width = Math.floor(cssW) + "px";
        fresh.style.height = Math.floor(cssH) + "px";
        const keep = keepView ? [body.scrollLeft, body.scrollTop] : [0, 0];
        canvas.replaceWith(fresh);
        canvas = fresh;
        status.hidden = true;
        body.scrollLeft = keep[0]; body.scrollTop = keep[1];
      }catch(e){
        if(e && e.name === "RenderingCancelledException") return;
        ready = true;
        status.className = "bk-msg err";
        status.textContent = "Không mở được " + (src ? BookCore.basename(src.key) : "trang này")
          + ". Nếu đang dùng bản trên Claude hoặc bản chỉ có index.html, vào tab Sách → Quản lý file sách → Nhập file sách từ máy.";
      }
    }
    draw();
  }

  /* ---------- lặp khi nghe / xem (thanh audio và video bài giảng) ----------
     Chế độ lặp và hẹn giờ dừng nhớ riêng cho audio / video trong trình duyệt này. Đếm số lượt đã nghe hết,
     thời gian nghe của lần này và của cả ngày — để nghe đi nghe lại một bài trong thời gian dài. */
  const REPEAT_MODES = ["off", "one", "all"];
  const SLEEP_MIN = [0, 15, 30, 45, 60, 90, 120, 180];
  function readJson(k){ try{ return JSON.parse(localStorage.getItem(k) || "null"); }catch(e){ return null; } }
  function writeJson(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){ /* hết chỗ hoặc bị chặn */ } }
  function listenKey(){ return LS + ":" + slug() + ":listen"; }
  function dayIso(){ try{ return iso(today()); }catch(e){ return new Date().toISOString().slice(0, 10); } }
  function fmtMin(m){ return m < 60 ? m + " phút" : Math.floor(m / 60) + " giờ" + (m % 60 ? " " + (m % 60) : ""); }
  let LISTEN = null;             // thời gian nghe trong ngày {d, sec}, dùng chung mọi thanh lặp trên trang
  const REP_PAINT = new Set();   // vẽ lại các thanh lặp đang hiện khi thời gian nghe trong ngày đổi

  /* kind "audio" | "video"; n bài trong danh sách; go(j) mở và phát bài j (0 ≤ j < n). Gắn từng media bằng attach(). */
  function repeater(kind, n, unit, go){
    const key = LS + ":repeat:" + kind;
    const saved = readJson(key) || {};
    const st = {mode: REPEAT_MODES.includes(saved.mode) ? saved.mode : "off",
                sleep: SLEEP_MIN.includes(saved.sleep) ? saved.sleep : 0};
    let laps = 0, heard = 0, since = null, note = "";
    LISTEN = readJson(listenKey());
    const el = h("div", "bk-rep");
    const seg = h("div", "seg");
    const cap = unit.charAt(0).toUpperCase() + unit.slice(1);
    const labels = {off: "Tắt", one: cap + " này", all: "Cả " + n + " " + unit};
    (n > 1 ? REPEAT_MODES : ["off", "one"]).forEach(m => {
      const b = h("button", null, labels[m]);
      b.type = "button"; b.dataset.mode = m;
      b.onclick = () => { st.mode = m; writeJson(key, st); paintMode(); };
      seg.append(b);
    });
    function paintMode(){
      const on = st.mode === "all" && n < 2 ? "one" : st.mode;  // một bài thì "lặp cả danh sách" cũng là lặp bài này
      [...seg.children].forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === on)));
    }
    const sel = document.createElement("select");
    sel.className = "inp bk-sleep";
    sel.setAttribute("aria-label", "Hẹn giờ dừng");
    SLEEP_MIN.forEach(m => {
      const o = h("option", null, m ? "Dừng sau " + fmtMin(m) : "Không hẹn giờ");
      o.value = String(m);
      sel.append(o);
    });
    sel.value = String(st.sleep);
    sel.onchange = () => {  // đổi hẹn giờ thì tính lại từ lúc này
      flush(); heard = 0; note = "";
      st.sleep = Number(sel.value) || 0; writeJson(key, st); paint();
    };
    const info = h("div", "tiny bk-rep-info", "");
    const top = h("div", "bk-rep-row");
    top.append(h("span", "bk-rep-k", "Lặp lại"), seg);
    const row = h("div", "bk-rep-row");
    row.append(sel, info);
    el.append(top, row);

    const live = () => since == null ? 0 : Math.max(0, nowMs() - since) / 1000;
    function flush(){  // cộng đoạn vừa nghe vào lần này và vào cả ngày (trần 2 phút, phòng máy ngủ giữa chừng)
      if(since == null) return;
      const d = Math.min(live(), 120);
      since = nowMs(); heard += d;
      LISTEN = BookCore.addListen(readJson(listenKey()), dayIso(), d);
      writeJson(listenKey(), LISTEN);
      REP_PAINT.forEach(r => { if(r.el.isConnected) r.paint(); else REP_PAINT.delete(r); });  // bỏ thanh của màn hình cũ
    }
    function paint(){
      const now = heard + live(), left = BookCore.sleepLeft(st.sleep, now);
      const daySec = (LISTEN && LISTEN.d === dayIso() ? LISTEN.sec : 0) + live();
      info.textContent = (note ? note + " · " : "") + (laps ? "Đã nghe hết " + laps + " lượt · " : "")
        + "Lần này " + BookCore.fmtHms(now) + (left != null && !note ? " (còn " + BookCore.fmtHms(left) + ")" : "")
        + " · Hôm nay " + BookCore.fmtHms(daySec);
    }
    function lap(){ laps++; paint(); }

    /* idx() là số thứ tự bài đang nằm trong media; ab là đoạn lặp A–B của media đó (nếu có). */
    function attach(media, idx, ab){
      media.addEventListener("play", () => {
        if(root) root.querySelectorAll("audio, video").forEach(m => { if(m !== media && !m.paused) m.pause(); });
        if(since == null) since = nowMs();
        note = ""; paint();
        if(n > 1 && "mediaSession" in navigator) try{  // nút bài trước / bài sau trên màn hình khóa theo bài vừa phát
          navigator.mediaSession.setActionHandler("nexttrack", () => go((idx() + 1) % n));
          navigator.mediaSession.setActionHandler("previoustrack", () => go((idx() + n - 1) % n));
        }catch(e){ /* trình duyệt không hỗ trợ */ }
      });
      media.addEventListener("pause", () => { flush(); since = null; paint(); });
      media.addEventListener("timeupdate", () => {
        // sự kiện pause của bài trước (cùng danh sách) đến sau play của bài này thì đồng hồ đã bị tắt: bật lại
        if(since == null && !media.paused) since = nowMs();
        if(ab && ab.jump()) lap();
        if(since != null && nowMs() - since >= 10000) flush();
        if(BookCore.sleepLeft(st.sleep, heard + live()) === 0){
          media.pause(); flush(); heard = 0;
          note = "Đã dừng theo hẹn giờ " + fmtMin(st.sleep);
        }
        paint();
      });
      media.addEventListener("ended", () => {
        if(ab && ab.active()){ media.currentTime = ab.a; media.play().catch(() => {}); lap(); return; }
        const i = idx(), j = BookCore.nextOnEnd(st.mode, i, n);
        lap();
        if(j < 0) return;
        if(j === i){ media.currentTime = 0; media.play().catch(() => {}); }
        else go(j);
      });
    }
    REP_PAINT.add({el, paint});
    paintMode(); paint();
    return {el, attach};
  }

  /* Đoạn lặp A–B trên một audio / video: phát tới B thì quay về A. range(t) (nếu có) cho nút "Lặp chương này". */
  function abLoop(media, range){
    const ab = {a: null, b: null, byChapter: false};
    const txt = h("span", "tiny bk-ab", "");
    const paint = () => {
      txt.textContent = ab.a == null ? "" : (ab.byChapter ? "Lặp chương " : "Lặp ")
        + BookCore.fmtClock(ab.a) + (ab.b == null ? " → …" : " → " + BookCore.fmtClock(ab.b));
    };
    ab.set = (a, b, byChapter) => { ab.a = a; ab.b = b; ab.byChapter = !!byChapter; paint(); };
    ab.active = () => ab.a != null && ab.b != null;
    ab.jump = () => {
      if(!ab.active() || media.currentTime < ab.b) return false;
      media.currentTime = ab.a;
      return true;
    };
    const setA = btn("A", "btn-sm", () => ab.set(media.currentTime || 0, null));
    const setB = btn("B", "btn-sm", () => { if(ab.a != null && media.currentTime > ab.a) ab.set(ab.a, media.currentTime); });
    const clr = btn("Bỏ lặp A–B", "btn-sm", () => ab.set(null, null));
    setA.title = "Đặt điểm đầu đoạn lặp"; setB.title = "Đặt điểm cuối đoạn lặp";
    ab.els = [setA, setB];
    if(range){
      ab.chapter = t => {  // lặp chương chứa thời điểm t, nhảy về đầu chương nếu đang ở ngoài
        const r = range(t);
        if(!r) return;
        ab.set(r[0], r[1], true);
        if(!(media.currentTime >= r[0] && media.currentTime < r[1])) try{ media.currentTime = r[0]; }catch(e){ /* chưa tải xong */ }
      };
      const ch = btn("Lặp chương này", "btn-sm", () => ab.chapter(media.currentTime || 0));
      ch.title = "Lặp đi lặp lại chương đang xem";
      ab.els.push(ch);
    }
    ab.els.push(clr, txt);
    return ab;
  }

  /* ---------- thanh audio ---------- */
  function audioBar(bookId, trackIds){
    const book = BOOKS[bookId].book;
    const wrap = h("div", "bk-audio");
    const list = h("div", "bk-tracks");
    const audio = document.createElement("audio");
    audio.controls = true; audio.preload = "metadata";
    const ctl = h("div", "bk-ctl");
    const msgEl = h("p", "bk-msg");
    let blobUrl = null, cur = null;
    const posKey = id => LS + ":audio-pos:" + bookId + ":" + id;

    const back = btn("−5s", "btn-sm", () => { audio.currentTime = Math.max(0, audio.currentTime - 5); });
    const fwd = btn("+5s", "btn-sm", () => { audio.currentTime = audio.currentTime + 5; });
    const speed = h("div", "seg");
    [0.75, 0.85, 1, 1.1, 1.25].forEach(r => {
      const b = h("button", null, r + "×");
      b.type = "button";
      b.setAttribute("aria-pressed", String(r === 1));
      b.onclick = () => {
        audio.playbackRate = r;
        try{ audio.preservesPitch = true; }catch(e){}
        [...speed.children].forEach(x => x.setAttribute("aria-pressed", "false"));
        b.setAttribute("aria-pressed", "true");
      };
      speed.append(b);
    });
    const ab = abLoop(audio);
    ctl.append(back, fwd, speed);
    const abRow = h("div", "bk-ctl bk-abrow");
    abRow.append(...ab.els);
    // lặp cả danh sách: hết track thì mở track sau từ đầu và phát luôn
    const advance = j => pick(trackIds[j], list.children[j], true).then(() => audio.play().catch(() => {}));
    const rep = repeater("audio", trackIds.length, "track", advance);
    rep.attach(audio, () => trackIds.indexOf(cur), ab);
    audio.addEventListener("timeupdate", () => {
      if(cur && Math.floor(audio.currentTime) % 5 === 0){
        try{ localStorage.setItem(posKey(cur), String(audio.currentTime)); }catch(e){}
      }
    });
    audio.addEventListener("error", () => {
      msgEl.className = "bk-msg err";
      msgEl.textContent = "Không phát được track này. Nếu đang dùng bản trên Claude, nhập file audio ở tab Sách → Quản lý file.";
    });

    async function pick(id, btnEl, fromStart){
      [...list.children].forEach(x => x.setAttribute("aria-pressed", "false"));
      btnEl.setAttribute("aria-pressed", "true");
      cur = id; ab.set(null, null);
      msgEl.textContent = ""; msgEl.className = "bk-msg";
      if(blobUrl){ URL.revokeObjectURL(blobUrl); blobUrl = null; }
      const src = await source(bookId, id);
      if(src.blob){ blobUrl = URL.createObjectURL(src.blob); audio.src = blobUrl; } else { audio.src = src.url; }
      const pos = fromStart ? 0 : Number(localStorage.getItem(posKey(id)) || 0);
      audio.addEventListener("loadedmetadata", () => { if(pos > 0 && pos < audio.duration - 2) audio.currentTime = pos; }, {once: true});
      if("mediaSession" in navigator && window.MediaMetadata){
        try{ navigator.mediaSession.metadata = new MediaMetadata({title: id + " · " + book.files[id].title, album: book.title}); }catch(e){}
      }
      const sc = book.files[id].script;
      scriptBtn.hidden = !sc;
    }
    const scriptBtn = btn("Tapescript của track", "btn-sm", () => {
      const sc = cur && book.files[cur].script;
      if(sc) openViewer(bookId, sc, "Tapescript · " + cur);
    });
    scriptBtn.hidden = true;
    trackIds.forEach((id, k) => {
      const f = book.files[id];
      const b = h("button", "btn btn-sm", f ? f.title.replace("Listening ", "") : id);
      b.type = "button";
      b.title = id + (f && f.durationSec ? " · " + BookCore.fmtClock(f.durationSec) : "");
      b.setAttribute("aria-pressed", "false");
      b.onclick = () => pick(id, b);
      list.append(b);
      if(k === 0) setTimeout(() => pick(id, b), 0);
    });
    wrap.append(h("div", "eyebrow", "Audio · " + trackIds.length + " track"), list, audio, ctl, abRow, rep.el, scriptBtn, msgEl);
    return wrap;
  }

  /* ---------- màn hình ---------- */
  function go(name, extra){
    view = Object.assign({name}, extra || {});
    if(tick){ clearInterval(tick); tick = null; }
    render();
    if(msg && name === "book"){ flash(msg); msg = ""; }
    window.scrollTo({top: 0, behavior: "instant"});
  }

  function render(){
    if(!root) return;
    root.textContent = "";
    const ids = Object.keys(BOOKS);
    if(!ids.length){
      root.append(h("h2", "sec-title", "Sách"));
      const c = card();
      c.append(h("p", "small", "Chưa có sách nào. Đặt PDF và audio vào thư mục books/<tên sách>/, viết book.yaml rồi chạy agent: "
        + "python -m book_ingest ingest books/<tên sách> (xem agents/README.md), sau đó chạy lại web/build.py."));
      root.append(c);
      return;
    }
    if(view.name === "session" && view.sessionId && BOOKS[view.bookId]) renderSession();
    else if(view.name === "book" && BOOKS[view.bookId]) renderBook();
    else renderLibrary();
  }

  /* ---------- màn 1: danh sách sách + thông tin lộ trình ---------- */
  const fmtNum = x => String(x).replace(".", ",");
  const fmtMonths = m => "~" + fmtNum(Math.round(m * 2) / 2) + " tháng";

  function kv(box, label, value){
    if(!value) return;
    const row = h("div", "bk-kv");
    row.append(h("span", "bk-k", label), h("span", "bk-v", value));
    box.append(row);
  }

  function levelText(info){
    if(!info) return "";
    const band = info.bandFrom != null && info.bandTo != null
      ? "Band " + Number(info.bandFrom).toFixed(1) + " → " + Number(info.bandTo).toFixed(1) : "";
    return [band, info.cefr ? "CEFR " + info.cefr : ""].filter(Boolean).join(" · ");
  }

  function contentText(book){
    const items = book.sections.flatMap(s => s.items);
    const n = k => items.filter(i => i.kind === k).length;
    const tracks = Object.values(book.files).filter(f => f.kind === "audio").length;
    return book.sections.length + " section · " + n("unit") + " unit · " + n("review") + " review · " + n("test") + " test"
      + (tracks ? " · " + tracks + " track audio" : "");
  }

  function paceText(plan, current){
    const fast = BookCore.duration(plan, 7), slow = BookCore.duration(plan, 5), cur = BookCore.duration(plan, current);
    return "Khoảng " + fmtNum(Math.round(fast.months * 2) / 2) + "–" + fmtNum(Math.round(slow.months * 2) / 2)
      + " tháng (7 đến 5 phiên/tuần). Nhịp đang chọn " + current + " phiên/tuần: " + cur.weeks + " tuần, " + fmtMonths(cur.months) + ".";
  }

  function catalogEntries(){
    const list = ((BOOK_CATALOG && BOOK_CATALOG.books) || []).slice();
    Object.keys(BOOKS).forEach(id => { if(!list.some(e => e.id === id)) list.push({id, title: BOOKS[id].book.title}); });
    return list;
  }

  function renderLibrary(){
    root.append(h("h2", "sec-title", "Sách"));
    root.append(h("p", "sec-note", "Các sách trong lộ trình 40 tuần. Chạm vào một sách để xem toàn bộ section, unit và chọn unit muốn học."));
    catalogEntries().forEach(entry => {
      const data = BOOKS[entry.id];
      const c = card((entry.role || (data && data.book.info && data.book.info.role) || "Sách")
        + (entry.weeks ? " · tuần " + entry.weeks[0] + "–" + entry.weeks[1] : ""));
      c.classList.add("bk-lib");
      c.append(h("h3", "sec-title", entry.title || (data && data.book.title)));
      if(!data){
        c.classList.add("bk-dim");
        if(entry.summary) c.append(h("p", "small", entry.summary));
        const box = h("div", "bk-kvs");
        kv(box, "Mục tiêu", entry.goal);
        c.append(box);
        c.append(h("p", "tiny", "Chưa nhập vào app — đặt PDF và audio vào books/<thư mục sách>/, viết book.yaml rồi chạy agent nhập sách."));
        root.append(c);
        return;
      }
      const {book, plan} = data;
      const info = book.info || {};
      const p = prog(entry.id);
      const st = BookCore.settingsOf(plan, p);
      const cnt = BookCore.counts(plan, p);
      const d = BookCore.duration(plan, st.sessionsPerWeek);
      const meta = [info.module, info.author, info.publisher].filter(Boolean).join(" · ");
      if(meta) c.append(h("p", "small muted", meta));
      const box = h("div", "bk-kvs");
      kv(box, "Trình độ", levelText(info));
      kv(box, "Nội dung", contentText(book));
      kv(box, "Thời lượng", d.sessions + " phiên × " + (plan.minutesPerSession || 75) + " phút ≈ " + d.hours + " giờ");
      kv(box, "Học xong trong", paceText(plan, st.sessionsPerWeek));
      kv(box, "Bắt đầu khi", info.startWhen);
      kv(box, "Mục tiêu", entry.goal);
      c.append(box);
      if(info.summary){
        const more = document.createElement("details");
        const sm = document.createElement("summary"); sm.className = "tiny"; sm.style.cursor = "pointer";
        sm.textContent = "Giới thiệu sách";
        more.append(sm, h("p", "small", info.summary));
        c.append(more);
      }
      const bar = h("div", "bk-bar"); const fill = h("i");
      fill.style.width = (cnt.total ? Math.round((cnt.done + cnt.skipped) / cnt.total * 100) : 0) + "%";
      bar.append(fill);
      c.append(bar, h("p", "tiny", "Đã xong " + cnt.done + "/" + cnt.total + " phiên" + (cnt.minutes ? " · " + fmtNum(Math.round(cnt.minutes / 6) / 10) + " giờ" : "")));
      const row = h("div", "rowx"); row.style.flexWrap = "wrap"; row.style.marginTop = "10px";
      const detail = btn("Xem unit & chọn bài học", "btn-primary btn-sm", () => go("book", {bookId: entry.id}));
      row.append(detail);
      const next = BookCore.nextSession(plan, p);
      if(next) row.append(btn("Học tiếp: " + next.title, "btn-sm", () => go("session", {bookId: entry.id, sessionId: next.id})));
      c.append(row);
      root.append(c);
    });

    const ac = card("Agent nhập sách");
    ac.append(h("p", "small", "Sách ở đây do agent nhập sách (agents/book_ingest) tạo từ PDF và audio. Xem việc đã triển khai và lịch sử thay đổi:"));
    const md = typeof DOCS !== "undefined" ? DOCS["docs/agent-hoc-tap/04-checklist.md"] : "";
    const stats = BookCore.checklistStats(md);
    const phases = Object.keys(stats).sort();
    if(phases.length){
      const all = phases.reduce((a, k) => ({done: a.done + stats[k].done, total: a.total + stats[k].total}), {done: 0, total: 0});
      const sbox = h("div", "bk-kvs");
      kv(sbox, "Đã xong", all.done + "/" + all.total + " task");
      phases.forEach(k => kv(sbox, "Giai đoạn " + k, stats[k].done + "/" + stats[k].total));
      ac.append(sbox);
    }
    const row = h("div", "rowx"); row.style.flexWrap = "wrap"; row.style.marginTop = "10px";
    row.append(btn("Checklist triển khai", "btn-sm", () => openPlanDoc("docs/agent-hoc-tap/04-checklist.md")),
               btn("Lịch sử thay đổi", "btn-sm", () => openPlanDoc("docs/agent-hoc-tap/05-lich-su-thay-doi.md")));
    ac.append(row);
    root.append(ac);
  }

  /* Mở một tài liệu ở tab Kế hoạch (dùng hàm openDoc sẵn có của app). */
  function openPlanDoc(path){
    const nav = document.querySelector('nav button[data-go="docs"]');
    if(nav) nav.click();
    if(typeof openDoc === "function" && typeof DOCS !== "undefined" && DOCS[path]) openDoc(path);
  }

  function sessionRow(bookId, s, isNext){
    const st = BookCore.statusOf(prog(bookId), s.id);
    const row = h("button", "bk-row" + (isNext ? " next" : ""));
    row.type = "button";
    row.onclick = () => go("session", {bookId, sessionId: s.id});
    const dot = h("span", "bk-dot " + st);
    dot.setAttribute("aria-label", STATUS_TXT[st]);
    const t = h("span", "bk-t", s.title.replace(/^(Unit|Review|Test) \d+ · /, ""));
    row.append(dot, t);
    if(s.core) row.append(h("span", "bk-core", "lõi"));
    row.append(h("span", "bk-w", "T" + BookCore.plannedWeek(BOOKS[bookId].plan, prog(bookId), s)));
    return row;
  }

  /* ---------- màn 2: chi tiết sách — mọi section, unit; chọn unit nào học cũng được ---------- */
  function startItem(bookId, itemId){
    const {plan} = BOOKS[bookId];
    setProg(bookId, BookCore.setSettings(prog(bookId), {focus: itemId}, nowMs()));
    const s = BookCore.entrySession(plan, prog(bookId), itemId);
    if(s) go("session", {bookId, sessionId: s.id});
  }

  function itemLabel(item){
    return item.kind === "unit" ? "U" + item.no : (item.kind === "review" ? "R" + item.no : "T" + item.no);
  }

  function unitCard(bookId, item, nextId){
    const {book, plan} = BOOKS[bookId];
    const p = prog(bookId);
    const sess = BookCore.itemSessions(plan, item.id);
    const cnt = BookCore.itemCounts(plan, p, item.id);
    const isNext = sess.some(s => s.id === nextId);
    const box = h("div", "bk-unit" + (isNext ? " now" : cnt.done === cnt.total && cnt.total ? " past" : ""));
    const top = h("div", "bk-unit-top");
    top.append(h("span", "wk-n", itemLabel(item)));
    const mid = h("div", "bk-unit-mid");
    const name = item.kind === "unit" ? "Unit " + item.no + " · " + item.title : item.title;
    mid.append(h("div", "bk-unit-t", name));
    const pr = item.pages ? [BookCore.printedPage(book, "course-book", item.pages[0]), BookCore.printedPage(book, "course-book", item.pages[1])] : null;
    const note = item.kind === "test" && item.activities[0] && item.activities[0].note ? " · chưa có sách Test" : "";
    mid.append(h("div", "tiny", (pr ? "Trang " + pr[0] + "–" + pr[1] + " · " : "") + sess.length + " phiên · đã xong " + cnt.done + "/" + cnt.total + note));
    const dots = h("div", "bk-dots");
    sess.forEach(s => {
      const st = BookCore.statusOf(p, s.id);
      const dd = h("i", "bk-dot " + st);
      dd.title = s.title + " — " + STATUS_TXT[st];
      dots.append(dd);
    });
    mid.append(dots);
    const learn = btn(cnt.done === cnt.total && cnt.total ? "Ôn lại" : (cnt.done ? "Học tiếp" : "Học"), isNext ? "btn-primary btn-sm" : "btn-sm",
      () => startItem(bookId, item.id));
    learn.setAttribute("aria-label", "Học " + name);
    top.append(mid, learn);
    box.append(top);
    const vids = BookCore.lessonsOf(BOOKS[bookId], {item: item.id});
    if(vids.length){
      // mục lục video của unit: mỗi phần (hoạt động) một hàng, ví dụ "Speaking & Vocabulary: Speaking 1 · Speaking 2 · Vocabulary 1–3"
      const vr = h("div", "bk-vids");
      vr.append(h("div", "tiny", "Video bài giảng · " + vids.length));
      const acts = BookCore.activitiesOf(book);
      BookCore.groupLessons(vids, Object.keys(acts)).forEach(g => {
        const row = h("div", "bk-vgroup");
        const a = acts[g.activity];
        row.append(h("span", "bk-vgroup-t", a ? a.title.replace(/^(Unit|Review|Test) \d+ · /, "") : g.activity));
        g.lessons.forEach(l => {
          const s = BookCore.lessonSession(plan, l);
          if(!s) return;
          const b = btn("▶ " + (l.label || l.title) + " · " + BookCore.fmtClock(l.duration), "btn-sm",
            () => go("session", {bookId, sessionId: s.id, lessonId: l.id}));
          b.setAttribute("aria-label", "Xem video " + l.title);
          row.append(b);
        });
        vr.append(row);
      });
      box.append(vr);
    }
    const det = document.createElement("details");
    const sm = document.createElement("summary"); sm.className = "tiny"; sm.style.cursor = "pointer";
    sm.textContent = "Chọn từng phiên";
    det.append(sm);
    if(isNext) det.open = true;
    sess.forEach(s => det.append(sessionRow(bookId, s, s.id === nextId)));
    box.append(det);
    return box;
  }

  function renderBook(){
    const bookId = view.bookId;
    const {book, plan} = BOOKS[bookId];
    const p = prog(bookId);
    const info = book.info || {};
    const c = BookCore.counts(plan, p);
    const focus = BookCore.focusOf(plan, p);
    const next = BookCore.nextSession(plan, p);
    const week = curWeek();
    const finish = BookCore.projectFinishWeek(plan, p, week);
    const st = BookCore.settingsOf(plan, p);
    const items = BookCore.itemsOf(book);

    const top = h("div", "reader-bar");
    top.append(btn("← Danh sách sách", "btn-sm", () => go("library")), h("span", "reader-title", book.title));
    root.append(top);

    const ic = card(info.role || "Sách");
    ic.append(h("h2", "sec-title", book.title));
    const box = h("div", "bk-kvs");
    kv(box, "Trình độ", levelText(info));
    kv(box, "Nội dung", contentText(book));
    kv(box, "Học xong trong", paceText(plan, st.sessionsPerWeek));
    ic.append(box);
    ic.append(h("p", "tiny", "Học theo thứ tự lộ trình, hoặc chọn bất kỳ unit nào bên dưới. Chọn một unit thì \"Phiên kế tiếp\" sẽ đi theo unit đó cho tới khi học xong, rồi tự quay về thứ tự lộ trình."));
    root.append(ic);

    const nc = card(next ? (focus ? "Phiên kế tiếp · unit tự chọn" : "Phiên kế tiếp theo lộ trình") : "Đã xong cả sách");
    nc.classList.add("bk-next");
    if(next){
      nc.append(h("h3", "sec-title", next.title));
      const wk = BookCore.plannedWeek(plan, p, next);
      nc.append(h("p", "small muted", "Tuần dự kiến " + wk + " · bạn đang ở tuần " + week
        + (BookCore.statusOf(p, next.id) === "doing" ? " · đang học dở" : "")));
      const row = h("div", "rowx"); row.style.flexWrap = "wrap"; row.style.marginTop = "12px";
      const go1 = btn("Học phiên này", "btn-primary", () => go("session", {bookId, sessionId: next.id}));
      go1.style.flex = "1";
      row.append(go1);
      if(focus) row.append(btn("Quay về theo lộ trình", "btn-sm", () => {
        setProg(bookId, BookCore.setSettings(prog(bookId), {focus: null}, nowMs()));
        render();
      }));
      nc.append(row);
    } else {
      nc.append(h("p", "small", "Mọi phiên đã xong hoặc bỏ qua. Tiếp tục với đề Cambridge GT theo lộ trình."));
    }
    root.append(nc);

    const pc = card("Tiến độ");
    const stat = h("div", "bk-stat");
    [[c.done + "/" + c.total, "phiên đã xong"], [String(c.total - c.done - c.skipped), "phiên còn lại"],
     [finish ? "T" + finish : "—", "dự kiến xong"]].forEach(([v, l]) => {
      const s = h("div", "stat"); s.append(h("b", null, v), h("span", null, l)); stat.append(s);
    });
    const bar = h("div", "bk-bar"); const fill = h("i");
    fill.style.width = (c.total ? Math.round((c.done + c.skipped) / c.total * 100) : 0) + "%";
    bar.append(fill);
    pc.append(stat, bar);
    const lastWeek = plan.sessions.length ? BookCore.plannedWeek(plan, p, plan.sessions[plan.sessions.length - 1]) : null;
    pc.append(h("p", "tiny", "Theo kế hoạch xong ở tuần " + lastWeek + ". "
      + (finish && finish > 30 ? "Đang chậm quá tuần 30 — cân nhắc học thêm phiên mỗi tuần." :
         finish && lastWeek && finish > lastWeek ? "Đang chậm hơn kế hoạch " + (finish - lastWeek) + " tuần." : "")
      + (c.minutes ? " Đã học " + Math.round(c.minutes / 60 * 10) / 10 + " giờ với sách." : "")));
    root.append(pc);

    root.append(settingsCard(bookId, plan, st));
    root.append(filesCard(bookId));

    root.append(h("h3", "sec-title bk-h", "Chọn unit để học"));
    book.sections.forEach(sec => {
      const head = h("div", "phase-head");
      const secSessions = plan.sessions.filter(s => s.section === sec.id);
      const secDone = secSessions.filter(s => ["done", "skipped"].includes(BookCore.statusOf(p, s.id))).length;
      const units = sec.items.filter(i => i.kind === "unit");
      head.append(h("h3", null, sec.title + (units.length ? " · Unit " + units[0].no + "–" + units[units.length - 1].no : "")),
                  h("span", null, secDone + "/" + secSessions.length + " phiên"));
      root.append(head);
      sec.items.forEach(item => root.append(unitCard(bookId, items[item.id] || item, next && next.id)));
    });
  }

  function settingsCard(bookId, plan, st){
    const c = document.createElement("details");
    c.className = "card";
    const sum = document.createElement("summary");
    sum.className = "eyebrow"; sum.style.cursor = "pointer"; sum.style.marginBottom = "0";
    sum.textContent = "Cài đặt nhịp học · " + st.sessionsPerWeek + " phiên/tuần từ tuần " + st.startWeek;
    c.append(sum);
    const body = h("div"); body.style.marginTop = "12px";
    body.append(h("p", "tiny", "5 phiên/tuần là mức sàn (xong sau khoảng 24 tuần), 6 là mục tiêu (20 tuần), 7 là nhanh (khoảng 17 tuần)."));
    const seg = h("div", "seg"); seg.style.margin = "8px 0 12px";
    [5, 6, 7].forEach(n => {
      const b = h("button", null, n + " phiên/tuần"); b.type = "button";
      b.setAttribute("aria-pressed", String(n === st.sessionsPerWeek));
      b.onclick = () => { setProg(bookId, BookCore.setSettings(prog(bookId), {sessionsPerWeek: n}, nowMs())); render(); };
      seg.append(b);
    });
    const f = h("div", "field");
    const lab = h("label", null, "Bắt đầu học sách từ tuần");
    const inp = document.createElement("input");
    inp.className = "inp num"; inp.type = "number"; inp.min = "1"; inp.max = "40"; inp.value = String(st.startWeek);
    inp.id = "bkStartWeek"; lab.htmlFor = inp.id;
    inp.onchange = () => {
      const v = Math.min(40, Math.max(1, parseInt(inp.value, 10) || plan.startWeek));
      setProg(bookId, BookCore.setSettings(prog(bookId), {startWeek: v}, nowMs()));
      render();
    };
    f.append(lab, inp);
    body.append(seg, f);
    c.append(body);
    return c;
  }

  function filesCard(bookId){
    const {book} = BOOKS[bookId];
    const c = document.createElement("details");
    c.className = "card";
    const sum = document.createElement("summary");
    sum.className = "eyebrow"; sum.style.cursor = "pointer"; sum.style.marginBottom = "0";
    sum.textContent = "Quản lý file sách";
    c.append(sum);
    const body = h("div"); body.style.marginTop = "12px";
    const need = BookCore.requiredPaths(book);
    const info = h("p", "small", "Đang kiểm tra…");
    body.append(h("p", "tiny", "Bản tự host đọc sách thẳng từ thư mục books/" + BOOKS[bookId].dir + "/ trên máy chủ. Bản trên Claude "
      + "hoặc bản chỉ có index.html không có thư mục đó: chọn từ máy các file MP3, file PDF nhỏ và các đoạn PDF trong thư mục web/ "
      + "của sách (" + need.length + " file) để lưu vào trình duyệt này."), info);
    const input = document.createElement("input");
    input.type = "file"; input.multiple = true; input.hidden = true;
    input.accept = ".pdf,.mp3,.m4a,application/pdf,audio/*";
    input.setAttribute("aria-label", "Chọn file PDF và MP3 của sách");
    const out = h("p", "bk-msg");
    input.onchange = async () => {
      const list = [...(input.files || [])];
      const {hit, miss} = BookCore.matchFiles(book, list.map(f => f.name));
      let n = 0;
      for(const f of list){
        const m = hit.find(x => x.name === f.name);
        if(!m) continue;
        out.textContent = "Đang lưu " + f.name + "…";
        try{ await idbPut(bookId + ":" + m.path, f); n++; }
        catch(e){ out.className = "bk-msg err"; out.textContent = "Không lưu được " + f.name + " — trình duyệt hết chỗ hoặc chặn lưu trữ."; return; }
      }
      Object.keys(PDF_CACHE).forEach(k => delete PDF_CACHE[k]);
      out.className = "bk-msg";
      out.textContent = "Đã lưu " + n + " file." + (miss.length ? " Bỏ qua " + miss.length + " file không thuộc sách: " + miss.slice(0, 3).join(", ") + (miss.length > 3 ? "…" : "") : "");
      input.value = "";
      refresh();
    };
    const pick = btn("Nhập file sách từ máy", "btn-primary btn-sm", () => input.click());
    const wipe = btn("Xóa file đã nhập", "btn-sm", async () => {
      if(!confirm("Xóa các file sách đã lưu trong trình duyệt này? Tiến độ học không bị ảnh hưởng.")) return;
      const keys = (await idbKeys()).filter(k => String(k).startsWith(bookId + ":"));
      for(const k of keys) await idbDel(k).catch(() => {});
      Object.keys(PDF_CACHE).forEach(k => delete PDF_CACHE[k]);
      refresh();
    });
    const row = h("div", "rowx"); row.style.marginTop = "10px";
    row.append(pick, wipe);
    body.append(row, input, out);
    c.append(body);
    async function refresh(){
      const keys = new Set((await idbKeys()).map(String));
      const local = need.filter(p => keys.has(bookId + ":" + p)).length;
      let server = false;
      try{
        const r = await fetch(fileUrl(bookId, need[0]), {method: "HEAD"});
        server = r.ok;
      }catch(e){ server = false; }
      info.textContent = "Đã lưu trong trình duyệt: " + local + "/" + need.length + " file. "
        + (server ? "Đọc được từ máy chủ (thư mục books/)." : "Không đọc được từ máy chủ.");
      wipe.hidden = local === 0;
    }
    c.addEventListener("toggle", () => { if(c.open) refresh(); });
    return c;
  }

  function refButtons(bookId, a){
    const box = h("div", "bk-refs");
    const book = BOOKS[bookId].book;
    if(a.pdf && a.pages){
      const pp = a.printedPages || [BookCore.printedPage(book, a.pdf, a.pages[0]), BookCore.printedPage(book, a.pdf, a.pages[1])];
      box.append(btn("Mở trang " + pp[0] + (pp[1] !== pp[0] ? "–" + pp[1] : ""), "btn-primary btn-sm",
        () => openViewer(bookId, {pdf: a.pdf, pages: a.pages}, a.title)));
    }
    (a.alt || []).forEach(r => box.append(btn(r.label || "Bản khác", "btn-sm", () => openViewer(bookId, r, a.title + " · " + (r.label || "")))));
    [["answer", "Đáp án"], ["script", "Tapescript"], ["vocab", "Từ vựng"]].forEach(([k, label]) => {
      if(a[k]) box.append(btn(label, "btn-sm", () => openViewer(bookId, a[k], a.title + " · " + label)));
    });
    return box;
  }

  const MP4 = 'video/mp4; codecs="avc1.64001F, mp4a.40.2"';
  function videoBox(bookId, l, start, rp, i){
    const box = h("div", "bk-video");
    box.id = "lesson-" + l.id;
    box.append(h("div", "bk-vid-t", l.label || l.title));
    if(l.titleVi) box.append(h("div", "tiny", l.titleVi));
    const v = document.createElement("video");
    v.controls = true; v.preload = "metadata"; v.playsInline = true;
    v.setAttribute("data-lesson", l.id);
    v.src = fileUrl(bookId, l.file);
    const out = h("p", "bk-msg");
    const fail = text => { out.className = "bk-msg err"; out.textContent = text; };
    const codecOk = !!v.canPlayType(MP4);
    if(!codecOk) fail("Trình duyệt này không phát được video MP4 (H.264). Mở app bằng Chrome, Edge, Safari hoặc Firefox.");
    v.addEventListener("error", () => {
      if(codecOk) fail("Không tải được video. Bản tự host cần máy chủ thấy thư mục books/ (web/serve.py); bản trên Claude chưa xem được video.");
    });
    const ab = abLoop(v, t => BookCore.chapterRange(l, BookCore.chapterAt(l, t)));
    const chaps = h("div", "bk-chaps");
    const chapBtns = (l.chapters || []).map(c => {
      const b = btn(BookCore.fmtClock(c.t) + " " + c.title, "btn-sm", () => {
        if(ab.byChapter) ab.chapter(c.t);  // đang lặp chương thì chuyển sang lặp chương vừa chọn
        try{ v.currentTime = c.t; v.play().catch(() => {}); }catch(e){ /* chưa tải xong */ }
      });
      chaps.append(b);
      return b;
    });
    const mark = () => {
      const i = BookCore.chapterAt(l, v.currentTime || 0);
      chapBtns.forEach((b, k) => b.setAttribute("aria-pressed", String(k === i)));
    };
    v.addEventListener("timeupdate", () => { VPOS[l.id] = v.currentTime; mark(); });
    v.addEventListener("loadedmetadata", () => { if(VPOS[l.id]) v.currentTime = VPOS[l.id]; });
    mark();
    const loop = h("div", "bk-ctl bk-vloop");
    loop.append(...ab.els);
    if(rp) rp.attach(v, () => i, ab);
    const meta = h("p", "tiny", BookCore.fmtClock(l.duration) + " · " + (l.voices || []).join(" · "));
    box.append(v, chaps, loop, out, meta);
    if(start){  // mở từ nút trên thẻ unit: cuộn tới video và phát một lần (vẽ lại trang thì không tự phát nữa)
      view.lessonId = null;
      setTimeout(() => { box.scrollIntoView({block: "start"}); v.play().catch(() => {}); }, 0);
    }
    return box;
  }

  function renderSession(){
    const bookId = view.bookId;
    const {book, plan} = BOOKS[bookId];
    const s = plan.sessions.find(x => x.id === view.sessionId);
    if(!s){ go("book", {bookId}); return; }
    if(!ACTS[bookId]){ ACTS[bookId] = BookCore.activitiesOf(book); ITEMS[bookId] = BookCore.itemsOf(book); }
    const rec = () => prog(bookId).sessions[s.id] || {};
    const st = BookCore.statusOf(prog(bookId), s.id);
    const item = ITEMS[bookId][s.item];

    const top = h("div", "reader-bar");
    top.append(btn("← Danh sách unit", "btn-sm", () => go("book", {bookId})), h("span", "reader-title", s.title));
    root.append(top);

    const head = card("Tuần dự kiến " + BookCore.plannedWeek(plan, prog(bookId), s) + " · phiên " + s.seq + "/" + plan.sessions.length);
    head.append(h("h2", "sec-title", s.title));
    const sub = h("p", "small muted", (item ? item.title + " · " : "") + "Trạng thái: " + STATUS_TXT[st] + (s.core ? " · phiên lõi" : ""));
    head.append(sub);
    if(s.note) head.append(h("p", "bk-note", s.note));
    root.append(head);

    // Đồng hồ 75 phút tính theo mốc thời gian
    const tc = card("Đồng hồ phiên · " + (s.estMinutes || 75) + " phút");
    const disp = h("div", "timer num", "");
    const lbl = h("div", "timer-lbl", "");
    const toggle = btn("", "btn-primary", () => {
      const r = rec(), now = nowMs();
      if(r.run) update(bookId, s.id, {acc: BookCore.elapsedSec(r, now), run: null});
      else update(bookId, s.id, {run: now, st: r.st === "done" ? "done" : "doing", acc: r.acc || 0});
      paint();
    });
    toggle.style.flex = "1";
    const rowT = h("div", "rowx"); rowT.append(toggle);
    tc.append(disp, lbl, rowT);
    function paint(){
      const r = rec(), el = BookCore.elapsedSec(r, nowMs()), left = (s.estMinutes || 75) * 60 - el;
      disp.textContent = BookCore.fmtClock(left);
      disp.className = "timer num" + (left < 0 ? " over" : (left <= 300 ? " warn" : ""));
      lbl.textContent = left < 0 ? "Đã quá giờ " + BookCore.fmtClock(-left) : "Đã học " + BookCore.fmtClock(el);
      toggle.textContent = r.run ? "Tạm dừng" : (el ? "Học tiếp" : "Bắt đầu phiên");
    }
    paint();
    tick = setInterval(paint, 1000);
    root.append(tc);

    // Hoạt động của phiên
    const ac = card("Hoạt động");
    s.activityIds.forEach(aid => {
      const a = ACTS[bookId][aid];
      if(!a) return;
      const box = h("div", "bk-act");
      box.style.setProperty("--rail", SKILL_RAIL[a.skill] || "var(--line-2)");
      box.append(h("h4", null, a.title));
      if(a.note) box.append(h("p", "bk-note", a.note));
      box.append(refButtons(bookId, a));
      if(a.tracks && a.tracks.length) box.append(audioBar(bookId, a.tracks));
      const vids = BookCore.lessonsOf(BOOKS[bookId], {activity: a.id});
      if(vids.length){
        box.append(h("div", "eyebrow bk-vh", "Video bài giảng · " + vids.length));
        const els = [];
        const rp = repeater("video", vids.length, "video", j => {  // lặp cả danh sách: cuộn tới video sau và phát từ đầu
          const v = els[j] && els[j].querySelector("video");
          if(!v) return;
          VPOS[vids[j].id] = 0;
          try{ v.currentTime = 0; }catch(e){ /* chưa tải xong */ }
          els[j].scrollIntoView({block: "start", behavior: "smooth"});
          v.play().catch(() => {});
        });
        box.append(rp.el);
        vids.forEach((l, i) => { els[i] = videoBox(bookId, l, view.lessonId === l.id, rp, i); box.append(els[i]); });
      }
      ac.append(box);
    });
    if(!s.activityIds.length) ac.append(h("p", "small muted", "Phiên này chưa có tài liệu trong sách."));
    root.append(ac);

    // Ghi lỗi nhanh vào sổ lỗi của app
    const ec = document.createElement("details");
    ec.className = "card";
    const es = document.createElement("summary");
    es.className = "eyebrow"; es.style.cursor = "pointer"; es.style.marginBottom = "0";
    es.textContent = "Ghi lỗi vào sổ lỗi";
    ec.append(es);
    const eb = h("div"); eb.style.marginTop = "12px";
    const mk = (label, id, ph) => {
      const f = h("div", "field"); const l = h("label", null, label); const i = document.createElement("input");
      i.className = "inp"; i.id = id; i.placeholder = ph; l.htmlFor = id; f.append(l, i); eb.append(f); return i;
    };
    const wrong = mk("Câu sai của tôi", "bkErrA", "Câu trả lời hoặc câu viết sai");
    const right = mk("Câu đúng", "bkErrB", "Đáp án hoặc câu đã sửa");
    const why = mk("Vì sao sai", "bkErrN", "Nghe nhầm số, thiếu -s, sai mạo từ…");
    const eo = h("p", "bk-msg");
    eb.append(btn("Thêm vào sổ lỗi", "btn-primary btn-sm", () => {
      const a = wrong.value.trim(), b = right.value.trim();
      if(!a || !b){ eo.textContent = "Nhập cả câu sai và câu đúng."; return; }
      try{
        S.errors.push({d: iso(today()), k: STEP_SKILL[s.step] || "V", a, b,
                       n: (why.value.trim() ? why.value.trim() + " · " : "") + s.title});
        save();
        if(typeof renderProgress === "function") renderProgress();
        wrong.value = right.value = why.value = "";
        eo.textContent = "Đã thêm vào sổ lỗi (tab Tiến độ).";
      }catch(e){ eo.textContent = "Không ghi được sổ lỗi."; }
    }), eo);
    ec.append(eb);
    root.append(ec);

    // Kết thúc phiên
    const fc = card("Kết thúc phiên");
    const el = BookCore.elapsedSec(rec(), nowMs());
    const fm = h("div", "field");
    const ml = h("label", null, "Số phút đã học");
    const mi = document.createElement("input");
    mi.className = "inp num"; mi.type = "number"; mi.min = "0"; mi.max = "300"; mi.id = "bkMin";
    mi.value = String(rec().min || (el ? Math.max(1, Math.round(el / 60)) : (s.estMinutes || 75)));
    ml.htmlFor = mi.id; fm.append(ml, mi);
    const chkWrap = h("label", "small"); chkWrap.style.display = "flex"; chkWrap.style.gap = "8px"; chkWrap.style.alignItems = "center";
    // Đã cộng giờ cho phiên này rồi (kể cả khi bỏ đánh dấu rồi học lại) thì mặc định không cộng nữa.
    const added = Number(rec().added) || 0;
    const chk = document.createElement("input"); chk.type = "checkbox"; chk.checked = !added;
    chkWrap.append(chk, document.createTextNode("Cộng số phút này vào giờ học hôm nay (tab Hôm nay)"
      + (added ? " — phiên này đã cộng " + added + " phút trước đó" : "")));
    const nf = h("div", "field"); nf.style.marginTop = "10px";
    const nl = h("label", null, "Ghi chú");
    const ni = document.createElement("input"); ni.className = "inp"; ni.id = "bkNote"; ni.value = rec().note || "";
    ni.placeholder = "Đúng 7/10 câu, sai dạng điền số…"; nl.htmlFor = ni.id; nf.append(nl, ni);
    const out = h("p", "bk-msg");
    const actions = h("div", "rowx"); actions.style.flexWrap = "wrap"; actions.style.marginTop = "6px";

    function finish(status){
      const r = rec(), now = nowMs();
      const min = Math.max(0, parseInt(mi.value, 10) || 0);
      const patch = {st: status, note: ni.value.trim(), acc: BookCore.elapsedSec(r, now), run: null};
      if(status === "done"){ patch.min = min; patch.d = iso(today()); }
      const addHours = status === "done" && chk.checked && min > 0;
      if(addHours) patch.added = (Number(r.added) || 0) + min;
      update(bookId, s.id, patch);
      if(addHours){
        try{
          const k = iso(today());
          S.hours[k] = Math.round(((Number(S.hours[k]) || 0) + min / 60) * 100) / 100;
          save();
          if(typeof renderAll === "function") renderAll();
        }catch(e){ /* app chưa sẵn sàng thì bỏ qua phần cộng giờ */ }
      }
      if(status === "done" || status === "skipped"){
        const nx = BookCore.nextSession(plan, prog(bookId));
        msg = status === "done" ? "Đã xong: " + s.title + "." + (nx ? " Tiếp theo: " + nx.title + "." : "") : "Đã bỏ qua: " + s.title + ".";
        go("book", {bookId});
      } else {
        out.textContent = "Đã lưu dở. Mở lại phiên này để học tiếp.";
        paint();
      }
    }
    actions.append(btn(st === "done" ? "Lưu lại" : "Hoàn thành phiên", "btn-primary", () => finish("done")));
    if(st !== "done") actions.append(btn("Lưu dở", "btn-sm", () => finish("doing")));
    if(BookCore.canSkip(s) && st !== "skipped") actions.append(btn("Bỏ qua phiên", "btn-sm", () => {
      if(confirm("Bỏ qua phiên này? Chỉ phiên không lõi mới bỏ được.")) finish("skipped");
    }));
    if(st === "done" || st === "skipped") actions.append(btn("Đánh dấu chưa học", "btn-sm", () => {
      update(bookId, s.id, {st: "todo", run: null}); render();
    }));
    fc.append(fm, chkWrap, nf, actions, out);
    root.append(fc);
  }

  /* ---------- khởi động ---------- */
  function show(){
    if(tick){ clearInterval(tick); tick = null; }
    view = {name: "library"};
    render();
    Object.keys(BOOKS).forEach(id => pull(id));
    if(msg){ flash(msg); msg = ""; }
  }
  function flash(text){
    const n = h("p", "bk-msg", text);
    n.setAttribute("role", "status");
    if(root && root.firstChild) root.insertBefore(n, root.children[1] || null);
  }

  function init(){
    root = document.getElementById("p-book");
    if(!root) return;
    const nav = document.querySelector('nav button[data-go="book"]');
    if(nav) nav.addEventListener("click", () => show());
    render();
  }

  return {init, show, render, _core: BookCore};
})();

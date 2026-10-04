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
    const zoomOut = btn("−", "btn-sm", () => { zoom = Math.max(1, zoom - 0.5); draw(); });
    const zoomIn = btn("+", "btn-sm", () => { zoom = Math.min(3, zoom + 0.5); draw(); });
    zoomOut.setAttribute("aria-label", "Thu nhỏ"); zoomIn.setAttribute("aria-label", "Phóng to");
    const close = btn("Đóng", "btn-sm", () => shut());
    bar.append(tt, zoomOut, zoomIn, close);
    const body = h("div", "bk-vbody");
    const canvas = document.createElement("canvas");
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
    let ready = false, page = ref.pages[0], zoom = 1, renderTask = null, drawing = 0;
    const onKey = e => {
      if(e.key === "Escape") shut();
      if(e.key === "ArrowRight") go(1);
      if(e.key === "ArrowLeft") go(-1);
    };
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
    async function draw(){
      const my = ++drawing;
      const inRange = page >= ref.pages[0] && page <= ref.pages[1];
      label.textContent = "Trang " + BookCore.printedPage(book, ref.pdf, page) + " trong sách"
        + (inRange ? " · " + (page - ref.pages[0] + 1) + "/" + (ref.pages[1] - ref.pages[0] + 1) : " · ngoài phần của phiên");
      prev.disabled = page <= 1; next.disabled = page >= total;
      status.textContent = "Đang mở trang…"; status.hidden = false; status.className = "bk-msg";
      let src = null;
      try{
        src = await pdfSource(bookId, ref.pdf, page, inRange ? ref.pages : null);
        const doc = await openPdf(bookId, src);
        ready = true;
        if(my !== drawing) return;
        const p = await doc.getPage(page - src.first + 1);
        const base = p.getViewport({scale: 1});
        const width = Math.max(280, body.clientWidth - 20) * zoom;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        let scale = width / base.width * dpr;
        const maxPx = 16e6;    // trần canvas của Safari iOS
        if(base.width * base.height * scale * scale > maxPx) scale = Math.sqrt(maxPx / (base.width * base.height));
        const vp = p.getViewport({scale});
        canvas.width = Math.floor(vp.width); canvas.height = Math.floor(vp.height);
        canvas.style.width = Math.floor(vp.width / dpr) + "px";
        canvas.style.height = Math.floor(vp.height / dpr) + "px";
        if(renderTask) try{ renderTask.cancel(); }catch(e){}
        renderTask = p.render({canvasContext: canvas.getContext("2d"), viewport: vp});
        await renderTask.promise;
        status.hidden = true;
        body.scrollTop = 0;
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

  /* ---------- thanh audio ---------- */
  function audioBar(bookId, trackIds){
    const book = BOOKS[bookId].book;
    const wrap = h("div", "bk-audio");
    const list = h("div", "bk-tracks");
    const audio = document.createElement("audio");
    audio.controls = true; audio.preload = "metadata";
    const ctl = h("div", "bk-ctl");
    const msgEl = h("p", "bk-msg");
    let blobUrl = null, cur = null, loopA = null, loopB = null;
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
    const loopTxt = h("span", "tiny", "");
    const setA = btn("A", "btn-sm", () => { loopA = audio.currentTime; paintLoop(); });
    const setB = btn("B", "btn-sm", () => { if(loopA != null && audio.currentTime > loopA){ loopB = audio.currentTime; paintLoop(); } });
    const clr = btn("Bỏ lặp", "btn-sm", () => { loopA = loopB = null; paintLoop(); });
    setA.title = "Đặt điểm đầu đoạn lặp"; setB.title = "Đặt điểm cuối đoạn lặp";
    function paintLoop(){
      loopTxt.textContent = loopA == null ? "" : "Lặp " + BookCore.fmtClock(loopA) + (loopB == null ? " → …" : " → " + BookCore.fmtClock(loopB));
    }
    ctl.append(back, fwd, speed, setA, setB, clr, loopTxt);
    audio.addEventListener("timeupdate", () => {
      if(loopA != null && loopB != null && audio.currentTime >= loopB) audio.currentTime = loopA;
      if(cur && Math.floor(audio.currentTime) % 5 === 0){
        try{ localStorage.setItem(posKey(cur), String(audio.currentTime)); }catch(e){}
      }
    });
    audio.addEventListener("error", () => {
      msgEl.className = "bk-msg err";
      msgEl.textContent = "Không phát được track này. Nếu đang dùng bản trên Claude, nhập file audio ở tab Sách → Quản lý file.";
    });

    async function pick(id, btnEl){
      [...list.children].forEach(x => x.setAttribute("aria-pressed", "false"));
      btnEl.setAttribute("aria-pressed", "true");
      cur = id; loopA = loopB = null; paintLoop();
      msgEl.textContent = ""; msgEl.className = "bk-msg";
      if(blobUrl){ URL.revokeObjectURL(blobUrl); blobUrl = null; }
      const src = await source(bookId, id);
      if(src.blob){ blobUrl = URL.createObjectURL(src.blob); audio.src = blobUrl; } else { audio.src = src.url; }
      const pos = Number(localStorage.getItem(posKey(id)) || 0);
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
    wrap.append(h("div", "eyebrow", "Audio · " + trackIds.length + " track"), list, audio, ctl, scriptBtn, msgEl);
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
    if(!view.bookId || !BOOKS[view.bookId]) view.bookId = ids[0];
    if(view.name === "session" && view.sessionId) renderSession();
    else renderBook(ids);
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

  function renderBook(ids){
    const {book, plan} = BOOKS[view.bookId];
    const bookId = view.bookId;
    const p = prog(bookId);
    const c = BookCore.counts(plan, p);
    const next = BookCore.nextSession(plan, p);
    const week = curWeek();
    const finish = BookCore.projectFinishWeek(plan, p, week);
    const st = BookCore.settingsOf(plan, p);

    root.append(h("h2", "sec-title", book.title));
    root.append(h("p", "sec-note", plan.sessions.length + " phiên × " + plan.minutesPerSession + " phút, học theo thứ tự. "
      + "Mỗi unit 7 phiên; phiên có nhãn \"lõi\" (Speaking, Writing, bài Test) không được bỏ qua."));
    if(ids.length > 1){
      const seg = h("div", "seg"); seg.style.marginBottom = "12px";
      ids.forEach(id => {
        const b = h("button", null, BOOKS[id].book.title); b.type = "button";
        b.setAttribute("aria-pressed", String(id === bookId));
        b.onclick = () => go("book", {bookId: id});
        seg.append(b);
      });
      root.append(seg);
    }

    const nc = card(next ? "Phiên kế tiếp" : "Đã xong cả sách");
    nc.classList.add("bk-next");
    if(next){
      nc.append(h("h3", "sec-title", next.title));
      const wk = BookCore.plannedWeek(plan, p, next);
      nc.append(h("p", "small muted", "Tuần dự kiến " + wk + " · bạn đang ở tuần " + week
        + (BookCore.statusOf(p, next.id) === "doing" ? " · đang học dở" : "")));
      const go1 = btn("Học phiên này", "btn-primary", () => go("session", {bookId, sessionId: next.id}));
      go1.style.marginTop = "12px"; go1.style.width = "100%";
      nc.append(go1);
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

    book.sections.forEach(sec => {
      const head = h("div", "phase-head");
      const secSessions = plan.sessions.filter(s => s.section === sec.id);
      const secDone = secSessions.filter(s => ["done", "skipped"].includes(BookCore.statusOf(p, s.id))).length;
      head.append(h("h3", null, sec.title), h("span", null, secDone + "/" + secSessions.length + " phiên"));
      root.append(head);
      sec.items.forEach(item => {
        const sess = secSessions.filter(s => s.item === item.id);
        const done = sess.filter(s => ["done", "skipped"].includes(BookCore.statusOf(p, s.id))).length;
        const det = document.createElement("details");
        det.className = "wk" + (next && next.item === item.id ? " now" : (done === sess.length ? " past" : ""));
        if(next && next.item === item.id) det.open = true;
        const sum = document.createElement("summary");
        sum.className = "wk-btn";
        const label = item.kind === "unit" ? "U" + item.no : (item.kind === "review" ? "R" + item.no : "T" + item.no);
        sum.append(h("span", "wk-n", label),
                   h("span", "wk-t", item.title + " · " + done + "/" + sess.length));
        const body = h("div", "wk-body");
        sess.forEach(s => body.append(sessionRow(bookId, s, next && next.id === s.id)));
        det.append(sum, body);
        root.append(det);
      });
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
    top.append(btn("← Sách", "btn-sm", () => go("book", {bookId})), h("span", "reader-title", s.title));
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
    if(view.name !== "session") view.name = "book";
    render();
    if(view.bookId) pull(view.bookId);
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

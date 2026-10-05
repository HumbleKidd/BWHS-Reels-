(function () {
  const VERSION = "1.3.0";
  const CODE = 4;
  const LANDED = "bwhs-reels-landed";
  if (window.__bwReelsBoot) return;
  window.__bwReelsBoot = true;
  try { localStorage.setItem("bwhs-reels-build", JSON.stringify({ version: VERSION, versionCode: CODE })); } catch (e) {}

  const css = document.createElement("style");
  css.textContent = ".bw-landed{position:fixed;inset:0;z-index:120;display:grid;place-items:end center;padding:18px 16px calc(24px + env(safe-area-inset-bottom));background:radial-gradient(900px 480px at 12% -10%, rgba(255,59,107,.34), transparent 60%),radial-gradient(700px 420px at 100% 0%, rgba(47,128,255,.28), transparent 55%),linear-gradient(180deg, rgba(255,255,255,.28), rgba(243,247,255,.94));overflow:hidden}.bw-landed canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.bw-landed .card{position:relative;width:min(440px,100%);background:rgba(255,255,255,.94);border:1px solid rgba(20,24,43,.08);border-radius:28px;padding:22px 18px 16px;box-shadow:0 24px 60px rgba(47,88,160,.2);text-align:center;color:#14182b}.bw-landed .logo-badge{width:86px;height:86px;border-radius:24px;margin:0 auto 10px;position:relative;overflow:hidden;box-shadow:0 10px 24px rgba(20,24,43,.14);background:#f4f8ff}.bw-landed .logo-badge img{width:100%;height:100%;object-fit:cover;display:block}.bw-landed .logo-badge span{position:absolute;right:6px;bottom:6px;width:28px;height:28px;border-radius:50%;background:#ff2d4e;color:#fff;font-weight:900;display:grid;place-items:center;border:2px solid #fff;font-size:16px}.bw-landed h3{margin:0 0 6px;font-family:Georgia,serif;font-size:2rem;letter-spacing:-.03em}.bw-landed p{margin:0 0 14px;color:#51607f;font-size:14.5px;line-height:1.5}.bw-landed button{width:100%;height:48px;border:0;border-radius:14px;background:#ff3b6b;color:#fff;font-weight:800;font-size:15px}.bw-upd{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:110;background:#fff;color:#14182b;border-radius:22px;padding:14px;box-shadow:0 16px 40px rgba(20,40,80,.2);border:1px solid rgba(20,24,43,.08)}.bw-upd b{display:block;font-size:15px}.bw-upd p{margin:4px 0 10px;color:#5d6b8c;font-size:13px}.bw-upd .bar{height:8px;border-radius:99px;background:#e7efff;overflow:hidden;margin-bottom:10px}.bw-upd .bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ff3b6b,#3b82f6)}.bw-upd .row{display:flex;gap:8px}.bw-upd button{flex:1;height:42px;border:0;border-radius:12px;font-weight:800}.bw-upd .go{background:#ff3b6b;color:#fff}.bw-upd .no{background:#eef3ff;color:#14182b}";
  document.head.appendChild(css);

  function confetti(canvas) {
    const ctx = canvas.getContext("2d");
    const colors = ["#ff3b6b", "#ffb703", "#3b82f6", "#22c55e", "#a855f7", "#ffffff"];
    const bits = Array.from({ length: 150 }, function (_, i) {
      return { x: Math.random() * canvas.clientWidth, y: -20 - Math.random() * 280, w: 6 + Math.random() * 7, h: 8 + Math.random() * 10, vx: -1.6 + Math.random() * 3.2, vy: 2.2 + Math.random() * 3.4, r: Math.random() * 6, vr: -0.2 + Math.random() * 0.4, color: colors[i % colors.length] };
    });
    let frame = 0;
    function tick() {
      if (!canvas.isConnected) return;
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = canvas.clientWidth * dpr;
      canvas.height = canvas.clientHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
      bits.forEach(function (b) {
        b.x += b.vx; b.y += b.vy; b.r += b.vr; b.vy += 0.03;
        ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.r); ctx.fillStyle = b.color; ctx.fillRect(-b.w / 2, -b.h / 2, b.w, b.h); ctx.restore();
      });
      if (++frame < 240) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function showLanded() {
    if (localStorage.getItem(LANDED) === "1" || document.getElementById("bwLanded")) return;
    const wrap = document.createElement("div");
    wrap.className = "bw-landed";
    wrap.id = "bwLanded";
    wrap.innerHTML = '<canvas></canvas><div class="card"><div class="logo-badge"><img alt="BWHS Reels"><span>R</span></div><h3>BWHS Reels just landed \uD83D\uDE0A</h3><p>The app is officially here. Scroll trailers, jump into films and episodes, and when a new build drops you can download and install it from inside the app.</p><button type="button">Enter Reels</button></div>';
    const img = wrap.querySelector("img");
    img.src = "icon-512.png";
    img.onerror = function () { img.onerror = null; img.src = "https://raw.githubusercontent.com/HumbleKidd/BWHS/main/android-chrome-512x512.png"; };
    document.body.appendChild(wrap);
    confetti(wrap.querySelector("canvas"));
    wrap.querySelector("button").onclick = function () {
      localStorage.setItem(LANDED, "1");
      wrap.remove();
    };
  }

  window.__bwUpdatePct = 0;
  window.__bwUpdateProgress = function (p) {
    window.__bwUpdatePct = Math.round(p);
    const bar = document.querySelector("#bwUpd .bar i");
    const btn = document.getElementById("bwUpdGo");
    if (bar) bar.style.width = window.__bwUpdatePct + "%";
    if (btn && window.__bwUpdatePct < 100) btn.textContent = "Downloading " + window.__bwUpdatePct + "%";
    if (btn && window.__bwUpdatePct >= 100) btn.textContent = "Installing...";
  };
  window.__bwUpdateStatus = function (msg) {
    const btn = document.getElementById("bwUpdGo");
    if (btn) btn.textContent = msg;
  };

  function showUpdate(data) {
    if (document.getElementById("bwUpd")) return;
    const sheet = document.createElement("div");
    sheet.className = "bw-upd";
    sheet.id = "bwUpd";
    sheet.innerHTML = '<b></b><p></p><div class="bar"><i></i></div><div class="row"><button class="no" type="button">Later</button><button class="go" id="bwUpdGo" type="button">Download & install</button></div>';
    sheet.querySelector("b").textContent = "New update " + data.version + " is ready";
    sheet.querySelector("p").textContent = data.notes || "Download and install the new BWHS Reels build right now.";
    document.body.appendChild(sheet);
    sheet.querySelector(".no").onclick = function () {
      window.__bwUpdateSnooze = Date.now();
      sheet.remove();
    };
    sheet.querySelector(".go").onclick = function () { startInstall(data); };
  }

  function startInstall(data) {
    if (window.BWUpdater && typeof window.BWUpdater.downloadAndInstall === "function") {
      window.__bwUpdateProgress(1);
      window.BWUpdater.downloadAndInstall(data.apk);
      return;
    }
    const a = document.createElement("a");
    a.href = data.apk;
    a.download = "BWHS-Reels.apk";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.__bwUpdateStatus("APK download started");
  }

  async function check() {
    if (window.__bwUpdateSnooze && Date.now() - window.__bwUpdateSnooze < 1000 * 60 * 60 * 6) return;
    const urls = ["version.json", "https://bwreels.online/version.json", "https://raw.githubusercontent.com/HumbleKidd/BWHS-Reels-/main/version.json"];
    for (const url of urls) {
      try {
        const res = await fetch(url + (url.indexOf("?") >= 0 ? "&" : "?") + "t=" + Date.now(), { cache: "no-store" });
        if (!res.ok) continue;
        const data = await res.json();
        if (Number(data.versionCode || 0) > CODE) { showUpdate(data); return; }
      } catch (e) {}
    }
  }

  function boot() { showLanded(); setTimeout(check, 1400); }
  if (document.body) boot(); else document.addEventListener("DOMContentLoaded", boot);
})();

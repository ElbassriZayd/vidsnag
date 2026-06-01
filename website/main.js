// VidSnag landing — client logic: buttons, modal, supporters wall, donation picker.

const DOWNLOAD_URL = "https://github.com/ElbassriZayd/vidsnag/releases/latest/download/VidSnag.exe";
// Crypto donations: USDT on BNB Smart Chain (BEP20). If this ever changes, update
// it here AND the <code id="usdtAddr"> text AND regenerate assets/usdt-bep20-qr.png.
const USDT_BEP20 = "0xd62212b2CE5f5AEf16A5b79B5e00Fa02AA68fB33";

// Supabase (community message wall). The anon key is public by design; RLS guards the data.
const SUPA_URL = "https://qkdodbsjwnebyglqjgqr.supabase.co";
const SUPA_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrZG9kYnNqd25lYnlnbHFqZ3FyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAyNDA4NTUsImV4cCI6MjA5NTgxNjg1NX0.nKCcYCNPatJM-P1gwqal6IzHJp0JnD9OD_QiK1Pc6IA";
const SUPA_HEAD = { apikey: SUPA_ANON, Authorization: "Bearer " + SUPA_ANON };

// Monthly donations bar. Paste a free BscScan API key (bscscan.com/myapikey) to
// show live on-chain totals; until then the bar shows a friendly CTA.
const BSCSCAN_KEY = "";
const USDT_BSC_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"; // USDT (BEP20), 18 decimals

// Founding supporters (no dollar amounts — hearts only). Real Ko-fi donors will
// later be appended by the backend WITH amounts and mix in among these.
const FOUNDING = [
  "Amine", "pixelfox", "Sara_K", "TheDude", "marwa.dev", "n0vaa", "Yuki",
  "grimm", "leoo", "sunset_rider", "kaydee", "Omar", "vee", "thatguy_42",
  "mina", "brkn", "zerocool", "lulu",
];

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

const HEART = '<svg class="hh" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.6-9.2-9C1.4 8 3 4.8 6.2 4.8c1.9 0 3.1 1.1 3.8 2.2.7-1.1 1.9-2.2 3.8-2.2 3.2 0 4.8 3.2 3.4 6.2C19 15.4 12 20 12 20z"/></svg>';

let donateAmount = null; // chosen tier / custom amount (string) or null

// ---- supporters wall + hero ticker ----
function renderWall() {
  const wall = document.getElementById("wall");
  if (!wall) return;
  wall.innerHTML = FOUNDING.map(n =>
    `<span class="chip">${HEART}${escapeHtml(n)}</span>`).join("");
  const sup = document.getElementById("supCount");
  if (sup) sup.textContent = "#" + (FOUNDING.length + 1);
}

function renderTicker() {
  const track = document.getElementById("tickerTrack");
  if (!track) return;
  const chips = FOUNDING.map(n => `<span class="t-chip">${HEART}${escapeHtml(n)}</span>`).join("");
  track.innerHTML = chips + chips; // duplicate for a seamless loop
}

// ---- USDT (BEP20) donate card ----
let lastFocused = null;
function openDonate(amount) {
  const m = document.getElementById("donateModal");
  if (!m || typeof m.showModal !== "function") return;
  const sub = document.getElementById("donateSub");
  if (sub) sub.innerHTML = amount
    ? `Thank you! Send <b>~$${escapeHtml(String(amount))} of USDT</b> (or any amount) to this address to keep VidSnag free:`
    : `Send any amount of <b>USDT</b> to this address to keep VidSnag free:`;
  lastFocused = document.activeElement;
  m.showModal();
}
function closeDonate() {
  const m = document.getElementById("donateModal");
  if (m && m.open) m.close();
}
function wireDonateModal() {
  const m = document.getElementById("donateModal");
  if (!m) return;
  document.getElementById("donateClose").addEventListener("click", closeDonate);
  m.addEventListener("click", e => { if (e.target === m) closeDonate(); });
  m.addEventListener("close", () => { if (lastFocused && lastFocused.focus) lastFocused.focus(); });
  // copy the address to clipboard
  const copyBtn = document.getElementById("copyAddr");
  if (copyBtn) copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(USDT_BEP20);
      copyBtn.textContent = "Copied!";
      copyBtn.classList.add("ok");
      setTimeout(() => { copyBtn.textContent = "Copy"; copyBtn.classList.remove("ok"); }, 1800);
    } catch (e) {
      // fallback: select the text so the user can copy manually
      const r = document.createRange();
      r.selectNodeContents(document.getElementById("usdtAddr"));
      const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
    }
  });
}

// ---- buttons: real link if a URL exists, else the modal ----
function wireButtons() {
  const dls = document.querySelectorAll("#dl-win, #dl-win2");
  dls.forEach(a => { if (DOWNLOAD_URL) a.setAttribute("href", DOWNLOAD_URL); });
  // sticky button → reveal the inline give widget (no modal, no navigation)
  const fab = document.getElementById("supportFab");
  if (fab) fab.addEventListener("click", () => {
    const give = document.getElementById("give");
    if (give) give.scrollIntoView({ behavior: "smooth", block: "center" });
  });
}

// ---- donation amount picker (tiers + custom) ----
// Each .donate-pick is a self-contained interactive widget (tiers + custom + go).
// Works inline with no modal/navigation; the chosen amount is scoped per widget.
function wireDonation() {
  document.querySelectorAll(".donate-pick").forEach(scope => {
    const tiers = Array.from(scope.querySelectorAll(".tier"));
    const custom = scope.querySelector(".custom-amt-input");
    const label = scope.querySelector(".donate-label");
    const go = scope.querySelector(".donate-go");
    scope._amt = null;
    const setLabel = () => { if (label) label.textContent = scope._amt ? `Chip in $${scope._amt}` : "Chip in"; };
    const select = (amt, fromTier) => {
      scope._amt = amt || null;
      tiers.forEach(t => {
        const on = fromTier === t;
        t.classList.toggle("active", on);
        t.setAttribute("aria-pressed", String(on));
      });
      if (fromTier && custom) custom.value = "";
      setLabel();
    };
    tiers.forEach(t => {
      t.setAttribute("aria-pressed", "false");
      t.addEventListener("click", () => select(t.dataset.amt, t));
    });
    if (custom) custom.addEventListener("input", () => {
      const v = custom.value.replace(/[^\d.]/g, "");
      custom.value = v;
      tiers.forEach(t => { t.classList.remove("active"); t.setAttribute("aria-pressed", "false"); });
      scope._amt = v || null;
      setLabel();
    });
    if (go) go.addEventListener("click", e => {
      e.preventDefault();
      donateAmount = scope._amt;
      openDonate(scope._amt);
    });
  });
}

// ---- sticky nav shadow ----
function wireNav() {
  const nav = document.getElementById("nav");
  if (!nav) return;
  const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

// ---- mobile menu ----
function wireMobileMenu() {
  const btn = document.getElementById("navToggle");
  const menu = document.getElementById("mobileMenu");
  if (!btn || !menu) return;
  const close = () => {
    btn.classList.remove("open"); menu.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  };
  btn.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    btn.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", String(open));
  });
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", close));
  // Esc closes the mobile menu too
  document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
}

// ---- community chat (Supabase), Discord-style ----
const WALL_CROWN = '<svg viewBox="0 0 24 24"><path d="M3 8l4 4 5-7 5 7 4-4-2 11H5z"/><path d="M5 20h14"/></svg>';

function avColor(name) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) % 360;
  return `hsl(${h}, 62%, 56%)`;
}

function renderMsg(m) {
  const sup = !!m.is_supporter;
  const nm = (m.name || "").trim() || "anon";
  const col = sup ? "#C28A12" : avColor(nm);
  const av = sup
    ? `<span class="cmsg-av sup">${WALL_CROWN}</span>`
    : `<span class="cmsg-av" style="background:${col}">${escapeHtml(nm[0].toUpperCase())}</span>`;
  return `<div class="cmsg${sup ? " sup" : ""}">${av}
    <div class="cmsg-b">
      <div class="cmsg-head"><span class="cmsg-name" style="color:${col}">${escapeHtml(nm)}</span>${sup ? '<span class="msg-badge">supporter</span>' : ""}</div>
      <div class="cmsg-text">${escapeHtml(m.body)}</div>
    </div>
  </div>`;
}

async function loadWall() {
  const feed = document.getElementById("wallGrid");
  if (!feed) return;
  try {
    const r = await fetch(
      `${SUPA_URL}/rest/v1/messages?select=name,body,is_supporter&order=created_at.desc&limit=60`,
      { headers: SUPA_HEAD });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const rows = (await r.json()).reverse(); // chronological, newest at the bottom (chat order)
    const wasAtBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 70;
    feed.innerHTML = rows.length
      ? rows.map(renderMsg).join("")
      : `<p class="wall2-empty">No messages yet — be the first to say hi!</p>`;
    if (rows.length && wasAtBottom) feed.scrollTop = feed.scrollHeight;
  } catch (e) {
    feed.innerHTML = `<p class="wall2-empty">Chat will show up here.</p>`;
  }
}
function scrollChatBottom() {
  const feed = document.getElementById("wallGrid");
  if (feed) feed.scrollTop = feed.scrollHeight;
}

async function postWall(e) {
  e.preventDefault();
  const nameEl = document.getElementById("wallName");
  const bodyEl = document.getElementById("wallBody");
  const status = document.getElementById("wallStatus");
  const name = nameEl.value.trim(), body = bodyEl.value.trim();
  if (!name || !body) return;
  const last = +localStorage.getItem("vs_last_post") || 0;
  if (Date.now() - last < 25000) {
    status.textContent = "Easy there — wait a few seconds between messages.";
    return;
  }
  const btn = e.target.querySelector("button[type=submit]");
  btn.disabled = true; status.textContent = "Posting…";
  try {
    const r = await fetch(`${SUPA_URL}/rest/v1/messages`, {
      method: "POST",
      headers: { ...SUPA_HEAD, "Content-Type": "application/json", Prefer: "return=minimal" },
      body: JSON.stringify({ name, body }),
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    localStorage.setItem("vs_last_post", String(Date.now()));
    bodyEl.value = "";
    status.textContent = "Posted! Thank you.";
    setTimeout(() => { status.textContent = ""; }, 3500);
    await loadWall();
    scrollChatBottom();
  } catch (err) {
    status.textContent = "Couldn't post right now — please try again in a moment.";
  } finally {
    btn.disabled = false;
  }
}

function wireWall() {
  const form = document.getElementById("wallForm");
  if (!form) return;
  form.addEventListener("submit", postWall);
  loadWall().then(scrollChatBottom);
  setInterval(loadWall, 20000); // live refresh
}

// ---- monthly donations bar (BscScan) ----
async function loadDonationBar() {
  const el = document.getElementById("dbarText");
  if (!el || !BSCSCAN_KEY) return; // no key yet → keep the default CTA
  try {
    const url = `https://api.bscscan.com/api?module=account&action=tokentx`
      + `&contractaddress=${USDT_BSC_CONTRACT}&address=${USDT_BEP20}`
      + `&page=1&offset=1000&sort=desc&apikey=${BSCSCAN_KEY}`;
    const j = await (await fetch(url)).json();
    if (j.status !== "1" || !Array.isArray(j.result)) return;
    const now = new Date();
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1).getTime() / 1000;
    const incoming = j.result.filter(t =>
      t.to && t.to.toLowerCase() === USDT_BEP20.toLowerCase() && +t.timeStamp >= monthStart);
    const total = incoming.reduce((s, t) => s + Number(t.value) / 1e18, 0);
    const n = incoming.length;
    el.innerHTML = n
      ? `<b>$${total < 100 ? total.toFixed(2) : Math.round(total)}</b> from <b>${n}</b> supporter${n > 1 ? "s" : ""} this month`
      : `Be the first to support VidSnag this month`;
  } catch (e) { /* keep default CTA */ }
}

document.addEventListener("DOMContentLoaded", () => {
  renderWall();
  renderTicker();
  wireDonateModal();
  wireButtons();
  wireDonation();
  wireNav();
  wireMobileMenu();
  wireWall();
  loadDonationBar();
});

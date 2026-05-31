// VidSnag landing — client logic: buttons, modal, supporters wall, donation picker.

// When the real destinations exist, set these and the buttons become real links
// automatically (no other change needed):
//   DOWNLOAD_URL = "https://github.com/<you>/vidsnag/releases/latest";
//   DONATE_URL   = "https://ko-fi.com/<you>";   // amount is appended as ?amount=N
const DOWNLOAD_URL = "https://github.com/ElbassriZayd/vidsnag/releases/latest/download/VidSnag.exe";
const DONATE_URL = null;   // null → show the "opens soon" modal (set to a Ko-fi/PayPal/crypto link to enable)

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

const MODAL_ICONS = {
  download: '<svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M8 11l4 4 4-4"/><path d="M5 17v2a2 2 0 002 2h10a2 2 0 002-2v-2"/></svg>',
  donate: '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.6-9.2-9C1.4 8 3 4.8 6.2 4.8c1.9 0 3.1 1.1 3.8 2.2.7-1.1 1.9-2.2 3.8-2.2 3.2 0 4.8 3.2 3.4 6.2C19 15.4 12 20 12 20z" fill="#fff" stroke="none"/></svg>',
};

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

// ---- coming-soon modal ----
let lastFocused = null;
function openModal(kind) {
  const m = document.getElementById("soonModal");
  if (!m || typeof m.showModal !== "function") return;
  const ico = document.getElementById("soonIco");
  const title = document.getElementById("soonTitle");
  const body = document.getElementById("soonBody");
  if (kind === "download") {
    ico.innerHTML = MODAL_ICONS.download;
    title.textContent = "Almost ready!";
    body.textContent = "The Windows build drops very soon. Bookmark this page and you can grab it the moment it lands.";
  } else {
    ico.innerHTML = MODAL_ICONS.donate;
    title.textContent = "Donations open soon";
    body.textContent = donateAmount
      ? `Thank you for wanting to chip in $${donateAmount}! Tipping goes live in a few days, and your name joins the wall then.`
      : "Thank you! Tipping goes live in a few days, and your name joins the supporters wall then.";
  }
  lastFocused = document.activeElement;
  m.showModal();
}
function closeModal() {
  const m = document.getElementById("soonModal");
  if (m && m.open) m.close();
}
function wireModal() {
  const m = document.getElementById("soonModal");
  if (!m) return;
  document.getElementById("soonClose").addEventListener("click", closeModal);
  document.getElementById("soonOk").addEventListener("click", closeModal);
  // click on the backdrop (outside the card) closes
  m.addEventListener("click", e => { if (e.target === m) closeModal(); });
  // restore focus to the trigger when the dialog closes (keyboard hygiene)
  m.addEventListener("close", () => { if (lastFocused && lastFocused.focus) lastFocused.focus(); });
}

// ---- buttons: real link if a URL exists, else the modal ----
function wireButtons() {
  const dls = document.querySelectorAll("#dl-win, #dl-win2");
  dls.forEach(a => {
    if (DOWNLOAD_URL) { a.setAttribute("href", DOWNLOAD_URL); return; }
    a.setAttribute("href", "#download");
    a.addEventListener("click", e => { e.preventDefault(); openModal("download"); });
  });
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
      if (DONATE_URL) {
        window.location.href = DONATE_URL + (scope._amt ? `?amount=${encodeURIComponent(scope._amt)}` : "");
        return;
      }
      e.preventDefault();
      donateAmount = scope._amt;
      openModal("donate");
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

document.addEventListener("DOMContentLoaded", () => {
  renderWall();
  renderTicker();
  wireModal();
  wireButtons();
  wireDonation();
  wireNav();
  wireMobileMenu();
});

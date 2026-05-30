// VidSnag landing — light client logic: links, sticky nav, count-up, supporters wall.

const DOWNLOAD_URL = "#"; // TODO: point to the released .exe (GitHub Releases)
const DONATE_URL = "#";   // TODO: point to the Ko-fi page

// Founding supporters (no dollar amounts — hearts only). Real Ko-fi donors will
// later be appended by the backend WITH amounts and mix in above/among these.
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

function renderWall() {
  const wall = document.getElementById("wall");
  if (!wall) return;
  wall.innerHTML = FOUNDING.map(n =>
    `<span class="chip">${HEART}${escapeHtml(n)}</span>`
  ).join("");
  const sup = document.getElementById("supCount");
  if (sup) sup.textContent = "#" + (FOUNDING.length + 1);
}

// Hero ticker: scroll supporter nicknames so the community is visible up top.
function renderTicker() {
  const track = document.getElementById("tickerTrack");
  if (!track) return;
  const chips = FOUNDING.map(n => `<span class="t-chip">${HEART}${escapeHtml(n)}</span>`).join("");
  track.innerHTML = chips + chips; // duplicate for seamless loop
}

// Donation: tiers are suggestions, custom amount is free choice. Build the Ko-fi
// link from whatever the user picked (no forced price).
function wireDonation() {
  const tiers = Array.from(document.querySelectorAll(".tier"));
  const custom = document.getElementById("customAmt");
  const label = document.getElementById("donateLabel");
  let amount = null;

  const setLabel = () => {
    if (label) label.textContent = amount ? `Chip in $${amount}` : "Chip in";
  };
  const select = (amt, fromTier) => {
    amount = amt;
    tiers.forEach(t => t.classList.toggle("active", fromTier === t));
    if (fromTier && custom) custom.value = "";
    setLabel();
  };

  tiers.forEach(t => t.addEventListener("click", () => select(t.dataset.amt, t)));
  if (custom) custom.addEventListener("input", () => {
    const v = custom.value.replace(/[^\d.]/g, "");
    custom.value = v;
    tiers.forEach(t => t.classList.remove("active"));
    amount = v ? v : null;
    setLabel();
  });
}

function wireLinks() {
  document.querySelectorAll("#dl-win, #dl-win2").forEach(a => a.setAttribute("href", DOWNLOAD_URL));
  const donate = document.getElementById("donate");
  if (donate) donate.setAttribute("href", DONATE_URL);
}

// sticky nav shadow on scroll
function wireNav() {
  const nav = document.getElementById("nav");
  if (!nav) return;
  const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

// count-up when the trust number scrolls into view
function wireCountUp() {
  const el = document.getElementById("userCount");
  if (!el) return;
  const target = parseInt(el.textContent, 10) || 0;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) { el.textContent = target; return; }
  let done = false;
  const run = () => {
    if (done) return; done = true;
    const dur = 1100, t0 = performance.now();
    const tick = now => {
      const p = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && run()), { threshold: .6 });
  io.observe(el);
}

document.addEventListener("DOMContentLoaded", () => {
  wireLinks();
  renderWall();
  renderTicker();
  wireDonation();
  wireNav();
  wireCountUp();
});

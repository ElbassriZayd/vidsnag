// VidSnag landing — light client logic.
// Supporters wall: for now renders from a static list; later this fetches
// from the backend (Supabase) populated by the Ko-fi donation webhook.

const DOWNLOAD_URL = "#"; // TODO: point to the released .exe (e.g. GitHub Releases)
const DONATE_URL = "#";   // TODO: point to the Ko-fi page

// Placeholder supporters until the backend is wired.
// Shape matches the future API: { nickname, amount, currency }
const SUPPORTERS = [];

function renderWall(list) {
  const wall = document.getElementById("wall");
  if (!wall) return;
  if (!list.length) return; // keep the "be the first" empty state
  wall.innerHTML = list
    .map(
      (s) =>
        `<span class="chip">${escapeHtml(s.nickname)}<span class="amt">$${Number(
          s.amount
        ).toFixed(0)}</span></span>`
    )
    .join("");
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function wireLinks() {
  const dl = document.getElementById("dl-win");
  if (dl) dl.setAttribute("href", DOWNLOAD_URL);
  const donate = document.getElementById("donate");
  if (donate) donate.setAttribute("href", DONATE_URL);
}

document.addEventListener("DOMContentLoaded", () => {
  wireLinks();
  renderWall(SUPPORTERS);
});

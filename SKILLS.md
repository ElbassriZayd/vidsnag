# Skills Used

## Video download engine
- Source: yt-dlp (PyPI) — already used in telecharger.py
- Type: library
- Why chosen: de-facto standard; handles YouTube + many sites, quality selection, ffmpeg merge
- Adapted: existing telecharger.py to be refactored into engine.py
- Date added: 2026-05-29

## Desktop packaging — PyInstaller (ADOPTED 2026-05-30)
- Source: PyInstaller 6.20, onefile. `vidsnag.spec` + `vidsnag_main.py` entry.
- Bundles ffmpeg.exe+ffprobe.exe (binaries=[...,'.']) + app/web datas; engine.py
  finds them via `sys._MEIPASS`; desktop.py resolves web/+icon frozen-aware.
- `version.txt` (VSVersionInfo) embeds publisher metadata → fewer AV false-positives.
- Spec reads `FFMPEG_DIR` env (CI) with local winget fallback. Output ~189MB.
- Date added: 2026-05-30

## CI build — GitHub Actions (ADOPTED, public repo)
- `.github/workflows/build.yml` on the public repo: Windows runner, downloads slim
  essentials ffmpeg, builds the exe, attaches to release on tag. Reproducible build =
  trust signal. SignPath signing step pre-wired (commented until approval).

## Distribution + trust (ADOPTED 2026-05-30)
- Public repo github.com/ElbassriZayd/vidsnag (MIT) — source auditable; binary on Releases.
- SHA-256 published in release notes. VirusTotal verified (Playwright headed-msedge anon
  upload): 1/69 (Bkav false-positive only), badged on site FAQ.
- SmartScreen "not commonly downloaded" = reputation, only signing removes it.
  SignPath Foundation = FREE OSS signing (PLANNED, needs traction); EV cert = paid instant.

## Coming-soon modal — native <dialog> (ADOPTED)
- main.js opens a native `<dialog>` (focus trap + Esc free) for Download/Donate until
  DOWNLOAD_URL/DONATE_URL are set; set the const → buttons become real links (one-liner).

## Desktop GUI shell — pywebview + WebView2 (ADOPTED)
- Renders the HTML/CSS UI in a native window via Windows' built-in WebView2 (no Chromium bundle).
- Window icon set via pywin32 WM_SETICON + ctypes AppUserModelID (webview.start(icon=) is ignored by WebView2 backend).
- Date added: 2026-05-30

## Logo background removal — saturation matte (ADOPTED)
- scripts/cut_logo.py: cut the VS logo off a navy GRADIENT bg using saturation (max-min channel), not color-distance (single-corner sampling fails on gradients). Exports transparent PNG set + .ico.
- Date added: 2026-05-30

## Website — plain static HTML/CSS/JS on Vercel (ADOPTED, replaced planned React)
- No framework/build; faster, cheaper, handles traffic on CDN. RELATIVE asset paths (absolute broke file://).
- Conversion landing built with marketing-psychology + copywriting + editorial-web-moves skills.
- SEO: SoftwareApplication + FAQPage JSON-LD, OG, canonical, llms.txt, robots, sitemap.
- 2026-05-30 REDESIGN (product-led): decoded category refs (Screen Studio + cobalt.tools,
  NOT manzili's look) → app-window-on-glow hero + paste-teaser + single CTA + ONE dark
  donation band. ui-ux-pro-max a11y pass: native <dialog> modal, focus-visible rings,
  WCAG-AA text contrast, 44px touch targets, aria-pressed tiers.
- Date added: 2026-05-30

## Donations + supporters wall (planned)
- Ko-fi (USD) + Payoneer US-bank route + crypto/BTCPay (Morocco payout).
- Supabase (supporters table) + Ko-fi webhook → real donors append with $ amounts.
- Pay-what-you-want; founding-supporter seeds are nicknames+hearts only (no fake $).
- Date added: 2026-05-29 (planned)

## NOTE on 21st.dev Magic MCP
- Added to user config; npx cache had to be cleared (corrupted is-inside-container). Boots clean but needs a Claude Code RESTART to connect. Not used yet — all UI hand-built.

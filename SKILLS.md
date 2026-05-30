# Skills Used

## Video download engine
- Source: yt-dlp (PyPI) — already used in telecharger.py
- Type: library
- Why chosen: de-facto standard; handles YouTube + many sites, quality selection, ffmpeg merge
- Adapted: existing telecharger.py to be refactored into engine.py
- Date added: 2026-05-29

## Desktop packaging (planned)
- Source: PyInstaller
- Type: tool
- Why chosen: bundle Python + yt-dlp + ffmpeg into a single Windows .exe
- Date added: 2026-05-29 (planned)

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
- Date added: 2026-05-30

## Donations + supporters wall (planned)
- Ko-fi (USD) + Payoneer US-bank route + crypto/BTCPay (Morocco payout).
- Supabase (supporters table) + Ko-fi webhook → real donors append with $ amounts.
- Pay-what-you-want; founding-supporter seeds are nicknames+hearts only (no fake $).
- Date added: 2026-05-29 (planned)

## NOTE on 21st.dev Magic MCP
- Added to user config; npx cache had to be cleared (corrupted is-inside-container). Boots clean but needs a Claude Code RESTART to connect. Not used yet — all UI hand-built.

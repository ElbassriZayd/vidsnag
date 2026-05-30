# VidSnag Roadmap

## Phase 0 — Unblock + scaffold ✅ DONE
- Disk freed, scaffold + git init + first commit.

## Phase 1 — Desktop app MVP ✅ DONE (except .exe packaging)
- engine.py (yt-dlp wrapper), WebView2/pywebview HTML UI, custom dropdown,
  folder picker, real logo + window icon, playful theme. Engine VERIFIED.
- REMAINING: package to a single `.exe` (PyInstaller, bundle yt-dlp + ffmpeg) — disk tight.

## Phase 2 — Landing page ✅ DONE (built), pending DNS
- Plain HTML/CSS/JS conversion landing (NOT React) on Vercel free CDN.
- Live at https://vidsnag-ten.vercel.app. NEXT: Porkbun DNS A @→76.76.21.21
  to point vidsnag.xyz; keep Porkbun nameservers. Then GSC submit.
- Wire Download→GitHub Releases .exe + donate/tiers→Ko-fi once those exist. + sitemap

## Phase 3 — Donations
- Open Payoneer (get US bank details); set up Ko-fi (USD)
- Add BTCPay/crypto (USDT/BTC) on the VPS as the universal fallback

## Phase 4 — Supporters wall
- Supabase table (nickname, amount, is_approved) + Ko-fi webhook → store donors
- Wall component on the site (and optionally in the app) + nickname moderation

## Phase 5 — Polish + launch
- App auto-update check
- Distribute via Reddit / YouTube / forums (not reliant on Google ranking)

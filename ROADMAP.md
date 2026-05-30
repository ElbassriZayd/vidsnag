# VidSnag Roadmap

## Phase 0 — Unblock + scaffold (current)
- Free disk space, set pagefile auto-managed, reboot
- Rewrite 0-byte README, create PROJECT_STATE/ROADMAP/SKILLS/ERRORS
- git init + first commit

## Phase 1 — Desktop app MVP (core product)
- Refactor `telecharger.py` → clean `engine.py` (yt-dlp logic)
- GUI: paste-URL box, quality picker (4K→480p + MP3), download button, progress bar
- Package to a Windows `.exe` with PyInstaller (bundle yt-dlp + ffmpeg)

## Phase 2 — Landing page
- React/Vite site on Vercel, point vidsnag.xyz at it
- Download buttons + how-it-works + supporters-wall slot
- Submit to Google Search Console + sitemap

## Phase 3 — Donations
- Open Payoneer (get US bank details); set up Ko-fi (USD)
- Add BTCPay/crypto (USDT/BTC) on the VPS as the universal fallback

## Phase 4 — Supporters wall
- Supabase table (nickname, amount, is_approved) + Ko-fi webhook → store donors
- Wall component on the site (and optionally in the app) + nickname moderation

## Phase 5 — Polish + launch
- App auto-update check
- Distribute via Reddit / YouTube / forums (not reliant on Google ranking)

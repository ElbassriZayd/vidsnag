# Project State

Last updated: 2026-05-29

---

## Current milestone
Phase 2 — website (landing page + supporters wall). Phase 1 desktop app DONE.

## Completed
- 2026-05-29 Product decided: VidSnag, free desktop video downloader, donation-funded
- 2026-05-29 Architecture locked: desktop app (download runs on user's PC → ban-resistant)
- 2026-05-29 Monetization: donations (not subscription) + public supporters wall
- 2026-05-29 Domain bought: vidsnag.xyz (Porkbun, Order 10504822, $2.04, renewal $12.98)
- 2026-05-29 Engine confirmed: telecharger.py (yt-dlp, quality tiers 4K→480p + MP3)
- 2026-05-29 Scaffold files created (.gitignore, README, PROJECT_STATE, ROADMAP, SKILLS, ERRORS)
- 2026-05-29 Phase 1 built: app/engine.py + app/gui.py (Tkinter). Engine VERIFIED (probe + MP3 download work end-to-end). git initialised + first commit.
- 2026-05-30 Phase 1 UPGRADED: switched UI to premium WebView2 (pywebview) HTML/CSS shell (app/web/index.html + app/desktop.py). Native folder picker, thumbnail/title/channel/duration preview, animated progress. Real download VERIFIED by user. Commit 9211692.

## In progress
- Phase 2 website: starting the landing page (reuses app/web/index.html design language).

## Next steps (in order)
1. Build website/ landing page (hero + download CTA + how-it-works + supporters wall slot)
2. Deploy to Vercel, point vidsnag.xyz, submit to Google Search Console
3. Package the desktop app to a single .exe (PyInstaller, bundle yt-dlp + ffmpeg) — needs more disk
4. Donations (Payoneer + Ko-fi + crypto) and supporters wall backend (Supabase + webhook)

## Blocked / waiting
- C: drive 100% full (<50 MB free) → file writes corrupt to 0 bytes. Must free space.

## Decisions made
- 2026-05-29 Desktop app over web service (ban-resistance + clean payments)
- 2026-05-29 Donations via Ko-fi + Payoneer US-bank route + crypto/BTCPay (Morocco payout)
- 2026-05-29 vidsnag.xyz on a SEPARATE registrar account from caftanfes (no contamination)

## Architecture notes
- app/     : Python + yt-dlp + GUI, packaged to a Windows .exe
- website/ : React/Vite on Vercel + Supabase + Ko-fi webhook (supporters wall)

## Files map
- telecharger.py : working yt-dlp CLI (engine source)
- liens.txt      : URL list (CLI input)
- videos/        : output (git-ignored)
- env_video/     : Python venv (git-ignored)
- app/           : desktop app (to build)
- website/       : landing page + supporters wall (to build)

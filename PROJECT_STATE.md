# Project State

Last updated: 2026-05-29

---

## Current milestone
Phase 1 — desktop app MVP (engine + Tkinter GUI). Engine working; next is .exe packaging.

## Completed
- 2026-05-29 Product decided: VidSnag, free desktop video downloader, donation-funded
- 2026-05-29 Architecture locked: desktop app (download runs on user's PC → ban-resistant)
- 2026-05-29 Monetization: donations (not subscription) + public supporters wall
- 2026-05-29 Domain bought: vidsnag.xyz (Porkbun, Order 10504822, $2.04, renewal $12.98)
- 2026-05-29 Engine confirmed: telecharger.py (yt-dlp, quality tiers 4K→480p + MP3)
- 2026-05-29 Scaffold files created (.gitignore, README, PROJECT_STATE, ROADMAP, SKILLS, ERRORS)
- 2026-05-29 Phase 1 built: app/engine.py + app/gui.py (Tkinter). Engine VERIFIED (probe + MP3 download work end-to-end). git initialised + first commit.

## In progress
- Phase 1 desktop app: engine + GUI built; engine verified (probe + MP3 OK). GUI not yet smoke-tested with a display. PyInstaller .exe packaging deferred (needs more disk).

## Next steps (in order)
1. Smoke-test the GUI window: `./env_video/Scripts/python.exe -m app.gui`
2. Free real disk space (C: still 238G/239G full) so PyInstaller can build the .exe
3. Package to a single .exe (PyInstaller, bundle yt-dlp + ffmpeg)
4. Phase 2: landing page on Vercel + point vidsnag.xyz

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

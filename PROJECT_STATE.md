# Project State

Last updated: 2026-05-30

---

## Current milestone
Phase 2 — website BUILT + polished (conversion landing). Next: DNS to take vidsnag.xyz live.

## Completed
- 2026-05-29 Product decided: VidSnag, free desktop video downloader, donation-funded
- 2026-05-29 Architecture locked: desktop app (download runs on user's PC → ban-resistant)
- 2026-05-29 Monetization: donations (not subscription) + public supporters wall
- 2026-05-29 Domain bought: vidsnag.xyz (Porkbun, Order 10504822, $2.04, renewal $12.98)
- 2026-05-29 Engine confirmed: telecharger.py (yt-dlp, quality tiers 4K→480p + MP3)
- 2026-05-29 Scaffold files created (.gitignore, README, PROJECT_STATE, ROADMAP, SKILLS, ERRORS)
- 2026-05-29 Phase 1 built: app/engine.py + app/gui.py (Tkinter). Engine VERIFIED (probe + MP3 download work end-to-end). git initialised + first commit.
- 2026-05-30 Phase 1 UPGRADED: premium WebView2 (pywebview) HTML/CSS shell (app/web/index.html + app/desktop.py). Native folder picker, thumbnail/title/channel/duration preview, animated progress. Real download VERIFIED by user.
- 2026-05-30 App polished: PLAYFUL redesign (warm cream, Baloo 2 + Nunito, custom dropdown), real VS logo cut from navy bg (scripts/cut_logo.py saturation matte) + window/taskbar icon via pywin32 WM_SETICON + AppUserModelID, window opens 560x720 top-aligned+scroll (no header clip).
- 2026-05-30 Phase 2 website BUILT: full conversion landing (marketing-psychology + copywriting + editorial-web-moves + SEO). Hero (enemy-framed headline "without the sketchy sites" + Chip-in btn + count-up trust), supporters TICKER bar under hero, pain strip, how-it-works, app demo in window frame (realistic thumb), 6 feature cards (SVG icons), supported-sites marquee, supporters WALL (18 founding supporters, hearts not fake $, "be #19"), community DONATION block (suggested tiers + pay-what-you-want custom amount, no forced price), FAQ accordion, final CTA, footer ghost wordmark.
- 2026-05-30 All emojis/glyphs replaced with crafted inline SVGs (project rule). SEO: SoftwareApplication + FAQPage JSON-LD, OG tags, canonical, llms.txt.
- 2026-05-30 Pre-launch fixes: mobile hamburger menu, mobile headline 25px, marquee+ticker overflow contained (verified clientWidth==scrollWidth, no horizontal overflow).
- 2026-05-30 Deploy decision: VERCEL (not the CaféOS/mail VPS — contamination risk to email reputation). Static landing on Vercel free CDN; .exe will go on GitHub Releases. Vercel project "vidsnag" exists; prod alias https://vidsnag-ten.vercel.app is LIVE (200). vidsnag.xyz added to project but NOT pointed yet.

- 2026-05-30 Landing REDESIGN (product-led pass): hand-built page read "generic template" (empty hero, app screenshot buried, single cream rhythm all the way down, no contrast). Fixed via the manzili METHOD (decode category references, not manzili's look): decoded Screen Studio (product-window-on-glow-stage hero) + cobalt.tools (paste-box-as-hero). Rebuilt hero = big app window on warm purple→mint→peach gradient-glow stage + fake "paste a link" teaser pill (4K·1080p·MP3 chips + Get) + ONE primary CTA (demoted "Chip in" to ghost link) + bigger headline (mobile 25→33px, fixed br-collision). Turned donation block into the page's one DARK contrast band. Retired the now-duplicate "See it in action" demo section (hero does that job). Verified local: no horizontal overflow desktop+mobile, screenshots reviewed. NOT yet deployed (live Vercel still old build).

- 2026-05-30 Landing redesign SHIPPED: committed on branch `feat/landing-redesign` + `vercel --prod`. LIVE + verified on https://vidsnag-ten.vercel.app (new-build marker confirmed). vidsnag.xyz still HTTP 000 (DNS not pointed — unchanged user-side step).

- 2026-05-30 UX/UI pass (ui-ux-pro-max): all 3 dead "#" buttons now functional via an accessible native `<dialog>` "coming-soon" modal (Download → "Almost ready!", Donate → amount-aware "opens soon"). FUTURE-PROOFED: set DOWNLOAD_URL / DONATE_URL consts in main.js and buttons auto-become real links (Ko-fi gets ?amount=N). a11y: focus-visible rings everywhere, body text contrast darkened to WCAG AA (--muted #8A8398→#645D77, --faint→#736C86), nav-toggle 44px touch target, tiers aria-pressed, decorative stars aria-hidden, Esc closes modal+menu, focus restored to trigger on close. Verified via Playwright: modal open/close/Esc, amount-aware copy, zero console errors, no overflow desktop+mobile.

- 2026-05-30 DOWNLOAD now REAL: packaged the desktop app to a single Windows .exe. PyInstaller 6.20 onefile (vidsnag.spec + vidsnag_main.py entry), bundles ffmpeg.exe+ffprobe.exe (Gyan 8.1, ~446MB src) + yt_dlp; final VidSnag.exe = 189MB. engine.py picks bundled ffmpeg via sys._MEIPASS; desktop.py resolves web/ + icon frozen-aware. Smoke-tested: exe launches, WebView2 window opens, no crash. Published PUBLIC repo github.com/ElbassriZayd/vidsnag (README + binary ONLY, no source/business docs) + release v0.1.0. Stable URL https://github.com/ElbassriZayd/vidsnag/releases/latest/download/VidSnag.exe returns 200. main.js DOWNLOAD_URL set → both Download buttons now real downloads. Hero copy "tiny download"→"Windows 10 & 11" (189MB isn't tiny). Disk survived: 3.0→2.6GB.

## In progress
- DOWNLOAD live. DONATE still pending USER input: user has Binance + PayPal; advised lead with Binance USDT (privacy + Morocco payout), PayPal only as Business acct (name exposure + downloader-freeze risk). Need the actual USDT address(+network)/PayPal.me handle to set DONATE_URL (one-liner). Branch `feat/landing-redesign` not merged. DNS at Porkbun still pending to take vidsnag.xyz live.
- TODO later: code-sign the .exe (SmartScreen warns unsigned); slim ffmpeg to essentials build to shrink .exe.

## Next steps (in order)
1. DNS at Porkbun: A record @ -> 76.76.21.21 (+ optional CNAME www -> cname.vercel-dns.com). Keep Porkbun as DNS host, do NOT switch nameservers. Then verify HTTPS + submit to Google Search Console.
2. Wire real links: Download btn -> .exe (GitHub Releases), donate/tiers -> Ko-fi (needs Payoneer first).
3. Package desktop app to single .exe (PyInstaller, bundle yt-dlp + ffmpeg) — disk tight (~3.4 GB free).
4. Donations (Payoneer US-bank route + Ko-fi + crypto) + supporters-wall backend (Supabase + Ko-fi webhook) so real donors append with $ amounts.

## Blocked / waiting
- DNS step is user-side (no Porkbun API creds saved; needs dashboard login).
- 21st.dev Magic MCP added to user config + cache-fixed (boots clean) but shows "Failed to connect" until Claude Code RESTART. Only Figma MCP active this session. All UI built by hand with design/marketing skills.
- Disk at ~3.4 GB free — will gate the PyInstaller .exe build.

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

# VidSnag Roadmap

## Phase 0 — Unblock + scaffold ✅ DONE
- Disk freed, scaffold + git init + first commit.

## Phase 1 — Desktop app MVP ✅ DONE (packaged + released)
- engine.py (yt-dlp wrapper), WebView2/pywebview HTML UI, custom dropdown,
  folder picker, real logo + window icon, playful theme. Engine VERIFIED.
- ✅ Packaged to a single `VidSnag.exe` (PyInstaller onefile, bundles ffmpeg+ffprobe,
  189MB) + version metadata. Smoke-tested. Published release v0.1.0 at
  github.com/ElbassriZayd/vidsnag.

## Phase 2 — Landing page ✅ DONE (redesigned), pending DNS
- Plain HTML/CSS/JS landing (NOT React) on Vercel. REDESIGNED product-led
  (app-window-on-glow hero + paste-teaser + dark donation band), full a11y pass,
  Download wired to the real .exe.
- Live at https://vidsnag-ten.vercel.app. NEXT: Porkbun DNS A @→76.76.21.21
  to point vidsnag.xyz; keep Porkbun nameservers. Then GSC submit. + sitemap.

## Phase 3 — Donations 🔄 IN PROGRESS (blocked on user)
- Donate buttons live but show a "coming soon" modal until DONATE_URL is set.
- User has Binance + PayPal. Plan: lead with Binance USDT (privacy + Morocco payout),
  PayPal only as Business acct. NEED: the actual USDT address(+network)/PayPal.me
  handle → one-line wire (crypto card w/ copy + QR, or amount carry-through).
- (Legacy plan kept: Payoneer US-bank + Ko-fi + BTCPay as alternates.)

## Phase 4 — Supporters wall
- Supabase table (nickname, amount, is_approved) + Ko-fi webhook → store donors
- Wall component on the site (and optionally in the app) + nickname moderation

## Phase 5 — Trust + polish + launch
- TRUST (the SmartScreen "not commonly downloaded" banner is reputation, NOT a virus):
  ✅ open-sourced app (MIT) + reproducible GitHub Actions build, ✅ version metadata,
  ✅ SHA-256 published, ✅ VirusTotal clean (1/69 = Bkav false-positive only) badged.
  PENDING: apply to SignPath Foundation for FREE OSS code-signing (needs traction;
  CI signing step pre-wired). EV cert (~$300/yr) = only instant-trust option, deferred.
- App auto-update check
- Slim local build to essentials ffmpeg (CI already uses it)
- Distribute via Reddit / YouTube / forums (not reliant on Google ranking)

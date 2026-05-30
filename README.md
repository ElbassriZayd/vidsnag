# VidSnag

Free desktop video downloader. Paste a URL (YouTube or other), pick a quality, download.
Supported by voluntary donations, with a public supporters wall.

- **Domain:** vidsnag.xyz (Porkbun, bought 2026-05-29)
- **Model:** Free desktop app. The download runs on the user's own PC (their IP), so there
  is no server doing downloads to be banned. The website is only a landing page + supporters wall.
- **Engine:** `yt-dlp` (already working in `telecharger.py`).

## Two parts

| Folder | What it is | Stack |
|--------|-----------|-------|
| `app/` | The desktop app users install (.exe) | Python + `yt-dlp` + GUI, packaged with PyInstaller |
| `website/` | Landing page + supporters wall | React/Vite on Vercel + Supabase + Ko-fi webhook |

## Existing files (the starting point)

- `telecharger.py` — working CLI downloader (the engine the app is built from)
- `liens.txt` — URL list used by the CLI
- `videos/` — output folder (git-ignored)
- `env_video/` — Python virtual environment (git-ignored)

See `ROADMAP.md` for phases and `PROJECT_STATE.md` for current status.

# Security

VidSnag is open source so you never have to trust a black box. This page documents
exactly what the app does on your machine, and how to verify it yourself.

## What the app actually does

VidSnag is a thin desktop wrapper around the open-source
[yt-dlp](https://github.com/yt-dlp/yt-dlp) engine. You paste a link, it probes the
formats, and it downloads the file you chose to a folder you chose. That's it.

## Network activity (full list — nothing hidden)

| When | What it contacts | Why |
|------|------------------|-----|
| You click **Fetch** / **Download** | the video's host (YouTube, etc.) | yt-dlp reads formats and downloads the file you asked for — the whole point of the app |
| After Fetch | the video host's thumbnail CDN | to show the little preview image of the video |
| App startup | **nothing** | UI fonts are bundled in the app; there are **no** Google Fonts / CDN / analytics calls |

There is **no telemetry, no analytics, no "phone home," no auto-update beacon, no
account, no tracking**. The app never uploads anything about you. Downloads happen
entirely on your computer.

## What's NOT in the code (audited)

A line-by-line audit of everything that ships in the `.exe` found **none** of:
`eval` / `exec`, `subprocess` / shell-out, raw sockets, `requests`/`urllib` calls of
its own, `base64`/`marshal`/`pickle` obfuscation, registry writes, scheduled tasks /
autostart / persistence, or any code that runs at install. The only Windows API calls
are `pywin32` setting the **taskbar icon** (cosmetic).

Runtime dependencies (`yt-dlp`, `pywebview`, `pywin32`, `pillow`) were scanned with
`pip-audit`: **no known vulnerabilities**.

## Verify it yourself

- **Read the code** — it's all in this repo (`app/engine.py`, `app/desktop.py`, `app/web/`).
- **Build it yourself** — `pyinstaller vidsnag.spec` (or read `.github/workflows/build.yml`),
  reproduces the released `.exe`.
- **Check the hash** — every release publishes a SHA-256; `certutil -hashfile VidSnag.exe SHA256`.
- **Scan it** — it's on [VirusTotal](https://www.virustotal.com); Microsoft Defender and
  every major engine pass it.

## About the antivirus / SmartScreen warnings

The "isn't commonly downloaded" banner and the occasional single antivirus flag are
**false positives**, not malware:

- They come from the **PyInstaller** packer (which bundles Python into one `.exe`) and from
  the app being **new and unsigned** — not from anything in the code.
- Names like `W32.Malware.*` (Bkav) or `Program:Win32/Wacapew.C!ml` (Microsoft `!ml` =
  a machine-learning *guess*) are **generic heuristics**. "Win32"/"W32" just means
  "a Windows program," not 32-bit and not a named threat.
- These clear up as the app gains download reputation, and disappear entirely once the
  build is code-signed.

## Reporting a security issue

Found something? Open an issue, or email the maintainer (see the website at
https://vidsnag.xyz). Please don't post exploit details publicly before it's fixed.

# VidSnag

**Free desktop video downloader for Windows. No ads, no sign-up, no sketchy sites.**

Paste a link, pick a quality (4K → 480p, or MP3), download. Everything runs on your
own computer. Powered by the open-source [yt-dlp](https://github.com/yt-dlp/yt-dlp)
engine with ffmpeg bundled in. Open source under the MIT license — read every line below.

## Download

➡️ **[Download VidSnag for Windows](../../releases/latest/download/VidSnag.exe)**

No installer, no setup. Double-click `VidSnag.exe` and you're running.

### "Windows says it isn't commonly downloaded"

That's a **reputation** message, **not** a virus. It shows for any brand-new app that
isn't code-signed yet — Windows still lets you Open/Save (a real threat would be
blocked outright). Click **More info → Run anyway**.

You don't have to take our word for it:
- **The source is right here** — read it, or build the exe yourself (see below).
- **Verify the download** matches the published build with its SHA-256 on the
  [Releases](../../releases/latest) page:
  ```powershell
  certutil -hashfile VidSnag.exe SHA256
  ```

## What it does

- Up to 4K video, or audio-only MP3
- Hundreds of sites (YouTube, Vimeo, TikTok, X, Facebook, Twitch, and more)
- Choose exactly where files land
- Zero ads, zero tracking — downloads happen locally

## Run from source

```bash
python -m pip install -r app/requirements.txt
python -m app.desktop
```
(ffmpeg must be on your PATH when running from source; the packaged .exe bundles it.)

## Build the .exe yourself

```bash
pip install pyinstaller
# point FFMPEG_DIR at a folder containing ffmpeg.exe + ffprobe.exe, then:
pyinstaller vidsnag.spec --noconfirm
# -> dist/VidSnag.exe
```
The same build runs automatically in GitHub Actions ([`.github/workflows/build.yml`](.github/workflows/build.yml))
on every release tag, so the published binary is reproducible.

## Project layout

| Path | What |
|------|------|
| `app/engine.py` | yt-dlp wrappers (probe + download) |
| `app/desktop.py` | native window (WebView2) + JS bridge |
| `app/web/` | the HTML/CSS/JS UI |
| `vidsnag.spec` | PyInstaller build recipe |

## Keep it alive

VidSnag is free forever, built and maintained by one person. Website:
**https://vidsnag.xyz**

---

You are responsible for what you download. Respect copyright and each site's terms of service.

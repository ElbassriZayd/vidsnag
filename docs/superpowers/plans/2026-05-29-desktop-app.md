# VidSnag Desktop App (Phase 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** A free Windows desktop app where the user pastes a video URL, picks a quality, and downloads — the download runs on the user's own PC (ban-resistant model).

**Architecture:** Refactor the existing interactive CLI (`telecharger.py`) into a non-interactive `engine.py` (pure functions a UI can call), then wrap it in a Tkinter GUI (`gui.py`) that runs downloads on a background thread and reports progress. Packaging to a single `.exe` (PyInstaller) is a later step (needs more disk).

**Tech Stack:** Python 3.11 (existing `env_video` venv), `yt-dlp` 2026.03.17 (installed), Tkinter (stdlib, no install), ffmpeg (installed via WinGet).

---

### Task 1: Engine — probe + format options

**Files:**
- Create: `app/engine.py`

- [ ] **Step 1: Write `app/engine.py` core (no interactive input)**

```python
"""VidSnag download engine. Pure, UI-agnostic wrappers around yt-dlp."""
import os
import yt_dlp

DEFAULT_OUTPUT_DIR = "videos"

# Resolution tiers offered, highest to lowest.
VIDEO_TIERS = [
    ("2160p (4K)", 2160),
    ("1440p (2K)", 1440),
    ("1080p (Full HD)", 1080),
    ("720p (HD)", 720),
    ("480p", 480),
]


def max_height(info: dict) -> int:
    """Highest video height available for a probed URL (0 if none)."""
    return max(
        (f.get("height") or 0)
        for f in info.get("formats", [])
        if f.get("vcodec") and f.get("vcodec") != "none"
    ) if info.get("formats") else 0


def format_options(max_h: int) -> list[tuple[str, str, int | None]]:
    """Return list of (label, mode, height) choices for a given max height.

    mode "video" + height None  -> original quality
    mode "video" + height int   -> capped to that height
    mode "mp3"   + height None  -> audio only, mp3
    """
    options = [("Video - original quality", "video", None)]
    for label, h in VIDEO_TIERS:
        if h < max_h:
            options.append((f"Video - {label}", "video", h))
    options.append(("MP3 (audio only)", "mp3", None))
    return options


def probe(url: str) -> dict:
    """Return {'title': str, 'max_height': int, 'options': list} for a URL.

    Raises yt_dlp.utils.DownloadError on an unusable URL.
    """
    opts = {"quiet": True, "skip_download": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    mh = max_height(info)
    return {
        "title": info.get("title", url),
        "max_height": mh,
        "options": format_options(mh),
    }
```

- [ ] **Step 2: Verify it imports and probes**

Run: `./env_video/Scripts/python.exe -c "from app.engine import probe; import json; print(probe('https://www.youtube.com/watch?v=BaW_jenozKc')['title'])"`
Expected: prints a video title, no traceback.

- [ ] **Step 3: Commit**

```bash
git add app/engine.py
git commit -m "feat(app): add engine probe + format options"
```

---

### Task 2: Engine — download with progress callback

**Files:**
- Modify: `app/engine.py`

- [ ] **Step 1: Append download functions to `app/engine.py`**

```python
def _ydl_opts(mode, height, output_dir, progress_hook):
    base = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook] if progress_hook else [],
        "quiet": True,
        "no_warnings": True,
    }
    if mode == "mp3":
        return {
            **base,
            "format": "ba/b",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    fmt = "bv*+ba/b" if height is None else f"bv*[height<={height}]+ba/b/b[height<={height}]"
    return {**base, "format": fmt, "merge_output_format": "mp4"}


def download(url, mode="video", height=None, output_dir=DEFAULT_OUTPUT_DIR, progress_hook=None):
    """Download one URL. progress_hook(d) receives yt-dlp progress dicts.

    Raises yt_dlp.utils.DownloadError on failure.
    """
    os.makedirs(output_dir, exist_ok=True)
    with yt_dlp.YoutubeDL(_ydl_opts(mode, height, output_dir, progress_hook)) as ydl:
        ydl.download([url])
```

- [ ] **Step 2: Verify a small MP3 download works**

Run: `./env_video/Scripts/python.exe -c "from app.engine import download; download('https://www.youtube.com/watch?v=BaW_jenozKc', mode='mp3', output_dir='videos')"`
Expected: an `.mp3` appears in `videos/`, no traceback.

- [ ] **Step 3: Commit**

```bash
git add app/engine.py
git commit -m "feat(app): add download with progress hook"
```

---

### Task 3: Tkinter GUI

**Files:**
- Create: `app/gui.py`

- [ ] **Step 1: Write `app/gui.py`**

```python
"""VidSnag desktop GUI (Tkinter). Run: python -m app.gui"""
import os
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from app import engine


class VidSnagApp:
    def __init__(self, root):
        self.root = root
        root.title("VidSnag")
        root.geometry("560x300")
        self.events = queue.Queue()
        self.options = []

        frm = ttk.Frame(root, padding=16)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Video URL:").pack(anchor="w")
        self.url_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.url_var, width=64).pack(fill="x", pady=(0, 8))

        self.fetch_btn = ttk.Button(frm, text="Fetch qualities", command=self.on_fetch)
        self.fetch_btn.pack(anchor="w")

        self.title_lbl = ttk.Label(frm, text="", wraplength=520, foreground="#444")
        self.title_lbl.pack(anchor="w", pady=(8, 0))

        self.quality = ttk.Combobox(frm, state="disabled", width=40)
        self.quality.pack(anchor="w", pady=8)

        self.dl_btn = ttk.Button(frm, text="Download", command=self.on_download, state="disabled")
        self.dl_btn.pack(anchor="w")

        self.progress = ttk.Progressbar(frm, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(12, 4))
        self.status = ttk.Label(frm, text="Paste a URL and fetch qualities.")
        self.status.pack(anchor="w")

        self.root.after(100, self._drain_events)

    # --- background workers ---
    def on_fetch(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("VidSnag", "Please paste a URL first.")
            return
        self.fetch_btn["state"] = "disabled"
        self.status["text"] = "Fetching available qualities..."
        threading.Thread(target=self._fetch_worker, args=(url,), daemon=True).start()

    def _fetch_worker(self, url):
        try:
            result = engine.probe(url)
            self.events.put(("probed", result))
        except Exception as e:
            self.events.put(("error", f"Could not read this URL: {e}"))

    def on_download(self):
        url = self.url_var.get().strip()
        idx = self.quality.current()
        if idx < 0 or idx >= len(self.options):
            return
        _, mode, height = self.options[idx]
        self.dl_btn["state"] = "disabled"
        self.fetch_btn["state"] = "disabled"
        self.progress["value"] = 0
        self.status["text"] = "Starting download..."
        threading.Thread(target=self._download_worker, args=(url, mode, height), daemon=True).start()

    def _download_worker(self, url, mode, height):
        def hook(d):
            self.events.put(("progress", d))
        try:
            engine.download(url, mode=mode, height=height, progress_hook=hook)
            self.events.put(("done", None))
        except Exception as e:
            self.events.put(("error", f"Download failed: {e}"))

    # --- UI thread event pump ---
    def _drain_events(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                self._handle(kind, payload)
        except queue.Empty:
            pass
        self.root.after(100, self._drain_events)

    def _handle(self, kind, payload):
        if kind == "probed":
            self.options = payload["options"]
            self.title_lbl["text"] = payload["title"]
            self.quality["values"] = [o[0] for o in self.options]
            self.quality["state"] = "readonly"
            self.quality.current(0)
            self.dl_btn["state"] = "normal"
            self.fetch_btn["state"] = "normal"
            self.status["text"] = f"Max resolution: {payload['max_height']}p. Pick a format."
        elif kind == "progress":
            d = payload
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                done = d.get("downloaded_bytes") or 0
                if total:
                    self.progress["value"] = done * 100 / total
                self.status["text"] = f"Downloading... {d.get('_percent_str', '').strip()}"
            elif d.get("status") == "finished":
                self.status["text"] = "Processing (merging / converting)..."
        elif kind == "done":
            self.progress["value"] = 100
            self.dl_btn["state"] = "normal"
            self.fetch_btn["state"] = "normal"
            self.status["text"] = f"Done. Saved in '{os.path.abspath(engine.DEFAULT_OUTPUT_DIR)}'."
            messagebox.showinfo("VidSnag", "Download complete.")
        elif kind == "error":
            self.dl_btn["state"] = "normal"
            self.fetch_btn["state"] = "normal"
            self.status["text"] = payload
            messagebox.showerror("VidSnag", payload)


def main():
    root = tk.Tk()
    VidSnagApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create `app/__init__.py`** (empty, makes `app` a package)

```python
```

- [ ] **Step 3: Launch the GUI manually to smoke-test**

Run: `./env_video/Scripts/python.exe -m app.gui`
Expected: a window opens; fetching a URL fills the quality dropdown; download fills the progress bar and saves a file.

- [ ] **Step 4: Commit**

```bash
git add app/gui.py app/__init__.py
git commit -m "feat(app): add Tkinter GUI with threaded download + progress"
```

---

### Task 4: Wire entry point + docs

**Files:**
- Create: `app/__main__.py`

- [ ] **Step 1: Add `app/__main__.py`** so `python -m app` launches the GUI

```python
from app.gui import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add app/__main__.py
git commit -m "feat(app): add python -m app entry point"
```

---

## Deferred (need more disk / later phases)
- PyInstaller packaging to a single `.exe` (bundle yt-dlp + ffmpeg)
- Batch mode (multiple URLs / playlist)
- Phase 2+: landing page, donations, supporters wall (separate plans)

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
        threading.Thread(
            target=self._download_worker, args=(url, mode, height), daemon=True
        ).start()

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

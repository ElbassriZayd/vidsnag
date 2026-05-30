"""VidSnag desktop GUI (Tkinter). Run: python -m app.gui"""
import os
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from app import engine
from app import theme


class VidSnagApp:
    def __init__(self, root):
        self.root = root
        root.title("VidSnag")
        root.geometry("620x440")
        root.minsize(520, 420)

        self.f = theme.apply(root)
        self.events = queue.Queue()
        self.options = []

        # ---- Header ----
        header = ttk.Frame(root, style="App.TFrame", padding=(28, 22, 28, 12))
        header.pack(fill="x")
        row = ttk.Frame(header, style="App.TFrame")
        row.pack(fill="x")
        ttk.Label(row, text="VidSnag", style="Wordmark.TLabel").pack(side="left")
        ttk.Label(row, text="FREE", style="Tag.TLabel").pack(side="left", padx=(10, 0), pady=(6, 0))
        ttk.Label(
            header,
            text="Paste a link, choose a quality, download. It runs on your computer.",
            style="Status.TLabel",
        ).pack(anchor="w", pady=(6, 0))

        # ---- Card ----
        card = ttk.Frame(root, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True, padx=28, pady=(8, 24))
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text="VIDEO URL", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(card, textvariable=self.url_var, style="App.TEntry", font=self.f["body"])
        self.url_entry.grid(row=1, column=0, sticky="ew", pady=(6, 12))
        self.url_entry.bind("<Return>", lambda e: self.on_fetch())

        self.fetch_btn = ttk.Button(card, text="Fetch qualities", style="Ghost.TButton", command=self.on_fetch, cursor="hand2")
        self.fetch_btn.grid(row=2, column=0, sticky="w")

        # divider
        ttk.Frame(card, style="App.TFrame", height=1).grid(row=3, column=0, sticky="ew", pady=18)

        self.title_lbl = ttk.Label(card, text="No video loaded yet.", style="Title.TLabel", wraplength=520)
        self.title_lbl.grid(row=4, column=0, sticky="w")

        ttk.Label(card, text="QUALITY", style="FieldLabel.TLabel").grid(row=5, column=0, sticky="w", pady=(14, 0))
        self.quality = ttk.Combobox(card, state="disabled", style="App.TCombobox", font=self.f["body"])
        self.quality.grid(row=6, column=0, sticky="ew", pady=(6, 16))

        self.dl_btn = ttk.Button(card, text="Download", style="CTA.TButton", command=self.on_download, state="disabled", cursor="hand2")
        self.dl_btn.grid(row=7, column=0, sticky="w")

        # ---- Progress / status ----
        self.progress = ttk.Progressbar(card, mode="determinate", maximum=100, style="App.Horizontal.TProgressbar")
        self.progress.grid(row=8, column=0, sticky="ew", pady=(20, 8))
        self.status = ttk.Label(card, text="Paste a URL and fetch qualities.", style="Status.TLabel")
        self.status.grid(row=9, column=0, sticky="w")

        self.url_entry.focus_set()
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
            self.status["text"] = f"Max resolution: {payload['max_height']}p. Pick a format and download."
        elif kind == "progress":
            d = payload
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                done = d.get("downloaded_bytes") or 0
                if total:
                    self.progress["value"] = done * 100 / total
                pct = d.get("_percent_str", "").strip()
                spd = d.get("_speed_str", "").strip()
                self.status["text"] = f"Downloading  {pct}   {spd}"
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

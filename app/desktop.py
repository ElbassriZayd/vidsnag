"""VidSnag desktop shell — a native window rendering the HTML UI via WebView2.

JavaScript calls into the Api class; the verified engine does the work on the
user's machine. Progress is pushed back to JS via window.evaluate_js.
Run: python -m app.desktop
"""
import os
import threading

import webview

from app import engine

HTML_PATH = os.path.join(os.path.dirname(__file__), "web", "index.html")


def _default_download_dir():
    """User's Downloads folder, falling back to the cwd 'videos' dir."""
    home = os.path.expanduser("~")
    downloads = os.path.join(home, "Downloads")
    target = os.path.join(downloads, "VidSnag") if os.path.isdir(downloads) else engine.DEFAULT_OUTPUT_DIR
    os.makedirs(target, exist_ok=True)
    return target


class Api:
    def __init__(self):
        self._window = None
        self.output_dir = _default_download_dir()

    def set_window(self, window):
        self._window = window

    def get_folder(self):
        """Current download folder (shown in the UI)."""
        return self.output_dir

    def choose_folder(self):
        """Open the native folder picker; return the chosen (or unchanged) folder."""
        try:
            result = self._window.create_file_dialog(webview.FOLDER_DIALOG, directory=self.output_dir)
            if result:
                chosen = result[0] if isinstance(result, (list, tuple)) else result
                if chosen:
                    self.output_dir = chosen
        except Exception:
            pass
        return self.output_dir

    def _js(self, fn, arg):
        """Call a JS function with one JSON-encoded string argument."""
        if self._window is None:
            return
        import json
        self._window.evaluate_js(f"window.{fn} && window.{fn}({json.dumps(arg)})")

    def probe(self, url):
        """Return video info for the UI, or {'error': msg}."""
        try:
            return engine.probe(url)
        except Exception as e:
            return {"error": str(e)}

    def download(self, url, mode, height):
        """Kick off a download on a background thread; report via JS callbacks."""
        def hook(d):
            status = d.get("status")
            if status == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                done = d.get("downloaded_bytes") or 0
                pct = (done * 100 / total) if total else 0
                self._js("onProgress", {
                    "status": "downloading",
                    "percent": pct,
                    "speed": (d.get("_speed_str") or "").strip(),
                })
            elif status == "finished":
                self._js("onProgress", {"status": "processing"})

        def worker():
            try:
                engine.download(url, mode=mode, height=height,
                                output_dir=self.output_dir, progress_hook=hook)
                self._js("onDone", os.path.abspath(self.output_dir))
            except Exception as e:
                self._js("onError", f"Download failed: {e}")

        threading.Thread(target=worker, daemon=True).start()
        return {"ok": True}


def main():
    api = Api()
    window = webview.create_window(
        "VidSnag",
        HTML_PATH,
        js_api=api,
        width=560,
        height=720,          # tall enough that nothing is clipped on open
        min_size=(460, 600),
        background_color="#FBF7F0",
    )
    api.set_window(window)
    icon = os.path.join(os.path.dirname(__file__), "web", "assets", "vidsnag.ico")
    try:
        webview.start(icon=icon)
    except TypeError:
        webview.start()


if __name__ == "__main__":
    main()

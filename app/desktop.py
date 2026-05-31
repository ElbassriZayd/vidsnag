"""VidSnag desktop shell — a native window rendering the HTML UI via WebView2.

JavaScript calls into the Api class; the verified engine does the work on the
user's machine. Progress is pushed back to JS via window.evaluate_js.
Run: python -m app.desktop
"""
import os
import sys
import threading

import webview

from app import engine


def _res(*parts):
    """Resolve a bundled resource from source, PyInstaller, or Nuitka.

    PyInstaller (onefile) ships web/ at app/web under sys._MEIPASS. Nuitka and
    source runs resolve relative to this module (Nuitka rewrites __file__ to the
    unpacked location).
    """
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, "app", *parts)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)


HTML_PATH = _res("web", "index.html")
ICON_PATH = _res("web", "assets", "vidsnag.ico")


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


def _set_app_id():
    """Give the process its own taskbar identity so Windows shows our icon
    instead of grouping under pythonw.exe."""
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("VidSnag.App")
    except Exception:
        pass


def _set_window_icon():
    """Replace the inherited python icon with VidSnag's, in title bar + taskbar.

    The WebView2 backend ignores webview.start(icon=...), so we set it directly
    via the Win32 API once the window exists. Best-effort: silently no-ops if
    pywin32 is missing or the window can't be found.
    """
    try:
        import win32con
        import win32gui
    except Exception:
        return

    hwnd = win32gui.FindWindow(None, "VidSnag")
    if not hwnd:
        return
    try:
        big = win32gui.LoadImage(0, ICON_PATH, win32con.IMAGE_ICON, 256, 256,
                                 win32con.LR_LOADFROMFILE)
        small = win32gui.LoadImage(0, ICON_PATH, win32con.IMAGE_ICON, 32, 32,
                                   win32con.LR_LOADFROMFILE)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, big)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, small)
    except Exception:
        pass


def main():
    _set_app_id()
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

    # set the taskbar/title-bar icon once the native window exists
    window.events.loaded += _set_window_icon

    try:
        webview.start(icon=ICON_PATH)
    except TypeError:
        webview.start()


if __name__ == "__main__":
    main()

"""VidSnag download engine. Pure, UI-agnostic wrappers around yt-dlp."""
import os
import sys
import yt_dlp

DEFAULT_OUTPUT_DIR = "videos"


def _ffmpeg_location():
    """Where bundled ffmpeg/ffprobe live in the packaged app, else None.

    Nuitka ships them next to this module (app/ffmpeg.exe); PyInstaller extracts
    them into sys._MEIPASS. None lets yt-dlp fall back to ffmpeg on PATH (dev).
    """
    candidates = [
        os.path.dirname(os.path.abspath(__file__)),   # Nuitka: app/ffmpeg.exe
        getattr(sys, "_MEIPASS", "") or "",            # PyInstaller onefile
    ]
    for base in candidates:
        if base and os.path.exists(os.path.join(base, "ffmpeg.exe")):
            return base
    return None


FFMPEG_LOCATION = _ffmpeg_location()

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
    heights = [
        (f.get("height") or 0)
        for f in info.get("formats", [])
        if f.get("vcodec") and f.get("vcodec") != "none"
    ]
    return max(heights) if heights else 0


def format_options(max_h: int):
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
    """Return {'title', 'max_height', 'options'} for a URL.

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
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader") or info.get("channel"),
        "duration_string": info.get("duration_string"),
    }


def _ydl_opts(mode, height, output_dir, progress_hook):
    base = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook] if progress_hook else [],
        "quiet": True,
        "no_warnings": True,
    }
    if FFMPEG_LOCATION:
        base["ffmpeg_location"] = FFMPEG_LOCATION
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

    # Prefer widely-compatible codecs (H.264 video + AAC/m4a audio) so the result
    # plays in Windows Media Player and everywhere else. YouTube's "best" streams
    # are often av1 video + opus audio, which technically have sound but most
    # Windows players can't decode -> looks like "video with no voice". We fall
    # back to best-available only if compatible streams don't exist.
    cap = "" if height is None else f"[height<={height}]"
    fmt = (
        f"bv*{cap}[vcodec^=avc1]+ba[acodec^=mp4a]/"   # H.264 + AAC (most compatible)
        f"bv*{cap}[ext=mp4]+ba[ext=m4a]/"             # any mp4 video + m4a audio
        f"bv*{cap}+ba/"                               # any video + any audio
        f"b{cap}/b"                                    # last resort: single file
    )
    return {
        **base,
        "format": fmt,
        "merge_output_format": "mp4",
        # If a merge still ends up with a codec mp4 dislikes, re-encode audio to AAC.
        "postprocessor_args": {"merger": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]},
    }


def download(url, mode="video", height=None, output_dir=DEFAULT_OUTPUT_DIR, progress_hook=None):
    """Download one URL. progress_hook(d) receives yt-dlp progress dicts.

    Raises yt_dlp.utils.DownloadError on failure.
    """
    os.makedirs(output_dir, exist_ok=True)
    with yt_dlp.YoutubeDL(_ydl_opts(mode, height, output_dir, progress_hook)) as ydl:
        ydl.download([url])

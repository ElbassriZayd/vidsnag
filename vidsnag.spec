# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the VidSnag desktop app (onefile, windowed).
# Build: env_video\Scripts\pyinstaller.exe vidsnag.spec --noconfirm
import os
from PyInstaller.utils.hooks import collect_submodules

# ffmpeg + ffprobe are bundled so the app works with no system install.
FF = r"C:\Users\ME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"

hidden = collect_submodules("yt_dlp") + ["win32gui", "win32con"]

a = Analysis(
    ["vidsnag_main.py"],
    pathex=["."],
    binaries=[
        (os.path.join(FF, "ffmpeg.exe"), "."),
        (os.path.join(FF, "ffprobe.exe"), "."),
    ],
    datas=[("app/web", "app/web")],
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=["numpy", "PIL", "tkinter", "matplotlib", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="VidSnag",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon="app/web/assets/vidsnag.ico",
    version="version.txt",
)

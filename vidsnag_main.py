"""PyInstaller entry point for the VidSnag desktop app.

Kept at the project root so the `app` package imports cleanly during the
frozen build. Run from source with `python -m app.desktop`.
"""
from app.desktop import main

if __name__ == "__main__":
    main()

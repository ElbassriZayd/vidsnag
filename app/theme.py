"""VidSnag visual theme — colors, fonts, and ttk style setup.

Kept separate from gui.py so the look can evolve without touching logic.
Palette: modern dark 'media app' look with an indigo accent.
"""
import tkinter.font as tkfont
from tkinter import ttk

# --- Palette ---
BG = "#13151A"          # app background
SURFACE = "#1C1F27"     # card background
SURFACE_2 = "#252A34"   # inputs / inset
BORDER = "#2E343F"      # hairline borders
TEXT = "#ECEEF1"        # primary text
MUTED = "#9AA1AD"       # secondary text
ACCENT = "#6D5EF7"      # CTA indigo
ACCENT_HOVER = "#5B4DE0"
ACCENT_ACTIVE = "#4C3FD0"
GHOST_HOVER = "#2A2F3A"  # subtle button hover
TRACK = "#252A34"       # progress trough
SUCCESS = "#36C28B"


def fonts():
    """Return a dict of named fonts (Segoe UI is the Windows system font)."""
    family = "Segoe UI"
    return {
        "wordmark": tkfont.Font(family=family, size=20, weight="bold"),
        "tag": tkfont.Font(family=family, size=9),
        "label": tkfont.Font(family=family, size=10),
        "title": tkfont.Font(family=family, size=11, weight="bold"),
        "body": tkfont.Font(family=family, size=10),
        "button": tkfont.Font(family=family, size=10, weight="bold"),
        "status": tkfont.Font(family=family, size=9),
    }


def apply(root):
    """Configure root + ttk styles. Returns the fonts dict for callers."""
    f = fonts()
    root.configure(bg=BG)

    # Combobox popdown (the dropdown list) is a classic Tk widget, themed via options.
    root.option_add("*TCombobox*Listbox.background", SURFACE_2)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox.font", f["body"])

    style = ttk.Style(root)
    style.theme_use("clam")  # most themeable base theme

    style.configure("App.TFrame", background=BG)
    style.configure("Card.TFrame", background=SURFACE)

    style.configure("Wordmark.TLabel", background=BG, foreground=TEXT, font=f["wordmark"])
    style.configure("Tag.TLabel", background=ACCENT, foreground="#FFFFFF", font=f["tag"], padding=(8, 2))
    style.configure("FieldLabel.TLabel", background=SURFACE, foreground=MUTED, font=f["label"])
    style.configure("Title.TLabel", background=SURFACE, foreground=TEXT, font=f["title"])
    style.configure("Status.TLabel", background=SURFACE, foreground=MUTED, font=f["status"])

    # Entry
    style.configure(
        "App.TEntry",
        fieldbackground=SURFACE_2, foreground=TEXT, insertcolor=TEXT,
        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
        borderwidth=1, padding=8,
    )
    style.map("App.TEntry", bordercolor=[("focus", ACCENT)], lightcolor=[("focus", ACCENT)])

    # Combobox
    style.configure(
        "App.TCombobox",
        fieldbackground=SURFACE_2, background=SURFACE_2, foreground=TEXT,
        arrowcolor=TEXT, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
        borderwidth=1, padding=6,
    )
    style.map(
        "App.TCombobox",
        fieldbackground=[("readonly", SURFACE_2)],
        bordercolor=[("focus", ACCENT)],
        foreground=[("disabled", MUTED)],
    )

    # Primary (CTA) button — flat, accent, no focus ring boxes
    style.configure(
        "CTA.TButton",
        background=ACCENT, foreground="#FFFFFF", font=f["button"],
        borderwidth=0, focusthickness=0, focuscolor=ACCENT, padding=(18, 10),
        relief="flat",
    )
    style.map(
        "CTA.TButton",
        background=[("disabled", SURFACE_2), ("active", ACCENT_ACTIVE), ("!disabled", ACCENT)],
        foreground=[("disabled", MUTED)],
    )
    # because ttk maps are ordered, set hover explicitly via 'active' above; add pressed
    style.map("CTA.TButton", background=[("pressed", ACCENT_ACTIVE), ("active", ACCENT_HOVER), ("disabled", SURFACE_2)])

    # Ghost / secondary button — outline style
    style.configure(
        "Ghost.TButton",
        background=SURFACE, foreground=TEXT, font=f["button"],
        borderwidth=1, focusthickness=0, padding=(14, 9), relief="flat",
        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
    )
    style.map(
        "Ghost.TButton",
        background=[("active", GHOST_HOVER), ("pressed", GHOST_HOVER)],
        bordercolor=[("active", ACCENT)],
        foreground=[("disabled", MUTED)],
    )

    # Progress bar
    style.configure(
        "App.Horizontal.TProgressbar",
        troughcolor=TRACK, background=ACCENT, bordercolor=TRACK,
        lightcolor=ACCENT, darkcolor=ACCENT, thickness=8, borderwidth=0,
    )

    return f

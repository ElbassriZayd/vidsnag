import os
import yt_dlp

FICHIER_LIENS = "liens.txt"
DOSSIER_SORTIE = "videos"

# Paliers de résolution proposés (du plus haut au plus bas).
PALIERS_VIDEO = [
    ("2160p (4K)", 2160),
    ("1440p (2K)", 1440),
    ("1080p (Full HD)", 1080),
    ("720p (HD)", 720),
    ("480p", 480),
]


def construire_options(max_height):
    """Construit la liste des options à proposer pour une vidéo donnée.

    Renvoie une liste de tuples (label, mode, hauteur) :
      - mode = "video", hauteur = None  → qualité d'origine
      - mode = "video", hauteur = int   → vidéo capée à cette hauteur
      - mode = "mp3",   hauteur = None  → audio seul converti en MP3
    """
    options = [("Vidéo — qualité d'origine", "video", None)]
    for label, h in PALIERS_VIDEO:
        if h < max_height:
            options.append((f"Vidéo — {label}", "video", h))
    options.append(("MP3 (audio seulement)", "mp3", None))
    return options


def demander_choix(titre, max_height, options):
    print()
    print(f"  Vidéo : {titre}")
    print(f"  Résolution maximale disponible : {max_height}p")
    print(f"  Choisissez le format :")
    for i, (label, _, _) in enumerate(options, start=1):
        print(f"    {i}) {label}")
    while True:
        choix = input(f"  Votre choix [1-{len(options)}] (défaut 1) : ").strip() or "1"
        if choix.isdigit() and 1 <= int(choix) <= len(options):
            return options[int(choix) - 1]
        print("  Choix invalide, réessayez.")


def ydl_opts_pour(mode, hauteur):
    base = {
        "outtmpl": os.path.join(DOSSIER_SORTIE, "%(title)s.%(ext)s"),
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
    fmt = "bv*+ba/b" if hauteur is None else f"bv*[height<={hauteur}]+ba/b/b[height<={hauteur}]"
    return {**base, "format": fmt, "merge_output_format": "mp4"}


def hauteur_max_disponible(info):
    return max(
        (f.get("height") or 0)
        for f in info.get("formats", [])
        if f.get("vcodec") and f.get("vcodec") != "none"
    )


def main():
    if not os.path.exists(FICHIER_LIENS):
        print(f"Erreur : Le fichier {FICHIER_LIENS} n'existe pas.")
        return

    with open(FICHIER_LIENS, "r", encoding="utf-8") as f:
        urls = [ligne.strip() for ligne in f if ligne.strip()]

    if not urls:
        print("Aucun lien trouvé dans le fichier.")
        return

    os.makedirs(DOSSIER_SORTIE, exist_ok=True)
    print(f"{len(urls)} vidéo(s) à traiter...\n")

    sondeur = yt_dlp.YoutubeDL({"quiet": True, "skip_download": True, "no_warnings": True})

    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] Analyse de : {url}")
        try:
            info = sondeur.extract_info(url, download=False)
        except Exception as e:
            print(f"  Impossible d'analyser cette URL : {e}\n")
            continue

        titre = info.get("title", url)
        max_h = hauteur_max_disponible(info)
        options = construire_options(max_h)
        _, mode, hauteur = demander_choix(titre, max_h, options)

        try:
            with yt_dlp.YoutubeDL(ydl_opts_pour(mode, hauteur)) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"  Échec du téléchargement : {e}\n")
            continue

    print("\nTerminé !")


if __name__ == "__main__":
    main()

"""
generer_icones.py

Génère les icônes du dashboard à partir d'une image source unique
et les place directement dans le dossier assets/ du projet Dash.

Usage :
    python generer_icones.py chemin/vers/mon_logo.png

Prérequis :
    pip install Pillow
"""

import sys
from pathlib import Path
from PIL import Image

# =========================================================
# CONFIGURATION
# =========================================================

# Dossier assets/ du projet Dash (à ajuster si le script n'est
# pas lancé depuis la racine du projet)
ASSETS_DIR = Path("assets")

# Fichiers à générer : (nom_de_sortie, taille_en_pixels)
ICONES_A_GENERER = [
    ("mon_icone.png", 512),        # icône principale (favicon HD)
    ("mon_icone_180.png", 180),    # apple-touch-icon (écran d'accueil iOS)
    ("favicon.ico", 32),           # secours pour {%favicon%} / anciens navigateurs
]


def generer_icones(chemin_source: str):
    source_path = Path(chemin_source)

    if not source_path.exists():
        print(f"❌ Fichier introuvable : {source_path}")
        sys.exit(1)

    ASSETS_DIR.mkdir(exist_ok=True)

    with Image.open(source_path) as img:
        # Conversion en RGBA pour préserver la transparence si présente
        img = img.convert("RGBA")

        for nom_sortie, taille in ICONES_A_GENERER:
            # Redimensionne en conservant les proportions dans un carré
            # taille x taille, fond transparent si l'image n'est pas carrée
            icone = Image.new("RGBA", (taille, taille), (0, 0, 0, 0))

            img_resized = img.copy()
            img_resized.thumbnail((taille, taille), Image.LANCZOS)

            offset = (
                (taille - img_resized.width) // 2,
                (taille - img_resized.height) // 2,
            )
            icone.paste(img_resized, offset, img_resized)

            destination = ASSETS_DIR / nom_sortie

            if nom_sortie.endswith(".ico"):
                icone.save(destination, format="ICO", sizes=[(taille, taille)])
            else:
                icone.save(destination, format="PNG")

            print(f"✅ Créé : {destination}  ({taille}x{taille})")

    print("\nTerminé. Fichiers prêts dans le dossier assets/.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python generer_icones.py chemin/vers/mon_logo.png")
        sys.exit(1)

    generer_icones(sys.argv[1])
import pandas as pd
import os

# ============================
# CHEMIN DU FICHIER EXCEL
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = os.path.join(BASE_DIR, "data", "services_transformes.xlsx")


# ============================
# LISTE DES SECTEURS / FEUILLES
# ============================

SECTEURS = [
    "HYGIENE",
    "POSTE TELECOMMUNICATION et TIC",
    "SFD ET BANQUES Les institutions d’appui",
    "TRANSPORTS",
    "CULTUTRE",
    " SPORTS ",
    "JEUNESSE",
    "PROCTECTION JUDICIARE ET SOCIALE AEMO",
    "VULNERABILITE PROTECTION SOCIALE",
    "FAMILLE ET AUTONOMISATION",
    "ENERGIE",
    "SANTE",
    "EDUCATION FORMATION",
    "EAU",
    "ASSAINISSEMENT",
    "AQUACULTURE",
    "PECHE",
    "Industrie Artisanat",
    "Commerce et ARM",
    "AGRICULTURE",
    "ELEVAGE",
    "MINES ET GEOLOGIE",
    "TOURISME"
]


# ============================
# CHARGEMENT DE TOUTES LES FEUILLES
# ============================

def load_all_sectors():
    """
    Charge toutes les feuilles Excel
    Retourne un dictionnaire :
    {
        'SANTE': dataframe,
        'EAU': dataframe,
        ...
    }
    """

    data_dict = {}

    for secteur in SECTEURS:
        try:
            df = pd.read_excel(FILE_PATH, sheet_name=secteur)

            # nettoyage colonnes
            df.columns = df.columns.str.strip()

            # suppression espaces texte
            df = df.apply(
                lambda col: col.str.strip() if col.dtype == "object" else col
            )

            data_dict[secteur] = df

        except Exception as e:
            print(f"Erreur chargement feuille {secteur} : {e}")

    return data_dict


# ============================
# CHARGEMENT D'UN SECTEUR UNIQUE
# ============================

def load_sector(secteur_name):
    """
    Charge une feuille spécifique
    """

    try:
        df = pd.read_excel(FILE_PATH, sheet_name=secteur_name)

        df.columns = df.columns.str.strip()

        df = df.apply(
            lambda col: col.str.strip() if col.dtype == "object" else col
        )

        return df

    except Exception as e:
        print(f"Erreur : {e}")
        return pd.DataFrame()
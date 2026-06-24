# import pandas as pd
# import os
# from functools import lru_cache

# DATA_PATH = "data"

# def get_all_sectors():
#     files = os.listdir(DATA_PATH)
#     return [f.replace(".xlsx", "") for f in files if f.endswith(".xlsx")]

# @lru_cache(maxsize=32)
# def load_sector_data(sector):
#     path = f"{DATA_PATH}/{sector}.xlsx"
#     df = pd.read_excel(path)
#     df.columns = df.columns.str.strip().str.lower()
#     return df

# def get_unique_values(df, col):
#     if col not in df.columns:
#         return []
#     return sorted(df[col].dropna().unique())

# import pandas as pd
# import os

# DATA_PATH = "data"


# # =========================
# # LISTE DES SECTEURS
# # =========================
# def get_all_sectors():

#     files = os.listdir(DATA_PATH)

#     liste_secteurs = [
#         f.replace(".xlsx", "")
#         for f in files
#         if f.endswith(".xlsx")
#     ]

#     return sorted(liste_secteurs)


# # =========================
# # LOAD DATA
# # =========================
# def load_sector_data(sector):

#     path = os.path.join(
#         DATA_PATH,
#         f"{sector}.xlsx"
#     )

#     df = pd.read_excel(path)

#     # NORMALISATION COLONNES
#     df.columns = (
#         df.columns
#         .str.strip()
#         .str.lower()
#     )

#     return df


# # =========================
# # VALEURS UNIQUES
# # =========================
# def get_unique_values(df, col):

#     if col not in df.columns:
#         return []

#     return sorted(
#         df[col]
#         .dropna()
#         .unique()
#     )

# import pandas as pd

# =========================
# GITHUB RAW URL
# =========================

# =========================
# GITHUB RAW URL
# =========================

# USERNAME="sekougit"
# REPOSITORY="dashboard_multi_sectoriel_kaffrine"

# BASE_URL = (
#     "https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/main/data"
# )

# #"https://raw.githubusercontent.com/sekougit/dashboard_multi_sectoriel_kaffrine/main/data/EAU.xlsx"


# # =========================
# # LISTE DES SECTEURS
# # =========================
# def get_all_sectors():

#     fichiers = [
# 'AGRICULTURE',
# 'AQUACULTURE',
# 'ASSAINISSEMENT',
# 'COMMERCE_ARM',
# 'CULTURE',
# 'EAU',
# 'EDUCATION_FORMATION',
# 'ELEVAGE',
# 'ENERGIE',
# 'FAMILLE_AUTONOMISATION',
# 'HYGIENE',
# 'INDUSTRIE_ARTISANAT',
# 'JEUNESSE',
# 'MINES_GEOLOGIE',
# 'PECHE',
# 'PROTECTION_JUDICIAIRE_SOCIALE_AEMO',
# 'SANTE',
# 'SFD_BANQUES',
# 'SPORTS',
# 'TIC',
# 'TOURISME',
# 'TRANSPORTS',
# 'VULNERABILITE_PROTECTION_SOCIAL',
#     ]

#     return sorted(fichiers)


# # =========================
# # LOAD DATA
# # =========================
# def load_sector_data(sector):

#     url = f"{BASE_URL}/{sector}.xlsx"

#     df = pd.read_excel(url,engine="openpyxl")

#     # NORMALISATION
#     df.columns = (
#         df.columns
#         .str.strip()
#         .str.lower()
#     )

#     return df


# # =========================
# # UNIQUE VALUES
# # =========================
# def get_unique_values(df, col):

#     if col not in df.columns:
#         return []

#     return sorted(
#         df[col]
#         .dropna()
#         .unique()
#     )


############### GOOGLE DRIVE #############################

import pandas as pd
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()


# =========================
# FICHIERS
# =========================
FILES = {
'AGRICULTURE' : os.getenv('AGRICULTURE_URL'),
'AQUACULTURE' : os.getenv('AQUACULTURE_URL'),
'ASSAINISSEMENT' : os.getenv('ASSAINISSEMENT_URL'),
'COMMERCE_ARM' : os.getenv('COMMERCE_ARM_URL'),
'CULTURE' : os.getenv('CULTURE_URL'),
'EAU' : os.getenv('EAU_URL'),
'EDUCATION_FORMATION' : os.getenv('EDUCATION_FORMATION_URL'),
'ELEVAGE' : os.getenv('ELEVAGE_URL'),
'ENERGIE' : os.getenv('ENERGIE_URL'),
'FAMILLE_AUTONOMISATION' : os.getenv('FAMILLE_AUTONOMISATION_URL'),
'HYGIENE' : os.getenv('HYGIENE_URL'),
'INDUSTRIE_ARTISANAT' : os.getenv('INDUSTRIE_ARTISANAT_URL'),
'JEUNESSE' : os.getenv('JEUNESSE_URL'),
'MINES_GEOLOGIE' : os.getenv('MINES_GEOLOGIE_URL'),
'PECHE' : os.getenv('PECHE_URL'),
'PROTECTION_JUDICIAIRE_SOCIALE_AEMO' : os.getenv('PROTECTION_JUDICIAIRE_SOCIALE_AEMO_URL'),
'SANTE' : os.getenv('SANTE_URL'),
'SFD_BANQUES' : os.getenv('SFD_BANQUES_URL'),
'SPORTS' : os.getenv('SPORTS_URL'),
'TIC' : os.getenv('TIC_URL'),
'TOURISME' : os.getenv('TOURISME_URL'),
'TRANSPORTS' : os.getenv('TRANSPORTS_URL'),
'VULNERABILITE_PROTECTION_SOCIAL' : os.getenv('VULNERABILITE_PROTECTION_SOCIAL_URL')
}


# =========================
# LISTE DES SECTEURS
# =========================
def get_all_sectors():

    return list(FILES.keys())


# =========================
# LOAD DATA
# =========================
# =========================
# CACHE MÉMOIRE
# =========================
@lru_cache(maxsize=32)
def load_sector_data(sector):

    url = FILES[sector]

    df = pd.read_excel(
        url,
        engine="openpyxl"
    )

    # NORMALISATION
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )
    df["annee"] = df["annee"].astype(str)
    df["region"] = df["region"].astype("category")
    df["departement"] = df["departement"].astype("category")
    df["commune"] = df["commune"].astype("category")

    return df


# =========================
# UNIQUE VALUES
# =========================
def get_unique_values(df, col):

    if col not in df.columns:
        return []

    return sorted(
        df[col]
        .dropna()
        .unique()
    )
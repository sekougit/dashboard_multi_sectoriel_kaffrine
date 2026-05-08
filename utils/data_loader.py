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


# =========================
# FICHIERS
# =========================
FILES = {

    "AGRICULTURE":
    "https://docs.google.com/spreadsheets/d/1VjpYE7JaRg-vWWil2E9a7-6pNwRmtbHk/export?format=xlsx",
    "AQUACULTURE":
    "https://docs.google.com/spreadsheets/d/1HyUftJnDUa5BndMeCd_iC2yDWDps4mJL/export?format=xlsx",
    "ASSAINISSEMENT":
    "https://docs.google.com/spreadsheets/d/13nJM6BufSjT6mzJ4FFv9S2_a1pn_G3tD/export?format=xlsx",
    "COMMERCE_ARM":
    "https://docs.google.com/spreadsheets/d/11Peb2tkDzsOR5G-ZzEe6PueFxlgMr4eH/export?format=xlsx",

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
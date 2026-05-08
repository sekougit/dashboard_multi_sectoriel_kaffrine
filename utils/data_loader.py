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
'AGRICULTURE' :'https://docs.google.com/spreadsheets/d/1VjpYE7JaRg-vWWil2E9a7-6pNwRmtbHk/export?format=xlsx',
'AQUACULTURE' :'https://docs.google.com/spreadsheets/d/1HyUftJnDUa5BndMeCd_iC2yDWDps4mJL/export?format=xlsx',
'ASSAINISSEMENT' :'https://docs.google.com/spreadsheets/d/13nJM6BufSjT6mzJ4FFv9S2_a1pn_G3tD/export?format=xlsx',
'COMMERCE_ARM' :'https://docs.google.com/spreadsheets/d/11Peb2tkDzsOR5G-ZzEe6PueFxlgMr4eH/export?format=xlsx',
'CULTURE' :'https://docs.google.com/spreadsheets/d/1-tWp3BFQLR0t17LYHJNeO7iup2wA4fJf/export?format=xlsx',
'EAU' :'https://docs.google.com/spreadsheets/d/1y_36MoAFyUjjcd-SEeJ3AyW_b8APo6kZ/export?format=xlsx',
'EDUCATION_FORMATION' :'https://docs.google.com/spreadsheets/d/1RH_wpaY_PudhUo9zDc4vDUJLQZbZdz_r/export?format=xlsx',
'ELEVAGE' :'https://docs.google.com/spreadsheets/d/17WwfiErnxXEpUWEld9hMsP4Wd-yWdKz0/export?format=xlsx',
'ENERGIE' :'https://docs.google.com/spreadsheets/d/16xQkyXACaFokropG91QsEy-TooVfNeH_/export?format=xlsx',
'FAMILLE_AUTONOMISATION' :'https://docs.google.com/spreadsheets/d/1gvdFdJsqgxUz287b_h7RQWF6yCkTHw6F/export?format=xlsx',
'HYGIENE' :'https://docs.google.com/spreadsheets/d/1N_fb2RHdWHtjR4n13oZxNB20B8GEFJzz/export?format=xlsx',
'INDUSTRIE_ARTISANAT' :'https://docs.google.com/spreadsheets/d/1GsQgi6mx51r1JsVgvd0tYNZesOuQ64JF/export?format=xlsx',
'JEUNESSE' :'https://docs.google.com/spreadsheets/d/1ik4cF2bsIoTo15pRhCnQb4fPVmoVNGOi/export?format=xlsx',
'MINES_GEOLOGIE' :'https://docs.google.com/spreadsheets/d/1sj2wgSWWMPhpu_PjvZkJWN54HvxLSJ0y/export?format=xlsx',
'PECHE' :'https://docs.google.com/spreadsheets/d/147cNLTKkkPGiCEb8IH7bNWhGVNGX_8Dg/export?format=xlsx',
'PROTECTION_JUDICIAIRE_SOCIALE_AEMO' :'https://docs.google.com/spreadsheets/d/1GUMNN4hKHrVvOb3ewf9GjyLns6v6mRDF/export?format=xlsx',
'SANTE' :'https://docs.google.com/spreadsheets/d/1G1fT1TATkOdAHpNMPp2yd3_GQjtXXXgM/export?format=xlsx',
'SFD_BANQUES' :'https://docs.google.com/spreadsheets/d/1-ximzzHKAGdSHRJBqOToRAlixKxaoXTg/export?format=xlsx',
'SPORTS' :'https://docs.google.com/spreadsheets/d/1huFJfNS-06JJlHD2-0w3shIGij0A9vMs/export?format=xlsx',
'TIC' :'https://docs.google.com/spreadsheets/d/1Z7SLGUWt0K8Sww8wXls3T3g0ynmUh6nY/export?format=xlsx',
'TOURISME' :'https://docs.google.com/spreadsheets/d/1uF4O4Lqz_cFrDX-uUzWtFsAjJ1BoAHOV/export?format=xlsx',
'TRANSPORTS' :'https://docs.google.com/spreadsheets/d/1VYsmouYHoFN5RqBcb1_4LDpc6cYtJjW_/export?format=xlsx',
'VULNERABILITE_PROTECTION_SOCIAL' :'https://docs.google.com/spreadsheets/d/1w_F9hxVc9TPaagwQdVVmeifnMaiEAWph/export?format=xlsx',
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
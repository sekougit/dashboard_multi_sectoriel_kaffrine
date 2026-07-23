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
'AGRICULTURE': os.getenv('AGRICULTURE_URL'),
'AQUACULTURE': os.getenv('AQUACULTURE_URL'),
'ASSAINISSEMENT': os.getenv('ASSAINISSEMENT_URL'),
'CENTRE_FORMATION': os.getenv('CENTRE_FORMATION_URL'),
'COMMERCE_ARM': os.getenv('COMMERCE_ARM_URL'),
'CULTURE': os.getenv('CULTURE_URL'),
'EAU': os.getenv('EAU_URL'),
'ELEVAGE': os.getenv('ELEVAGE_URL'),
'ENERGIE': os.getenv('ENERGIE_URL'),
'ENSEIGNEMENT_DAARA': os.getenv('ENSEIGNEMENT_DAARA_URL'),
'ENSEIGNEMENT_ELEMENTAIRE': os.getenv('ENSEIGNEMENT_ELEMENTAIRE_URL'),
'ENSEIGNEMENT_MOYEN': os.getenv('ENSEIGNEMENT_MOYEN_URL'),
'ENSEIGNEMENT_PRESCOLAIRE': os.getenv('ENSEIGNEMENT_PRESCOLAIRE_URL'),
'ENSEIGNEMENT_SECONDAIRE': os.getenv('ENSEIGNEMENT_SECONDAIRE_URL'),
'FAMILLE_AUTONOMISATION': os.getenv('FAMILLE_AUTONOMISATION_URL'),
'GESTION_FONCIERE': os.getenv('GESTION_FONCIERE_URL'),
'GOUVERNANCE_TERRITORIALE': os.getenv('GOUVERNANCE_TERRITORIALE_URL'),
'HYGIENE': os.getenv('HYGIENE_URL'),
'INDUSTRIE_ARTISANAT': os.getenv('INDUSTRIE_ARTISANAT_URL'),
'JEUNESSE': os.getenv('JEUNESSE_URL'),
'MINES_GEOLOGIE': os.getenv('MINES_GEOLOGIE_URL'),
'PECHE': os.getenv('PECHE_URL'),
'POSTE_TELECOMS_TIC': os.getenv('POSTE_TELECOMS_TIC_URL'),
'PROTECTION_JUDICIAIRE_SOCIALE_AEMO': os.getenv('PROTECTION_JUDICIAIRE_SOCIALE_AEMO_URL'),
'SANTE': os.getenv('SANTE_URL'),
'SFD_BANQUES': os.getenv('SFD_BANQUES_URL'),
'SPORTS': os.getenv('SPORTS_URL'),
'TOURISME': os.getenv('TOURISME_URL'),
'TRANSPORTS': os.getenv('TRANSPORTS_URL'),
'VULNERABILITE_PROTECTION_SOCIALE': os.getenv('VULNERABILITE_PROTECTION_SOCIALE_URL'),
'POPULATION': os.getenv('POPULATION_URL')
}


# =========================
# LISTE DES SECTEURS
# =========================
def get_all_sectors():

    return sorted(FILES.keys())



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

def clear_cache():
    load_sector_data.cache_clear()

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


# =========================
# Détection automatique des indicateurs de taux
# =========================
RATE_KEYWORDS = [
    "taux",
    "ratio",
    "%",
    "proportion",
    "part",
    "indice",
    "moyenne",
    "pourcentage"
]


def is_rate_indicator(col):
    """
    Retourne True si l'indicateur est un taux,
    False si c'est une valeur brute.
    """
    col = col.lower()

    return any(k in col for k in RATE_KEYWORDS)

def aggregate_indicator(df, indicateur, group_cols):

    agg = "mean" if is_rate_indicator(indicateur) else "sum"

    result = (
        df.groupby(group_cols)
          .agg(
              **{
                  indicateur: (indicateur, agg),
                  "nb_na": (indicateur, lambda x: x.isna().sum())
              }
          )
          .reset_index()
    )

    return result

def compute_kpi(df, col):
    """
    Retourne :
        valeur,
        moyenne,
        nb_nan,
        type_indicateur
    """

    s = pd.to_numeric(df[col], errors="coerce")

    nb_nan = s.isna().sum()

    if is_rate_indicator(col):

        valeur = s.mean(skipna=True)
        typ = "taux"

    else:

        valeur = s.sum(skipna=True)
        typ = "brut"

    moyenne = s.mean(skipna=True)

    return valeur, moyenne, nb_nan, typ

def format_value(value, typ):
    """
    Formatage uniforme des KPI.
    """

    if pd.isna(value):
        return "NA"

    if typ == "taux":
        return f"{value:,.2f} %".replace(",", " ")

    return f"{value:,.0f}".replace(",", " ")

def count_missing(df, col):
    """
    Nombre de valeurs manquantes.
    """

    return pd.to_numeric(
        df[col],
        errors="coerce"
    ).isna().sum()
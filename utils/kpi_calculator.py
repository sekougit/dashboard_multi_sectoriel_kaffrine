import numpy as np
import pandas as pd

from config import (
    TAUX_KEYWORDS,
    NB_DECIMALES_TAUX,
    NB_DECIMALES_BRUT,
    LABEL_BRUT,
    LABEL_TAUX
)


# ==========================================================
# DETECTION DU TYPE D'INDICATEUR
# ==========================================================
def is_rate(indicateur: str) -> bool:
    """
    Détermine automatiquement si un indicateur est un taux.
    """

    nom = indicateur.lower()

    return any(
        mot.lower() in nom
        for mot in TAUX_KEYWORDS
    )


# ==========================================================
# TYPE D'AGREGATION
# ==========================================================
def aggregation_type(indicateur):

    return "mean" if is_rate(indicateur) else "sum"


# ==========================================================
# FORMAT AFFICHAGE
# ==========================================================
def format_value(indicateur, valeur):

    if pd.isna(valeur):
        return "-"

    if is_rate(indicateur):
        return f"{valeur:,.{NB_DECIMALES_TAUX}f}".replace(",", " ")

    return f"{valeur:,.{NB_DECIMALES_BRUT}f}".replace(",", " ")


# ==========================================================
# CALCUL KPI
# ==========================================================
def compute_kpi(df, indicateur):
    """
    Retourne toutes les informations utiles d'un KPI.
    """

    if indicateur not in df.columns:

        return None

    serie = pd.to_numeric(
        df[indicateur],
        errors="coerce"
    )

    nb_na = int(serie.isna().sum())

    nb_valides = int(serie.notna().sum())

    if nb_valides == 0:

        valeur = np.nan

    else:

        if is_rate(indicateur):

            valeur = serie.mean(skipna=True)

        else:

            valeur = serie.sum(skipna=True)

    return {

        "indicateur": indicateur,

        "type": "Taux" if is_rate(indicateur) else "Brut",

        "operation": LABEL_TAUX if is_rate(indicateur) else LABEL_BRUT,

        "value": valeur,

        "formatted": format_value(
            indicateur,
            valeur
        ),

        "na": nb_na,

        "valides": nb_valides,

        "total": len(serie)

    }


# ==========================================================
# AGREGATION PAR DIMENSION
# ==========================================================
def aggregate_indicator(
    df,
    indicateur,
    dimension
):
    """
    Utilisé par les graphiques.
    """

    if indicateur not in df.columns:

        return pd.DataFrame()

    data = df[
        [dimension, "annee", indicateur]
    ].copy()

    data[indicateur] = pd.to_numeric(
        data[indicateur],
        errors="coerce"
    )

    if is_rate(indicateur):

        grouped = (

            data.groupby(
                [dimension, "annee"],
                observed=True
            )[indicateur]

            .agg(

                valeur="mean",

                na=lambda x: x.isna().sum(),

                n=lambda x: x.notna().sum()

            )

            .reset_index()

        )

    else:

        grouped = (

            data.groupby(
                [dimension, "annee"],
                observed=True
            )[indicateur]

            .agg(

                valeur="sum",

                na=lambda x: x.isna().sum(),

                n=lambda x: x.notna().sum()

            )

            .reset_index()

        )

    return grouped


# ==========================================================
# POURCENTAGES
# ==========================================================
def compute_percent(grouped, colonne="valeur"):

    grouped = grouped.copy()

    if grouped.empty:

        grouped["percent"] = []

        return grouped

    grouped["percent"] = (

        grouped.groupby(
            grouped.columns[0]
        )[colonne]

        .transform(

            lambda x:
            x / x.sum() * 100
            if x.sum() != 0
            else 0

        )

    )

    return grouped


# ==========================================================
# HOVER DES GRAPHIQUES
# ==========================================================
def build_hover(indicateur):

    unite = "%" if is_rate(indicateur) else ""

    return (
        "<b>%{x}</b><br>"
        "Valeur : %{customdata[0]:,.2f}"
        + unite +
        "<br>"
        "NA : %{customdata[1]}"
        "<br>"
        "Valeurs utilisées : %{customdata[2]}"
        "<br>"
        "Proportion : %{y:.1f}%"
        "<extra></extra>"
    )


# ==========================================================
# LIBELLE KPI
# ==========================================================
def get_operation_label(indicateur):

    return LABEL_TAUX if is_rate(indicateur) else LABEL_BRUT
import dash
from dash import html, dcc, Input, Output, callback, ctx, no_update
import dash_bootstrap_components as dbc

from utils.data_loader import get_all_sectors, load_sector_data
from utils.filters import filter_data

dash.register_page(__name__, path="/secteurs")

# =========================
# FILTRES
# =========================
filters_bar = html.Div([

    dbc.Row([

        dbc.Col(dcc.Dropdown(
            id="secteur-dd",
            placeholder="Secteur",
            clearable=False
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="annee-dd",
            placeholder="Année",
            multi=True
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="region-dd",
            placeholder="Région",
            multi=True
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="departement-dd",
            placeholder="Département",
            multi=True
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="commune-dd",
            placeholder="Commune",
            multi=True
        ), width=2),

        # 🔥 INDICATEURS
        dbc.Col(dcc.Dropdown(
            id="indicateur-dd",
            placeholder="Indicateurs",
            multi=True
        ), width=2),

    ])

], className="filters-bar")


# =========================
# LAYOUT
# =========================
layout = html.Div([

    html.H2("📊 Analyse multi-sectorielle"),

    filters_bar,

    html.Div(id="kpi-container")

])

# =========================
# SECTEURS
# =========================
@callback(
    Output("secteur-dd", "options"),
    Input("secteur-dd", "id")
)
def load_secteurs(_):
    return [{"label": s, "value": s} for s in get_all_sectors()]


# =========================
# INDICATEURS DYNAMIQUES
# =========================
@callback(
    Output("indicateur-dd", "options"),
    Input("secteur-dd", "value")
)
def load_indicateurs(secteur):

    if not secteur:
        return []

    df = load_sector_data(secteur)

    exclude = ["annee", "region", "departement", "commune", "secteur"]

    cols = [
        c for c in df.columns
        if c not in exclude and df[c].dtype != "object"
    ]

    return [{"label": c, "value": c} for c in cols]


# =========================
# CASCADE FILTRES
# =========================
@callback(
    Output("annee-dd", "options"),
    Output("region-dd", "options"),
    Output("departement-dd", "options"),
    Output("commune-dd", "options"),

    Input("secteur-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
)
def update_filters(secteur, regions, departements):

    if not secteur:
        return [], [], [], []

    df = load_sector_data(secteur)

    all_regions = sorted(df["region"].dropna().unique())

    if regions:
        df = df[df["region"].isin(regions)]

    all_departements = sorted(df["departement"].dropna().unique())

    if departements:
        df = df[df["departement"].isin(departements)]

    communes = sorted(df["commune"].dropna().unique())
    annees = sorted(df["annee"].dropna().unique())

    return (
        [{"label": i, "value": i} for i in annees],
        [{"label": i, "value": i} for i in all_regions],
        [{"label": i, "value": i} for i in all_departements],
        [{"label": i, "value": i} for i in communes],
    )


# =========================
# RESET SAFE
# =========================
@callback(
    Output("departement-dd", "value"),
    Output("commune-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
)
def reset_filters(region, departement):

    trigger = ctx.triggered_id

    if trigger == "region-dd":
        return None, None

    if trigger == "departement-dd":
        return no_update, None

    return no_update, no_update


# =========================
# KPI FINAL
# =========================
@callback(
    Output("kpi-container", "children"),

    Input("secteur-dd", "value"),
    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
    Input("indicateur-dd", "value"),
)
def update_kpis(secteur, annees, regions, departements, communes, indicateurs):

    if not secteur:
        return "Sélectionnez un secteur"

    df = load_sector_data(secteur)

    if annees:
        df = df[df["annee"].isin(annees)]
    if regions:
        df = df[df["region"].isin(regions)]
    if departements:
        df = df[df["departement"].isin(departements)]
    if communes:
        df = df[df["commune"].isin(communes)]

    if df.empty:
        return "Aucune donnée"

    exclude = ["annee", "region", "departement", "commune", "secteur"]

    if not indicateurs:
        indicateurs = [c for c in df.columns if c not in exclude]

    return dbc.Row([
        dbc.Col(
            html.Div([
                html.Div(ind.upper(), className="kpi-title"),
                html.Div(f"{df[ind].sum():.0f}", className="kpi-value"),
                html.Div(f"Moy: {df[ind].mean():.2f}", className="kpi-sub")
            ], className="kpi-card"),
            width=3
        )
        for ind in indicateurs if ind in df.columns
    ], className="g-3")
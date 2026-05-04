import dash
from dash import html, dcc, Input, Output, callback, ctx, no_update
import dash_bootstrap_components as dbc

from utils.data_loader import get_all_sectors, load_sector_data, get_unique_values
from utils.filters import filter_data
from utils.kpi_calculator import compute_kpis

dash.register_page(__name__, path="/secteurs")

# =========================
# FILTRES (STICKY)
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
            placeholder="Année"
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="region-dd",
            placeholder="Région"
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="departement-dd",
            placeholder="Département"
        ), width=2),

        dbc.Col(dcc.Dropdown(
            id="commune-dd",
            placeholder="Commune"
        ), width=2),

    ])

], className="filters-bar")


# =========================
# LAYOUT
# =========================
layout = html.Div([

    html.H2("📊 Analyse par secteur"),

    filters_bar,

    html.Div(id="kpi-container", className="mt-4")

])


# =========================
# CALLBACK 1 : secteurs
# =========================
@callback(
    Output("secteur-dd", "options"),
    Input("secteur-dd", "id")
)
def load_secteurs(_):
    sectors = get_all_sectors()
    return [{"label": s, "value": s} for s in sectors]


# =========================
# CALLBACK 2 : CASCADE FILTRES
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
def update_filters(secteur, region, departement):

    if not secteur:
        return [], [], [], []

    df = load_sector_data(secteur)

    # REGION
    regions = sorted(df["region"].dropna().unique())

    if region:
        df = df[df["region"] == region]

    # DEPARTEMENT
    departements = sorted(df["departement"].dropna().unique())

    if departement:
        df = df[df["departement"] == departement]

    # COMMUNE (dépend du département)
    communes = sorted(df["commune"].dropna().unique())

    # ANNEE
    annees = sorted(df["annee"].dropna().unique())

    return (
        [{"label": i, "value": i} for i in annees],
        [{"label": i, "value": i} for i in regions],
        [{"label": i, "value": i} for i in departements],
        [{"label": i, "value": i} for i in communes],
    )


# =========================
# CALLBACK 3 : RESET CASCADE (SANS CONFLIT)
# =========================
@callback(
    Output("departement-dd", "value"),
    Output("commune-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
)
def reset_filters(region, departement):

    trigger = ctx.triggered_id

    # si région change → reset tout en dessous
    if trigger == "region-dd":
        return None, None

    # si département change → reset commune
    elif trigger == "departement-dd":
        return no_update, None

    return no_update, no_update


# =========================
# CALLBACK 4 : RESET ANNEE
# =========================
@callback(
    Output("annee-dd", "value"),
    Input("secteur-dd", "value")
)
def reset_annee(secteur):
    return None


# =========================
# CALLBACK 5 : KPI DESIGN PRO
# =========================
@callback(
    Output("kpi-container", "children"),
    Input("secteur-dd", "value"),
    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
)
def update_kpis(secteur, annee, region, departement, commune):

    if not secteur:
        return html.Div("Veuillez sélectionner un secteur")

    df = load_sector_data(secteur)
    df = filter_data(df, secteur, annee, region, departement, commune)

    if df.empty:
        return html.Div("Aucune donnée disponible")

    kpis = compute_kpis(df)

    cards = []

    for k, v in kpis.items():
        cards.append(
            dbc.Col(
                html.Div([
                    html.Div(k.upper(), className="kpi-title"),
                    html.Div(f"{v['total']:.0f}", className="kpi-value"),
                    html.Div(f"Moyenne: {v['moyenne']:.2f}", className="kpi-sub")
                ], className="kpi-card"),
                width=3
            )
        )

    return dbc.Row(cards, className="g-3")
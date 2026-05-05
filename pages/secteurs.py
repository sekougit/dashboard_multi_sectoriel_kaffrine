import dash
from dash import html, dcc, Input, Output, callback, ctx, no_update, State
import dash_bootstrap_components as dbc

from utils.data_loader import get_all_sectors, load_sector_data

dash.register_page(__name__, path="/secteurs")

# =========================
# 🔥 COMPONENT DROPDOWN AVEC LABEL
# =========================
def dropdown_block(label, component):
    return html.Div([
        html.Div(label, className="filter-label"),
        component
    ], className="filter-block")


# =========================
# 🔥 FORMAT NOM KPI
# =========================
def format_kpi_name(name):
    return (
        name.replace("_", " ")
            .replace("indicateur", "ind.")
            .replace("nombre", "nbr")
            .replace("population", "pop")
            .title()
    )


# =========================
# LAYOUT
# =========================
layout = html.Div([

    html.H2("📊 Analyse multi-sectorielle"),

    html.Div([
        dbc.Row([

            dbc.Col(dropdown_block("📊 Secteur",
                dcc.Dropdown(id="secteur-dd", clearable=False)
            ), width=2),

            dbc.Col(dropdown_block("📅 Année",
                dcc.Dropdown(id="annee-dd", multi=True)
            ), width=2),

            dbc.Col(dropdown_block("🌍 Région",
                dcc.Dropdown(id="region-dd", multi=True)
            ), width=2),

            dbc.Col(dropdown_block("🏙️ Département",
                dcc.Dropdown(id="departement-dd", multi=True)
            ), width=2),

            dbc.Col(dropdown_block("📍 Commune",
                dcc.Dropdown(id="commune-dd", multi=True)
            ), width=2),

            dbc.Col(dropdown_block("📈 Indicateurs",
                dcc.Dropdown(id="indicateur-dd", multi=True)
            ), width=2),

        ])
    ], className="filters-bar"),

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
# INDICATEURS
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

    cols = [c for c in df.columns if c not in exclude and df[c].dtype != "object"]

    return [{"label": c, "value": c} for c in cols]


# =========================
# CASCADE
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

    regions_all = sorted(df["region"].dropna().unique())

    if regions:
        df = df[df["region"].isin(regions)]

    deps_all = sorted(df["departement"].dropna().unique())

    if departements:
        df = df[df["departement"].isin(departements)]

    communes = sorted(df["commune"].dropna().unique())
    annees = sorted(df["annee"].dropna().unique())

    return (
        [{"label": i, "value": i} for i in annees],
        [{"label": i, "value": i} for i in regions_all],
        [{"label": i, "value": i} for i in deps_all],
        [{"label": i, "value": i} for i in communes],
    )


# =========================
# RESTORE + RESET
# =========================
@callback(
    Output("secteur-dd", "value"),
    Output("annee-dd", "value"),
    Output("region-dd", "value"),
    Output("departement-dd", "value"),
    Output("commune-dd", "value"),
    Output("indicateur-dd", "value"),

    Input("region-dd", "value"),
    Input("departement-dd", "value"),

    State("global-filters", "data"),
)
def manage_filters(region, departement, data):

    trigger = ctx.triggered_id

    if trigger == "region-dd":
        return no_update, no_update, no_update, None, None, no_update

    if trigger == "departement-dd":
        return no_update, no_update, no_update, no_update, None, no_update

    if data:
        return (
            data.get("secteur"),
            data.get("annee"),
            data.get("region"),
            data.get("departement"),
            data.get("commune"),
            data.get("indicateur"),
        )

    return no_update, no_update, no_update, no_update, no_update, no_update


# =========================
# SAVE
# =========================
@callback(
    Output("global-filters", "data"),

    Input("secteur-dd", "value"),
    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
    Input("indicateur-dd", "value"),

    prevent_initial_call=True
)
def save_filters(secteur, annee, region, departement, commune, indicateur):

    return {
        "secteur": secteur,
        "annee": annee,
        "region": region,
        "departement": departement,
        "commune": commune,
        "indicateur": indicateur
    }


# =========================
# KPI
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

    cards = []

    for ind in indicateurs:

        if ind not in df.columns:
            continue

        total = df[ind].sum()
        moyenne = df[ind].mean()

        total_fmt = f"{total:,.0f}".replace(",", " ")
        moy_fmt = f"{moyenne:,.2f}".replace(",", " ")

        cards.append(
            dbc.Col(
                html.Div([

                    html.Div(format_kpi_name(ind), className="kpi-title", title=ind),

                    html.Div(total_fmt, className="kpi-value"),

                    html.Div(f"● Moyenne : {moy_fmt}", className="kpi-sub")

                ], className="kpi-card"),

                xs=12, sm=6, md=4, lg=3
            )
        )

    return dbc.Row(cards, className="g-3")
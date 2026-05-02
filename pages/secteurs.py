from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from utils.load_data import load_sector

# ==========================
# SECTEURS
# ==========================
SECTEURS = [
    "AGRICULTURE",
    "AQUACULTURE",
    "SANTE",
    "EDUCATION",
    "ENERGIE"
]

def fmt(x):
    try:
        return f"{float(x):,.2f}"
    except:
        return "0.00"

# ==========================
# LAYOUT
# ==========================
secteurs_layout = html.Div([

    html.H2("Secteurs"),

    # ==========================
    # SELECT SECTEUR
    # ==========================
    dcc.Dropdown(
        id="secteur-select",
        options=[{"label": s, "value": s} for s in SECTEURS],
        placeholder="Choisir un secteur"
    ),

    html.Br(),

    # ==========================
    # FILTRES
    # ==========================
    dbc.Row([

        dbc.Col(dcc.Dropdown(id="filter-region", placeholder="Région"), md=4),
        dbc.Col(dcc.Dropdown(id="filter-departement", placeholder="Département"), md=4),
        dbc.Col(dcc.Dropdown(id="filter-commune", placeholder="Commune"), md=4),

    ]),

    html.Br(),

    # ==========================
    # KPI
    # ==========================
    html.Div(id="kpi-container")
])

# =========================================================
# 🔥 CALLBACK 1 : LOAD FILTRES (RÉGION)
# =========================================================
@callback(
    Output("filter-region", "options"),
    Input("secteur-select", "value")
)
def load_regions(sector):

    if not sector:
        return []

    df = load_sector(sector)

    return [
        {"label": r, "value": r}
        for r in sorted(df["region"].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 2 : LOAD DÉPARTEMENTS
# =========================================================
@callback(
    Output("filter-departement", "options"),
    Input("secteur-select", "value"),
    Input("filter-region", "value")
)
def load_departements(sector, region):

    if not sector:
        return []

    df = load_sector(sector)

    if region:
        df = df[df["region"] == region]

    return [
        {"label": d, "value": d}
        for d in sorted(df["departement"].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 3 : LOAD COMMUNES
# =========================================================
@callback(
    Output("filter-commune", "options"),
    Input("secteur-select", "value"),
    Input("filter-departement", "value")
)
def load_communes(sector, departement):

    if not sector:
        return []

    df = load_sector(sector)

    if departement:
        df = df[df["departement"] == departement]

    return [
        {"label": c, "value": c}
        for c in sorted(df["commune"].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 4 : KPI DYNAMIQUE
# =========================================================
@callback(
    Output("kpi-container", "children"),
    [
        Input("secteur-select", "value"),
        Input("filter-region", "value"),
        Input("filter-departement", "value"),
        Input("filter-commune", "value")
    ]
)
def display_kpis(sector, region, dep, com):

    if not sector:
        return html.H4("Sélectionne un secteur")

    df = load_sector(sector)

    if region:
        df = df[df["region"] == region]
    if dep:
        df = df[df["departement"] == dep]
    if com:
        df = df[df["commune"] == com]

    numeric_cols = df.select_dtypes(include=["number"]).columns

    kpis = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6(col),
                    html.H4(fmt(df[col].sum()))
                ])
            ),
            md=3
        )
        for col in numeric_cols
    ]

    return dbc.Row(kpis)
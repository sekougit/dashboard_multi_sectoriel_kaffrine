from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from utils.load_data import load_sector

# ==========================
# DATA
# ==========================
df = load_sector("AGRICULTURE")

# ==========================
# FORMAT
# ==========================
def fmt(x):
    try:
        return f"{float(x):,.2f}"
    except:
        return "0.00"

# ==========================
# OPTIONS INIT (RÉGION)
# ==========================
regions = sorted(df['region'].dropna().unique())

# ==========================
# LAYOUT
# ==========================
agriculture_layout = html.Div([

    html.H2("Agriculture - KPI"),

    # ==========================
    # FILTRES
    # ==========================
    dbc.Row([

        dbc.Col(
            dcc.Dropdown(
                id='agri-region',
                options=[{'label': r, 'value': r} for r in regions],
                placeholder="Région"
            ),
            md=4
        ),

        dbc.Col(
            dcc.Dropdown(
                id='agri-departement',
                placeholder="Département"
            ),
            md=4
        ),

        dbc.Col(
            dcc.Dropdown(
                id='agri-commune',
                placeholder="Commune"
            ),
            md=4
        ),

    ], className="mb-4"),

    # ==========================
    # KPI PRODUCTION
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='agri-kpi-superficie')),
        dbc.Col(html.H4(id='agri-kpi-production')),
    ]),

    # ==========================
    # CULTURES
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='agri-kpi-cereales')),
        dbc.Col(html.H4(id='agri-kpi-arachide')),
        dbc.Col(html.H4(id='agri-kpi-divers')),
        dbc.Col(html.H4(id='agri-kpi-horti')),
    ]),

    # ==========================
    # AMENAGEMENT
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='agri-kpi-terres')),
        dbc.Col(html.H4(id='agri-kpi-ouvrages')),
        dbc.Col(html.H4(id='agri-kpi-dac')),
    ]),

    # ==========================
    # INFRASTRUCTURES
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='agri-kpi-stockage')),
        dbc.Col(html.H4(id='agri-kpi-transformation')),
        dbc.Col(html.H4(id='agri-kpi-motorises')),
        dbc.Col(html.H4(id='agri-kpi-cooperatives')),
    ])

])

# =========================================================
# 🔥 CALLBACK 1 : UPDATE DEPARTEMENTS
# =========================================================
@callback(
    Output('agri-departement', 'options'),
    Input('agri-region', 'value')
)
def update_departement(region):

    dff = df.copy()

    if region:
        dff = dff[dff['region'] == region]

    return [
        {'label': d, 'value': d}
        for d in sorted(dff['departement'].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 2 : UPDATE COMMUNES
# =========================================================
@callback(
    Output('agri-commune', 'options'),
    Input('agri-departement', 'value')
)
def update_commune(departement):

    dff = df.copy()

    if departement:
        dff = dff[dff['departement'] == departement]

    return [
        {'label': c, 'value': c}
        for c in sorted(dff['commune'].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 3 : KPI
# =========================================================
@callback(
    [
        Output('agri-kpi-superficie', 'children'),
        Output('agri-kpi-production', 'children'),
        Output('agri-kpi-cereales', 'children'),
        Output('agri-kpi-arachide', 'children'),
        Output('agri-kpi-divers', 'children'),
        Output('agri-kpi-horti', 'children'),
        Output('agri-kpi-terres', 'children'),
        Output('agri-kpi-ouvrages', 'children'),
        Output('agri-kpi-dac', 'children'),
        Output('agri-kpi-stockage', 'children'),
        Output('agri-kpi-transformation', 'children'),
        Output('agri-kpi-motorises', 'children'),
        Output('agri-kpi-cooperatives', 'children'),
    ],
    [
        Input('agri-region', 'value'),
        Input('agri-departement', 'value'),
        Input('agri-commune', 'value')
    ]
)
def update_agri(region, departement, commune):

    dff = df.copy()

    if region:
        dff = dff[dff['region'] == region]
    if departement:
        dff = dff[dff['departement'] == departement]
    if commune:
        dff = dff[dff['commune'] == commune]

    return (
        fmt(dff["Superficie totale cultivée (ha)"].sum()),
        fmt(dff["Production totale Régionale en T"].sum()),
        fmt(dff["Superficies cultivées en Céréales (mil, maîs, sorgho et riz pluvial) en ha"].sum()),
        fmt(dff["Superficies cultivées en Arachide (ha)"].sum()),
        fmt(dff["Superficies cultivées en Espèces diverses (niébé, sésame, pastèque, manioc, etc.) en ha"].sum()),
        fmt(dff["Superficies exploitées en horticulture en ha"].sum()),
        fmt(dff["Superficies des Terres aménagées (ha)"].sum()),
        fmt(dff["Nombre Ouvrages hydro-agricoles (digues de retenues, anti-sel, etc…)"].sum()),
        fmt(dff["Nombre de Domaines agricoles communautaires (DAC)"].sum()),
        fmt(dff["Nombre Infratructures de Stockage (magasins, seccos métalliques, banques céréalières villageoises, ect…)"].sum()),
        fmt(dff["Nombre Unités de Transformation des Produits agricoles (moulins, batteuses, décortiqueuses, égreneuses, plateformes multifonctionnelles, etc…)"].sum()),
        fmt(dff["Nombre d'Unités de matériels motorisés (tracteurs équipés d'accessoires, motoculteurs équipés, moissonneuses-batteuses, etc…)"].sum()),
        fmt(dff["Nombre de Sociétés coopératives agricoles agréées"].sum()),
    )
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from utils.load_data import load_sector

# ==========================
# DATA
# ==========================
df = load_sector("AQUACULTURE")

# ==========================
# FORMAT
# ==========================
def fmt(x):
    try:
        return f"{float(x):,.2f}"
    except:
        return "0.00"

# ==========================
# OPTIONS INIT
# ==========================
regions = sorted(df['region'].dropna().unique())

# ==========================
# LAYOUT
# ==========================
aquaculture_layout = html.Div([

    html.H2("Aquaculture - KPI"),

    # ==========================
    # FILTRES
    # ==========================
    dbc.Row([

        dbc.Col(
            dcc.Dropdown(
                id='aq-region',
                options=[{'label': r, 'value': r} for r in regions],
                placeholder="Région"
            ),
            md=4
        ),

        dbc.Col(
            dcc.Dropdown(
                id='aq-departement',
                placeholder="Département"
            ),
            md=4
        ),

        dbc.Col(
            dcc.Dropdown(
                id='aq-commune',
                placeholder="Commune"
            ),
            md=4
        ),

    ], className="mb-4"),

    # ==========================
    # PRODUCTION
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='aq-kpi-plans-eau')),
        dbc.Col(html.H4(id='aq-kpi-bassins')),
        dbc.Col(html.H4(id='aq-kpi-fermes')),
        dbc.Col(html.H4(id='aq-kpi-fermes-non')),
    ]),

    # ==========================
    # TRANSFORMATION
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='aq-kpi-transformation')),
        dbc.Col(html.H4(id='aq-kpi-conditionnement')),
        dbc.Col(html.H4(id='aq-kpi-ecloseries')),
        dbc.Col(html.H4(id='aq-kpi-aliment')),
    ]),

    # ==========================
    # LOGISTIQUE
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='aq-kpi-carburant')),
        dbc.Col(html.H4(id='aq-kpi-frigo')),
        dbc.Col(html.H4(id='aq-kpi-camions')),
    ]),

    # ==========================
    # ORGANISATION
    # ==========================
    dbc.Row([
        dbc.Col(html.H4(id='aq-kpi-gie')),
    ])

])

# =========================================================
# 🔥 CALLBACK 1 : DEPARTEMENTS
# =========================================================
@callback(
    Output('aq-departement', 'options'),
    Input('aq-region', 'value')
)
def update_dept(region):

    dff = df.copy()

    if region:
        dff = dff[dff['region'] == region]

    return [
        {'label': d, 'value': d}
        for d in sorted(dff['departement'].dropna().unique())
    ]


# =========================================================
# 🔥 CALLBACK 2 : COMMUNES
# =========================================================
@callback(
    Output('aq-commune', 'options'),
    Input('aq-departement', 'value')
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
        Output('aq-kpi-plans-eau', 'children'),
        Output('aq-kpi-bassins', 'children'),
        Output('aq-kpi-fermes', 'children'),
        Output('aq-kpi-fermes-non', 'children'),
        Output('aq-kpi-transformation', 'children'),
        Output('aq-kpi-conditionnement', 'children'),
        Output('aq-kpi-ecloseries', 'children'),
        Output('aq-kpi-aliment', 'children'),
        Output('aq-kpi-carburant', 'children'),
        Output('aq-kpi-frigo', 'children'),
        Output('aq-kpi-camions', 'children'),
        Output('aq-kpi-gie', 'children'),
    ],
    [
        Input('aq-region', 'value'),
        Input('aq-departement', 'value'),
        Input('aq-commune', 'value')
    ]
)
def update_aqua(region, departement, commune):

    dff = df.copy()

    if region:
        dff = dff[dff['region'] == region]
    if departement:
        dff = dff[dff['departement'] == departement]
    if commune:
        dff = dff[dff['commune'] == commune]

    return (
        fmt(dff["Nombre de plans d'eau"].sum()),
        fmt(dff["Nombre de bassins en béton"].sum()),
        fmt(dff["Nombre de fermes aquacoles"].sum()),
        fmt(dff["Nombre de fermes non fonctionnels"].sum()),
        fmt(dff["Nombre d'Aires de transformation"].sum()),
        fmt(dff["Nombre d'Unités de conditionnement"].sum()),
        fmt(dff["Nombre d'écloseries"].sum()),
        fmt(dff["Nombre d’unités productions d’aliment de poisson"].sum()),
        fmt(dff["Nombre de Stations d’approvisionnement de carburant"].sum()),
        fmt(dff["Nombre de complexes frigorifiques"].sum()),
        fmt(dff["Nombre de camions frigorifiques"].sum()),
        fmt(dff["Nombre de GIE"].sum()),
    )
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utils.load_data import load_sector


# =====================
# CHARGEMENT DATA
# =====================

df = load_sector("AGRICULTURE")


# =====================
# DROPDOWNS
# =====================

regions = sorted(df['region'].dropna().unique())
departements = sorted(df['departement'].dropna().unique())
communes = sorted(df['commune'].dropna().unique())


# =====================
# LAYOUT
# =====================

agriculture_layout = html.Div([

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': i, 'value': i} for i in regions],
                placeholder='Choisir région'
            )
        ], md=4),

        dbc.Col([
            dcc.Dropdown(
                id='departement-filter',
                options=[{'label': i, 'value': i} for i in departements],
                placeholder='Choisir département'
            )
        ], md=4),

        dbc.Col([
            dcc.Dropdown(
                id='commune-filter',
                options=[{'label': i, 'value': i} for i in communes],
                placeholder='Choisir commune'
            )
        ], md=4),

    ], className="mb-4"),


    # =====================
    # CATEGORIE 1
    # =====================

    html.H3("Superficies et Productions Agricoles", className="section-title"),

    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Totale Cultivée (ha)"),
            html.H3(id='kpi-superficie-totale')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Production Totale Régionale (T)"),
            html.H3(id='kpi-production-regionale')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Céréales (ha)"),
            html.H3(id='kpi-cereales-surface')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Production Céréales (T)"),
            html.H3(id='kpi-cereales-prod')
        ])), md=3),

    ], className="mb-4"),


    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Arachide (ha)"),
            html.H3(id='kpi-arachide-surface')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Production Arachide (T)"),
            html.H3(id='kpi-arachide-prod')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Espèces Diverses (ha)"),
            html.H3(id='kpi-divers-surface')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Production Espèces Diverses (T)"),
            html.H3(id='kpi-divers-prod')
        ])), md=3),

    ], className="mb-4"),


    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Horticulture (ha)"),
            html.H3(id='kpi-horti-surface')
        ])), md=6),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Production Horticole (T)"),
            html.H3(id='kpi-horti-prod')
        ])), md=6),

    ], className="mb-4"),


    # =====================
    # CATEGORIE 2
    # =====================

    html.H3("Aménagements Hydroagricoles", className="section-title"),

    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie des Terres Aménagées (ha)"),
            html.H3(id='kpi-terres-amenagees')
        ])), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Ouvrages Hydro-agricoles"),
            html.H3(id='kpi-ouvrages')
        ])), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Nombre DAC"),
            html.H3(id='kpi-dac')
        ])), md=4),

    ], className="mb-4"),


    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie DAC (ha)"),
            html.H3(id='kpi-superficie-dac')
        ])), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Nombre Fermes Agricoles"),
            html.H3(id='kpi-fermes')
        ])), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Superficie Fermes (ha)"),
            html.H3(id='kpi-fermes-superficie')
        ])), md=4),

    ], className="mb-4"),


    # =====================
    # CATEGORIE 3
    # =====================

    html.H3("Matériels et Infrastructures", className="section-title"),

    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Infrastructures de Stockage"),
            html.H3(id='kpi-stockage')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Unités Transformation"),
            html.H3(id='kpi-transformation')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Matériels Motorisés"),
            html.H3(id='kpi-motorises')
        ])), md=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Traction Animale"),
            html.H3(id='kpi-traction')
        ])), md=3),

    ], className="mb-4"),


    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Coopératives Agricoles"),
            html.H3(id='kpi-cooperatives')
        ])), md=12),

    ])

])


from dash import callback
from dash.dependencies import Input, Output


@callback(
    [
        Output('kpi-superficie-totale', 'children'),
        Output('kpi-production-regionale', 'children'),
        Output('kpi-cereales-surface', 'children'),
        Output('kpi-cereales-prod', 'children'),
        Output('kpi-arachide-surface', 'children'),
        Output('kpi-arachide-prod', 'children'),
        Output('kpi-divers-surface', 'children'),
        Output('kpi-divers-prod', 'children'),
        Output('kpi-horti-surface', 'children'),
        Output('kpi-horti-prod', 'children'),
        Output('kpi-terres-amenagees', 'children'),
        Output('kpi-ouvrages', 'children'),
        Output('kpi-dac', 'children'),
        Output('kpi-superficie-dac', 'children'),
        Output('kpi-fermes', 'children'),
        Output('kpi-fermes-superficie', 'children'),
        Output('kpi-stockage', 'children'),
        Output('kpi-transformation', 'children'),
        Output('kpi-motorises', 'children'),
        Output('kpi-traction', 'children'),
        Output('kpi-cooperatives', 'children')
    ],
    [
        Input('region-filter', 'value'),
        Input('departement-filter', 'value'),
        Input('commune-filter', 'value')
    ]
)
def update_dashboard(region, departement, commune):

    filtered_df = df.copy()

    if region:
        filtered_df = filtered_df[filtered_df['region'] == region]

    if departement:
        filtered_df = filtered_df[filtered_df['departement'] == departement]

    if commune:
        filtered_df = filtered_df[filtered_df['commune'] == commune]

    return (
        f"{filtered_df['Superficie totale cultivée (ha)'].sum():,.0f}",
        f"{filtered_df['Production totale Régionale en T'].sum():,.0f}",
        f"{filtered_df['Superficies cultivées en Céréales (mil, maîs, sorgho et riz pluvial) en ha'].sum():,.0f}",
        f"{filtered_df['Production totale en Céréales  en T'].sum():,.0f}",
        f"{filtered_df['Superficies cultivées en Arachide (ha)'].sum():,.0f}",
        f"{filtered_df['Production totale en Arachide  en T'].sum():,.0f}",
        f"{filtered_df['Superficies cultivées en Espèces diverses (niébé, sésame, pastèque, manioc, etc.) en ha'].sum():,.0f}",
        f"{filtered_df['Production totale Espèces diverses  en T'].sum():,.0f}",
        f"{filtered_df['Superficies exploitées en horticulture en ha'].sum():,.0f}",
        f"{filtered_df['Production totale Horticole en T'].sum():,.0f}",
        f"{filtered_df['Superficies des Terres aménagées (ha)'].sum():,.0f}",
        f"{filtered_df['Nombre Ouvrages hydro-agricoles (digues de retenues, anti-sel, etc…)'].sum():,.0f}",
        f"{filtered_df['Nombre de Domaines agricoles communautaires (DAC)'].sum():,.0f}",
        f"{filtered_df['Superficie des Domaines agricoles communautaires (DAC) en ha'].sum():,.0f}",
        f"{filtered_df['Nombre de Fermes agricoles installées'].sum():,.0f}",
        f"{filtered_df['Superficies des Fermes agricoles installées en ha'].sum():,.0f}",
        f"{filtered_df['Nombre Infratructures de Stockage (magasins, seccos métalliques, banques céréalières villageoises, ect…)'].sum():,.0f}",
        f"{filtered_df['Nombre Unités de Transformation des Produits agricoles (moulins, batteuses, décortiqueuses, égreneuses, plateformes multifonctionnelles, etc…)'].sum():,.0f}",
        f"{filtered_df["Nombre d'Unités de matériels motorisés (tracteurs équipés d'accessoires, motoculteurs équipés, moissonneuses-batteuses, etc…)"].sum():,.0f}",
        f"{filtered_df["Nombre d'Unités d'équipements à traction animale (semoirs, houes, charrues, charrettes, etc…)"].sum():,.0f}",
        f"{filtered_df['Nombre de Sociétés coopératives agricoles agréées'].sum():,.0f}"
    )

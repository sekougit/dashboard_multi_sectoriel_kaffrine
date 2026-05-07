import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.data_loader import load_sector_data, get_all_sectors

dash.register_page(__name__, path="/graphiques")

# =========================
# LAYOUT
# =========================
layout = html.Div([

    html.H2(id="graph-title", className="mb-3"),

    dcc.Store(id="graph-store", storage_type="local"),
    dcc.Store(id="restore-done", data=False),

    dbc.Row([

        dbc.Col([
            html.Div("📊 Secteur", className="filter-title"),
            dcc.Dropdown(id="graph-secteur", clearable=False,
                         persistence=True, persistence_type="local")
        ], width=2),

        dbc.Col([
            html.Div("📅 Année", className="filter-title"),
            dcc.Dropdown(id="graph-annee", multi=True,
                         persistence=True, persistence_type="local")
        ], width=2),

        dbc.Col([
            html.Div("🌍 Région", className="filter-title"),
            dcc.Dropdown(id="graph-region", multi=True,
                         persistence=True, persistence_type="local")
        ], width=2),

        dbc.Col([
            html.Div("🏙️ Département", className="filter-title"),
            dcc.Dropdown(id="graph-departement", multi=True,
                         persistence=True, persistence_type="local")
        ], width=2),

        dbc.Col([
            html.Div("📍 Commune", className="filter-title"),
            dcc.Dropdown(id="graph-commune", multi=True,
                         persistence=True, persistence_type="local")
        ], width=2),

        dbc.Col([
            html.Div("📈 Indicateur", className="filter-title"),
            dcc.Dropdown(id="graph-indicateur", multi=True,
                         persistence=True, persistence_type="local")
        ], width=2),

    ], className="filters-bar"),

    html.Br(),

    html.Div(id="graphs-container")

])


# =========================
# TITRE DYNAMIQUE
# =========================
@callback(
    Output("graph-title", "children"),
    Input("graph-secteur", "value")
)
def update_title(secteur):
    return f"📊 Graphiques analytiques - {secteur}" if secteur else "📊 Graphiques analytiques"


# =========================
# LOAD DATA
# =========================
@callback(
    Output("graph-secteur", "options"),
    Input("graph-secteur", "id")
)
def load_secteurs(_):
    return [{"label": s, "value": s} for s in get_all_sectors()]


@callback(
    Output("graph-indicateur", "options"),
    Input("graph-secteur", "value")
)
def load_indicateurs(secteur):

    if not secteur:
        return []

    df = load_sector_data(secteur)
    exclude = ["annee", "region", "departement", "commune", "secteur"]

    return [{"label": c, "value": c} for c in df.columns if c not in exclude]


# =========================
# CASCADE FILTERS
# =========================
@callback(
    Output("graph-annee", "options"),
    Output("graph-region", "options"),
    Output("graph-departement", "options"),
    Output("graph-commune", "options"),

    Input("graph-secteur", "value"),
    Input("graph-region", "value"),
    Input("graph-departement", "value"),
)
def update_dropdowns(secteur, regions, departements):

    if not secteur:
        return [], [], [], []

    df = load_sector_data(secteur)

    annees = sorted(df["annee"].dropna().unique())
    regions_all = sorted(df["region"].dropna().unique())

    if regions:
        df = df[df["region"].isin(regions)]

    deps_all = sorted(df["departement"].dropna().unique())

    if departements:
        df = df[df["departement"].isin(departements)]

    communes = sorted(df["commune"].dropna().unique())

    return (
        [{"label": a, "value": a} for a in annees],
        [{"label": r, "value": r} for r in regions_all],
        [{"label": d, "value": d} for d in deps_all],
        [{"label": c, "value": c} for c in communes],
    )


# =========================
# SAVE FILTERS
# =========================
@callback(
    Output("graph-store", "data"),
    Input("graph-secteur", "value"),
    Input("graph-annee", "value"),
    Input("graph-region", "value"),
    Input("graph-departement", "value"),
    Input("graph-commune", "value"),
    Input("graph-indicateur", "value"),
    prevent_initial_call=True
)
def save_filters(s, a, r, d, c, i):
    return {
        "secteur": s,
        "annee": a,
        "region": r,
        "departement": d,
        "commune": c,
        "indicateur": i
    }


# =========================
# RESTORE FILTERS
# =========================
@callback(
    Output("graph-secteur", "value"),
    Output("graph-annee", "value"),
    Output("graph-region", "value"),
    Output("graph-departement", "value"),
    Output("graph-commune", "value"),
    Output("graph-indicateur", "value"),
    Output("restore-done", "data"),

    Input("graph-secteur", "options"),
    State("graph-store", "data"),
    State("restore-done", "data"),
)
def restore_filters(options, data, done):

    if done:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True

    if not data:
        return None, None, None, None, None, None, True

    return (
        data.get("secteur"),
        data.get("annee"),
        data.get("region"),
        data.get("departement"),
        data.get("commune"),
        data.get("indicateur"),
        True
    )


# =========================
# 🔥 GRAPHIQUES DYNAMIQUES
# =========================
@callback(
    Output("graphs-container", "children"),

    Input("graph-secteur", "value"),
    Input("graph-annee", "value"),
    Input("graph-region", "value"),
    Input("graph-departement", "value"),
    Input("graph-commune", "value"),
    Input("graph-indicateur", "value"),
)
def generate_graphs(
    secteur,
    annees,
    regions,
    departements,
    communes,
    indicateurs
):

    if not secteur:
        return "Sélectionnez un secteur"

    # =========================
    # LOAD DATA
    # =========================
    df = load_sector_data(secteur)

    # =========================
    # FILTRES
    # =========================
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

    # =========================
    # INDICATEURS
    # =========================
    exclude = [
        "annee",
        "region",
        "departement",
        "commune",
        "secteur"
    ]

    if not indicateurs:
        indicateurs = [
            c for c in df.columns
            if c not in exclude
        ]

    # =========================
    # DIMENSION
    # =========================
    dimension = "departement"

    if communes:
        dimension = "commune"

    elif departements:
        dimension = "departement"

    elif regions:
        dimension = "region"

    # =========================
    # COULEURS ANNÉES
    # =========================
    annees_uniques = sorted(
        df["annee"].astype(str).unique()
    )

    couleurs = [
        "#27ae60",
        "#3498db",
        "#9b59b6",
        "#f39c12",
        "#e74c3c",
        "#1abc9c",
        "#34495e",
        "#d35400",
        "#7f8c8d",
        "#2ecc71"
    ]

    color_map = {
        annee: couleurs[i % len(couleurs)]
        for i, annee in enumerate(annees_uniques)
    }

    # =========================
    # MODE STACK 100%
    # =========================
    stack_mode = len(annees_uniques) > 1

    # =========================
    # CONTAINER
    # =========================
    graphs = []

    # =========================
    # MULTI-GRAPHIQUES
    # =========================
    for ind in indicateurs:

        if ind not in df.columns:
            continue

        # =========================
        # AGRÉGATION
        # =========================
        grouped = df.groupby(
            [dimension, "annee"],
            as_index=False
        )[ind].sum()

        # =========================
        # 🔥 PROPORTIONS
        # =========================

        # UNE ANNÉE
        if not stack_mode:

            total = grouped[ind].sum()

            grouped["percent"] = (
                grouped[ind] / total
            ) * 100

        # PLUSIEURS ANNÉES
        else:

            grouped["percent"] = grouped.groupby(
                dimension
            )[ind].transform(
                lambda x: (x / x.sum()) * 100
            )

        # =========================
        # LABELS
        # =========================
        grouped["label"] = grouped.apply(
            lambda r:
            f"{r[ind]:,.0f}\n({r['percent']:.1f}%)",
            axis=1
        )

        # =========================
        # GRAPH
        # =========================
        fig = px.bar(

            grouped,

            x=dimension,
            y="percent",

            color=grouped["annee"].astype(str),

            color_discrete_map=color_map,

            barmode="stack" if stack_mode else "group",

            text="label",

            title=f"{ind} - Répartition (%) par {dimension}"
        )

        # =========================
        # STYLE BARRES
        # =========================
        fig.update_traces(

            textposition="inside",

            textangle=-90,

            insidetextanchor="middle",

            textfont=dict(
                size=10,
                color="white"
            ),

            marker_line_color="#145a32",
            marker_line_width=1
        )

        # =========================
        # LAYOUT
        # =========================
        fig.update_layout(

            template="plotly_white",

            title=dict(
                x=0.5,
                font=dict(size=13)
            ),

            yaxis=dict(
                title="Proportion (%)"
            ),

            xaxis=dict(
                title=dimension.capitalize()
            ),

            legend_title="Année",

            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            ),

            height=520
        )

        # =========================
        # MODE EMPILÉ 100%
        # =========================
        if stack_mode:

            fig.update_yaxes(
                range=[0, 100]
            )

        # =========================
        # CARD DESIGN
        # =========================
        graphs.append(

            dbc.Col(

                html.Div(

                    dcc.Graph(
                        figure=fig,
                        config={
                            "displayModeBar": False
                        }
                    ),

                    style={
                        "border": "2px solid #27ae60",
                        "borderRadius": "12px",
                        "padding": "10px",
                        "background": "white",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"
                    }

                ),

                width=6
            )
        )

    return dbc.Row(
        graphs,
        className="g-4"
    )
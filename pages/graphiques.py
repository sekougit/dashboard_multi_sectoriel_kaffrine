import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.data_loader import load_sector_data, get_all_sectors

dash.register_page(__name__, path="/graphiques")


# =========================================================
# LAYOUT
# =========================================================
layout = html.Div([

    html.H2(
        id="graph-title",
        className="mb-3"
    ),

    dcc.Store(
        id="graph-store",
        storage_type="local"
    ),

    dcc.Store(
        id="restore-done",
        data=False
    ),

    dbc.Row([

        dbc.Col([
            html.Div("📊 Secteur", className="filter-title"),

            dcc.Dropdown(
                id="graph-secteur",
                clearable=False,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div("📅 Année", className="filter-title"),

            dcc.Dropdown(
                id="graph-annee",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div("🌍 Région", className="filter-title"),

            dcc.Dropdown(
                id="graph-region",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div("🏙️ Département", className="filter-title"),

            dcc.Dropdown(
                id="graph-departement",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div("📍 Commune", className="filter-title"),

            dcc.Dropdown(
                id="graph-commune",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div("📈 Indicateur", className="filter-title"),

            dcc.Dropdown(
                id="graph-indicateur",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

    ], className="filters-bar g-2"),

    html.Br(),

    html.Div(id="graphs-container")

])


# =========================================================
# TITRE
# =========================================================
@callback(
    Output("graph-title", "children"),
    Input("graph-secteur", "value")
)
def update_title(secteur):

    if not secteur:
        return "📊 Graphiques analytiques"

    return f"📊 Graphiques analytiques - {secteur}"


# =========================================================
# LOAD SECTEURS
# =========================================================
@callback(
    Output("graph-secteur", "options"),
    Input("graph-secteur", "id")
)
def load_secteurs(_):

    return [
        {"label": s, "value": s}
        for s in get_all_sectors()
    ]


# =========================================================
# LOAD INDICATEURS
# =========================================================
@callback(
    Output("graph-indicateur", "options"),
    Input("graph-secteur", "value")
)
def load_indicateurs(secteur):

    if not secteur:
        return []

    df = load_sector_data(secteur)

    exclude = [
        "annee",
        "region",
        "departement",
        "commune",
        "secteur"
    ]

    return [
        {"label": c, "value": c}
        for c in df.columns
        if c not in exclude
    ]


# =========================================================
# CASCADE FILTERS
# =========================================================
@callback(
    Output("graph-annee", "options"),
    Output("graph-region", "options"),
    Output("graph-departement", "options"),
    Output("graph-commune", "options"),

    Input("graph-secteur", "value"),
    Input("graph-region", "value"),
    Input("graph-departement", "value"),
)
def update_dropdowns(
    secteur,
    regions,
    departements
):

    if not secteur:
        return [], [], [], []

    df = load_sector_data(secteur)

    annees = sorted(
        df["annee"].dropna().unique()
    )

    regions_all = sorted(
        df["region"].dropna().unique()
    )

    if regions:
        df = df[df["region"].isin(regions)]

    deps_all = sorted(
        df["departement"].dropna().unique()
    )

    if departements:
        df = df[df["departement"].isin(departements)]

    communes = sorted(
        df["commune"].dropna().unique()
    )

    return (
        [{"label": a, "value": a} for a in annees],
        [{"label": r, "value": r} for r in regions_all],
        [{"label": d, "value": d} for d in deps_all],
        [{"label": c, "value": c} for c in communes],
    )


# =========================================================
# SAVE FILTERS
# =========================================================
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
def save_filters(
    s,
    a,
    r,
    d,
    c,
    i
):

    return {
        "secteur": s,
        "annee": a,
        "region": r,
        "departement": d,
        "commune": c,
        "indicateur": i
    }


# =========================================================
# RESTORE FILTERS
# =========================================================
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
def restore_filters(
    options,
    data,
    done
):

    if done:

        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            True
        )

    if not data:

        return (
            None,
            None,
            None,
            None,
            None,
            None,
            True
        )

    return (
        data.get("secteur"),
        data.get("annee"),
        data.get("region"),
        data.get("departement"),
        data.get("commune"),
        data.get("indicateur"),
        True
    )


# =========================================================
# GRAPHIQUES
# =========================================================
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

    df = load_sector_data(secteur)

    # =====================================================
    # FILTRES
    # =====================================================
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

    # =====================================================
    # INDICATEURS
    # =====================================================
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

    # =====================================================
    # DIMENSION
    # =====================================================
    dimension = "departement"

    if communes:
        dimension = "commune"

    elif departements:
        dimension = "departement"

    elif regions:
        dimension = "region"

    # =====================================================
    # COULEURS
    # =====================================================
    annees_uniques = sorted(
        df["annee"].astype(str).unique()
    )

    palette = [
        "#27ae60",
        "#3498db",
        "#9b59b6",
        "#f39c12",
        "#e74c3c",
        "#1abc9c",
        "#34495e",
        "#d35400",
        "#2ecc71",
        "#8e44ad"
    ]

    color_map = {
        a: palette[i % len(palette)]
        for i, a in enumerate(annees_uniques)
    }

    # =====================================================
    # STACK MODE
    # =====================================================
    stack_mode = len(annees_uniques) > 1

    graphs = []

    # =====================================================
    # LOOP INDICATEURS
    # =====================================================
    for ind in indicateurs:

        if ind not in df.columns:
            continue

        grouped = df.groupby(
            [dimension, "annee"],
            as_index=False
        )[ind].sum()

        # =================================================
        # PROPORTIONS
        # =================================================
        if stack_mode:

            grouped["percent"] = grouped.groupby(
                dimension
            )[ind].transform(
                lambda x: x / x.sum() * 100
            )

        else:

            total = grouped[ind].sum()

            grouped["percent"] = (
                grouped[ind] / total
            ) * 100

        # =================================================
        # LABELS
        # =================================================
        grouped["label"] = grouped.apply(
            lambda r:
            f"{int(r[ind])}\n({r['percent']:.1f}%)",
            axis=1
        )

        # =================================================
        # FIGURE
        # =================================================
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

        # =================================================
        # STYLE BARRES
        # =================================================
        fig.update_traces(

            textposition="inside",

            textangle=-90,

            insidetextanchor="middle",

            textfont=dict(
                size=8,
                color="white"
            ),

            marker_line_width=0.8
        )

        # =================================================
        # LAYOUT
        # =================================================
        fig.update_layout(

            template="plotly_white",

            autosize=True,

            height=340,

            title=dict(
                text=f"{ind} - Répartition (%) par {dimension}",
                x=0.5,
                y=0.93,
                font=dict(
                    size=11
                )
            ),

            margin=dict(
                l=15,
                r=15,
                t=90,
                b=15
            ),

            # 🔥 LEGENDE EN HAUT A DROITE
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.12,
                xanchor="right",
                x=1,
                font=dict(size=9),
                title_text="",
                bgcolor="rgba(255,255,255,0.7)"
            ),

            xaxis=dict(
                title=dimension.capitalize(),
                tickfont=dict(size=9)
            ),

            yaxis=dict(
                title="Proportion (%)",
                tickfont=dict(size=9)
            )
        )

        # =================================================
        # STACK 100%
        # =================================================
        if stack_mode:
            fig.update_yaxes(range=[0, 100])

        # =================================================
        # CARD
        # =================================================
        graphs.append(

            dbc.Col(

                html.Div(

                    dcc.Graph(
                        figure=fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        },
                        style={
                            "height": "340px"
                        }
                    ),

                    style={
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "14px",
                        "padding": "8px",
                        "background": "white",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.05)"
                    }

                ),

                xs=12,
                sm=12,
                md=6,
                lg=6,
                xl=6
            )
        )

    return dbc.Row(
        graphs,
        className="g-3"
    )
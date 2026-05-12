import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import ALL
import pandas as pd
import io
import io
import zipfile
import base64
from dash import ctx

from utils.data_loader import (
    load_sector_data,
    get_all_sectors
)

dash.register_page(
    __name__,
    path="/graphiques"
)


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
    # =====================================================
    # DOWNLOAD
    # =====================================================
    dcc.Download(id="download-graph-excel"),

    dcc.Download(id="download-all-excel"),
    dcc.Download(id="download-all-images"),
    # =====================================================
    # FILTRES
    # =====================================================
    dbc.Row([

        dbc.Col([
            html.Div(
                "📊 Secteur",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-secteur",
                clearable=False,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div(
                "📅 Année",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-annee",
                multi=True,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div(
                "🌍 Région",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-region",
                multi=True,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div(
                "🏙️ Département",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-departement",
                multi=True,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div(
                "📍 Commune",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-commune",
                multi=True,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div(
                "📈 Indicateur",
                className="filter-title"
            ),

            dcc.Dropdown(
                id="graph-indicateur",
                multi=True,
                persistence=True,
                persistence_type="local"
            )

        ], xs=12, sm=6, md=4, lg=2),

    ], className="filters-bar g-2"),

    html.Br(),

    html.Div([

    dbc.Button(
        "📥 Télécharger Excel",
        id="download-all-excel-btn",
        color="success",
        className="me-2"
    ),

    dbc.Button(
        "🖼️ Télécharger Images",
        id="download-all-images-btn",
        color="primary"
    ),

], className="d-flex justify-content-end mb-3"),

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
        df = df[
            df["departement"].isin(departements)
        ]

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
# GENERATE GRAPHS
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

        return html.Div(
            "📊 Sélectionnez un secteur",
            className="text-center mt-4 fw-bold text-muted"
        )

    # =====================================================
    # LOAD DATA
    # =====================================================
    df = load_sector_data(secteur)

    # =====================================================
    # FILTRES
    # =====================================================
    if annees:
        df = df[df["annee"].isin(annees)]

    if regions:
        df = df[df["region"].isin(regions)]

    if departements:
        df = df[
            df["departement"].isin(departements)
        ]

    if communes:
        df = df[df["commune"].isin(communes)]

    # =====================================================
    # DATA VIDE
    # =====================================================
    if df.empty:

        return html.Div(
            "❌ Aucune donnée disponible",
            className="text-center mt-4 fw-bold text-danger"
        )

    # =====================================================
    # INDICATEURS
    # =====================================================
    if not indicateurs:

        return html.Div(
            "📈 Sélectionnez un ou plusieurs indicateurs",
            className="text-center mt-4 fw-bold text-muted"
        )

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
        # POURCENTAGES
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
            f"{int(r[ind]):,}\n({r['percent']:.1f}%)".replace(",", " "),
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
        # STYLE
        # =================================================
        fig.update_traces(

            textposition="inside",

            textangle=-90,

            insidetextanchor="middle",

            textfont=dict(
                size=8,
                color="white"
            ),

            marker_line_width=0.6
        )

        # =================================================
        # LAYOUT
        # =================================================
        fig.update_layout(

            template="plotly_white",

            autosize=True,

            height=330,

            title=dict(
                x=0.5,
                y=0.90,
                xanchor="center",
                font=dict(size=11)
            ),

            margin=dict(
                l=15,
                r=15,
                t=85,
                b=15
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.03,
                xanchor="right",
                x=1,
                font=dict(size=9),
                title_text=""
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

        if stack_mode:

            fig.update_yaxes(
                range=[0, 100]
            )

        # =================================================
        # CARD GRAPH
        # =================================================
        graphs.append(

            dbc.Col(

                html.Div([

                    # =================================
                    # BOUTON EXCEL
                    # =================================
                    html.Div([

                        dbc.Button(
                            "📥 Excel",
                            id={
                                "type": "excel-btn",
                                "index": ind
                            },
                            color="success",
                            size="sm"
                        )

                    ],
                    className="d-flex justify-content-end mb-2"),

                    # =================================
                    # GRAPH
                    # =================================
                    dcc.Graph(
                        id={
                            "type": "graph",
                            "index": ind
                        },
                        figure=fig,

                        # 🔥 IMPORTANT
                        config={
                            "displayModeBar": True,
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": ind
                            }
                        }
                    )

                ],

                style={
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "14px",
                    "padding": "8px",
                    "background": "white",
                    "boxShadow": "0 2px 6px rgba(0,0,0,0.05)"
                }),

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


@callback(
    Output("download-graph-excel", "data"),

    Input({
        "type": "excel-btn",
        "index": ALL
    }, "n_clicks"),

    State("graph-secteur", "value"),
    State("graph-annee", "value"),
    State("graph-region", "value"),
    State("graph-departement", "value"),
    State("graph-commune", "value"),

    prevent_initial_call=True
)
def export_excel(
    clicks,
    secteur,
    annees,
    regions,
    departements,
    communes
):

    from dash import ctx

    # =====================================================
    # AUCUN CLIC
    # =====================================================
    if not clicks:
        return dash.no_update

    # =====================================================
    # SI TOUS LES BOUTONS = NONE OU 0
    # =====================================================
    valid_click = any(
        c is not None and c > 0
        for c in clicks
    )

    if not valid_click:
        return dash.no_update

    # =====================================================
    # BOUTON CLIQUÉ
    # =====================================================
    if not ctx.triggered_id:
        return dash.no_update

    indicateur = ctx.triggered_id["index"]

@callback(
    Output("download-all-excel", "data"),
    Input("download-all-excel-btn", "n_clicks"),
    State("graph-secteur", "value"),
    State("graph-annee", "value"),
    State("graph-region", "value"),
    State("graph-departement", "value"),
    State("graph-commune", "value"),
    State("graph-indicateur", "value"),
    prevent_initial_call=True
)
def download_all_excel(
    n,
    secteur,
    annees,
    regions,
    departements,
    communes,
    indicateurs
):

    if not n:
        return dash.no_update

    import io
    import zipfile

    df = load_sector_data(secteur)

    if annees:
        df = df[df["annee"].isin(annees)]
    if regions:
        df = df[df["region"].isin(regions)]
    if departements:
        df = df[df["departement"].isin(departements)]
    if communes:
        df = df[df["commune"].isin(communes)]

    if not indicateurs:
        return dash.no_update

    dimension = "departement"
    if communes:
        dimension = "commune"
    elif departements:
        dimension = "departement"
    elif regions:
        dimension = "region"

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:

        for ind in indicateurs:

            if ind not in df.columns:
                continue

            grouped = df.groupby(
                [dimension, "annee"],
                as_index=False
            )[ind].sum()

            output = io.BytesIO()

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                grouped.to_excel(writer, index=False, sheet_name="data")

            zip_file.writestr(
                f"{ind}.xlsx",
                output.getvalue()
            )

    zip_buffer.seek(0)

    return dcc.send_bytes(
        zip_buffer.getvalue(),
        "tous_graphes_excel.zip"
    )


@callback(
    Output("download-all-images", "data"),
    Input("download-all-images-btn", "n_clicks"),
    State("graph-secteur", "value"),
    State("graph-annee", "value"),
    State("graph-region", "value"),
    State("graph-departement", "value"),
    State("graph-commune", "value"),
    State("graph-indicateur", "value"),
    prevent_initial_call=True
)
def download_all_images(
    n,
    secteur,
    annees,
    regions,
    departements,
    communes,
    indicateurs
):

    if not n:
        return dash.no_update

    import io
    import zipfile
    import plotly.express as px
    import plotly.io as pio

    df = load_sector_data(secteur)

    if annees:
        df = df[df["annee"].isin(annees)]
    if regions:
        df = df[df["region"].isin(regions)]
    if departements:
        df = df[df["departement"].isin(departements)]
    if communes:
        df = df[df["commune"].isin(communes)]

    if not indicateurs:
        return dash.no_update

    dimension = "departement"
    if communes:
        dimension = "commune"
    elif departements:
        dimension = "departement"
    elif regions:
        dimension = "region"

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:

        for ind in indicateurs:

            if ind not in df.columns:
                continue

            grouped = df.groupby(
                [dimension, "annee"],
                as_index=False
            )[ind].sum()

            fig = px.bar(
                grouped,
                x=dimension,
                y=ind,
                color="annee",
                title=ind
            )

            img = pio.to_image(fig, format="png", scale=2)

            zip_file.writestr(
                f"{ind}.png",
                img
            )

    zip_buffer.seek(0)

    return dcc.send_bytes(
        zip_buffer.getvalue(),
        "tous_graphes_images.zip"
    )
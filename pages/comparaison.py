import io
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    callback,
    ctx,
)
from dash.dependencies import ALL


from utils.data_loader import (
    get_all_sectors,
    load_sector_data,
    is_rate_indicator
)

dash.register_page(
    __name__,
    path="/comparaison",
    name="Comparaison"
)


# ==========================================================
# COULEURS (cohérent avec le thème vert du dashboard)
# ==========================================================
COULEUR_N1 = "#94a3b8"       # gris-bleu : année de référence
COULEUR_N = "#27ae60"        # vert marque : année courante
COULEUR_EVOLUTION = "#f39c12"  # ambre : évolution (glissée dans le même graphe)
COULEUR_HAUSSE = "#16a34a"
COULEUR_BAISSE = "#dc2626"
COULEUR_STABLE = "#64748b"


# ==========================================================
# CALCUL PARTAGÉ (KPI / Graphiques / Tableau utilisent tous ceci)
# ==========================================================
def compute_comparaison_data(
    df,
    secteur,
    annee1,
    annee2,
    regions,
    deps,
    communes,
    indicateurs
):
    """
    Calcule la comparaison N-1 vs N pour chaque zone géographique
    (au niveau de granularité impliqué par les filtres actifs) et
    chaque indicateur sélectionné.

    Retourne une liste de dicts :
        secteur, region, departement, commune, indicateur, type,
        valeur_n1, valeur_n, evolution_valeur, evolution_pct,
        tendance, vides_n1, vides_n
    """

    df1 = df[df.annee == annee1]
    df2 = df[df.annee == annee2]

    # Niveau de granularité selon les filtres actifs
    if communes:
        dimensions = ["region", "departement", "commune"]
    elif deps:
        dimensions = ["region", "departement"]
    elif regions:
        dimensions = ["region"]
    else:
        dimensions = ["region", "departement", "commune"]

    zones = df[dimensions].drop_duplicates()

    resultat = []

    for _, z in zones.iterrows():

        filtres = {col: z[col] for col in dimensions}

        g1 = df1.copy()
        g2 = df2.copy()

        for col, valeur in filtres.items():
            g1 = g1[g1[col] == valeur]
            g2 = g2[g2[col] == valeur]

        if g1.empty or g2.empty:
            continue

        r = z.get("region", "")
        d = z.get("departement", "")
        c = z.get("commune", "")

        for ind in indicateurs:

            if ind not in df.columns:
                continue

            typ = is_rate_indicator(ind)

            serie1 = g1[ind]
            serie2 = g2[ind]

            vides_n1 = int(serie1.isna().sum())
            vides_n = int(serie2.isna().sum())

            if typ == "taux":
                v1 = serie1.mean(skipna=True)
                v2 = serie2.mean(skipna=True)
            else:
                v1 = serie1.sum(skipna=True)
                v2 = serie2.sum(skipna=True)

            evo = v2 - v1

            evo_pct = None

            if pd.notna(v1) and v1 != 0:
                evo_pct = (evo / v1) * 100

            if pd.isna(evo_pct):
                tendance = ""
            elif evo_pct > 0:
                tendance = "▲ Hausse"
            elif evo_pct < 0:
                tendance = "▼ Baisse"
            else:
                tendance = "▬ Stable"

            resultat.append({
                "secteur": secteur,
                "region": r,
                "departement": d,
                "commune": c,
                "indicateur": ind,
                "type": typ,
                "valeur_n1": v1,
                "valeur_n": v2,
                "evolution_valeur": evo,
                "evolution_pct": evo_pct,
                "tendance": tendance,
                "vides_n1": vides_n1,
                "vides_n": vides_n,
            })

    return resultat


def format_nombre(x, typ):
    if pd.isna(x):
        return "—"
    if typ == "taux":
        return f"{x:.2f} %"
    return f"{x:,.2f}".replace(",", " ")


def zone_label(row, communes, deps):
    """Libellé Département : X | Commune : Y pour l'en-tête d'un bloc KPI."""
    if communes:
        return f"Département : {row['departement']}    Commune : {row['commune']}"
    if deps:
        return f"Département : {row['departement']}    Commune : Toutes"
    return f"Région : {row['region']}    Département : Toutes"


def zone_axis_label(row, communes, deps):
    """Libellé court pour l'axe X des graphiques."""
    if communes:
        return row["commune"]
    if deps:
        return row["departement"]
    return row["region"]


# ==========================================================
# LAYOUT
# ==========================================================
layout = html.Div([

    dcc.Store(
        id="comparaison-store",
        storage_type="local"
    ),

    dcc.Store(
        id="comparaison-restore-done",
        data=False
    ),

    # =====================================================
    # BARRE STICKY
    # =====================================================
    html.Div([

        html.H2(
            id="comp-dynamic-title",
            className="graph-title"
        ),

        dbc.Row([

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-grid-fill me-1"),
                    " Secteur"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-secteur",
                    clearable=False,
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-calendar-minus me-1"),
                    " Année N-1"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-annee1",
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-calendar-plus me-1"),
                    " Année N"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-annee2",
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-globe2 me-1"),
                    " Région"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-region",
                    multi=True,
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-buildings-fill me-1"),
                    " Département"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-departement",
                    multi=True,
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

            dbc.Col([

                html.Div([
                    html.I(className="bi bi-geo-alt-fill me-1"),
                    " Commune"
                ], className="filter-title"),

                dcc.Dropdown(
                    id="comp-commune",
                    multi=True,
                    persistence=True,
                    persistence_type="local"
                )

            ], xs=12, sm=6, md=4, lg=2),

        ], className="g-2 mt-2"),

dbc.Row([

    dbc.Col([

        html.Div([
            html.I(className="bi bi-bar-chart-line-fill me-1"),
            " Indicateurs"
        ], className="filter-title"),

        dcc.Dropdown(
            id="comp-indicateurs",
            multi=True,
            persistence=True,
            persistence_type="local"
        )

    ], width=10),


    dbc.Col([

        dbc.Button(
            [
                html.I(className="bi bi-arrow-counterclockwise me-2"),
                "Réinitialiser"
            ],
            id="reset-comparaison-btn",
            color="warning",
            outline=True,
            className="mt-4"
        )

    ], width=2)


], className="g-1 mt-2 align-items-center")

    ], className="graph-toolbar"),

    # =================================================
    # BARRE MODE + EXPORT (hors du toolbar sticky,
    # pour ne pas grignoter la place des graphiques/KPI/tableau)
    # =================================================
    dbc.Row([

        dbc.Col([

            dcc.Store(id="comp-mode", data="kpi"),

            dbc.ButtonGroup([

                dbc.Button(
                    [html.I(className="bi bi-speedometer2 me-2"), "KPI"],
                    id={"type": "comp-mode-btn", "mode": "kpi"},
                    color="success",
                    outline=True,
                    active=True,
                ),

                dbc.Button(
                    [html.I(className="bi bi-bar-chart-line-fill me-2"), "Graphiques"],
                    id={"type": "comp-mode-btn", "mode": "graphiques"},
                    color="success",
                    outline=True,
                ),

                dbc.Button(
                    [html.I(className="bi bi-table me-2"), "Tableau"],
                    id={"type": "comp-mode-btn", "mode": "tableau"},
                    color="success",
                    outline=True,
                ),

            ]),

        ], width="auto"),

        dbc.Col([

            dbc.Button(
                [
                    html.I(className="bi bi-download me-2"),
                    "Exporter Excel"
                ],
                id="export-comparaison-btn",
                color="success"
            ),

        ], width="auto", className="ms-auto"),

    ], className="g-2 my-3 align-items-center"),

    html.Br(),

    dcc.Download(id="download-comparaison"),
    dcc.Download(id="download-comp-graph-excel"),

    # =====================================================
    # MODE KPI
    # =====================================================
    html.Div(
        id="comparaison-kpi-container"
    ),

    # =====================================================
    # MODE GRAPHIQUES
    # =====================================================
    html.Div(
        id="comparaison-graphs-container"
    ),

    # =====================================================
    # MODE TABLEAU
    # =====================================================
    html.Div(

        dag.AgGrid(

            id="comparaison-grid",

            columnDefs=[],

            rowData=[],

            defaultColDef={
                "sortable": True,
                "filter": True,
                "resizable": True,
                "floatingFilter": True,
            },

            dashGridOptions={
                "pagination": True,
                "paginationPageSize": 20,
                "animateRows": True,
            },

            className="ag-theme-alpine",

            style={
                "height": "700px",
                "width": "100%"
            }

        ),

        id="comparaison-table-container"

    )

])


# ==========================================================
# CHARGEMENT DES SECTEURS
# ==========================================================
@callback(
    Output("comp-secteur", "options"),
    Input("comp-secteur", "id")
)
def load_secteurs(_):

    return [
        {"label": s, "value": s}
        for s in get_all_sectors()
    ]


@callback(
    Output("comp-dynamic-title", "children"),
    Input("comp-secteur", "value")
)
def update_title(secteur):

    if not secteur:
        return html.Div(
            "Comparaison indicateurs",
            className="page-title"
        )

    return html.Div([
        html.Span(
            "Comparaison indicateurs",
            className="page-title-main"
        ),
        html.Span(
            f" • {secteur}",
            className="page-title-sector"
        )
    ])


# =========================================================
# SÉLECTEUR DE MODE (boutons à icônes)
# =========================================================
@callback(
    Output("comp-mode", "data"),
    Output({"type": "comp-mode-btn", "mode": ALL}, "active"),

    Input({"type": "comp-mode-btn", "mode": ALL}, "n_clicks"),
    State({"type": "comp-mode-btn", "mode": ALL}, "id"),

    prevent_initial_call=True
)
def switch_mode(n_clicks_list, ids):

    triggered = ctx.triggered_id

    if not triggered:
        return dash.no_update, [dash.no_update] * len(ids)

    mode = triggered["mode"]

    return mode, [id_["mode"] == mode for id_ in ids]


# =========================================================
# AFFICHAGE / MASQUAGE SELON LE MODE CHOISI
# =========================================================
@callback(
    Output("comparaison-kpi-container", "style"),
    Output("comparaison-graphs-container", "style"),
    Output("comparaison-table-container", "style"),
    Input("comp-mode", "data")
)
def toggle_mode(mode):

    hidden = {"display": "none"}
    visible = {"display": "block"}

    return (
        visible if mode == "kpi" else hidden,
        visible if mode == "graphiques" else hidden,
        visible if mode == "tableau" else hidden,
    )


# =========================================================
# CASCADE FILTERS
# =========================================================
@callback(

    Output("comp-annee1", "options"),
    Output("comp-annee2", "options"),
    Output("comp-region", "options"),
    Output("comp-departement", "options"),
    Output("comp-commune", "options"),
    Output("comp-indicateurs", "options"),

    Input("comp-secteur", "value"),
    Input("comp-region", "value"),
    Input("comp-departement", "value"),

)
def update_dropdowns(
    secteur,
    regions,
    departements
):

    if not secteur:
        return [], [], [], [], [], []

    df = load_sector_data(secteur)

    annees = sorted(df["annee"].dropna().unique())

    regions_all = sorted(df["region"].dropna().unique())

    if regions:
        df = df[df["region"].isin(regions)]

    deps_all = sorted(df["departement"].dropna().unique())

    if departements:
        df = df[df["departement"].isin(departements)]

    communes = sorted(df["commune"].dropna().unique())

    indicateurs = [

        c

        for c in df.columns

        if c not in [

            "secteur",
            "annee",
            "region",
            "departement",
            "commune"

        ]

    ]

    return (

        [{"label": a, "value": a} for a in annees],
        [{"label": a, "value": a} for a in annees],

        [{"label": r, "value": r} for r in regions_all],

        [{"label": d, "value": d} for d in deps_all],

        [{"label": c, "value": c} for c in communes],

        [{"label": i, "value": i} for i in indicateurs],

    )

from dash import ctx


# =========================================================
# RESTORE + RESET FILTERS
# =========================================================

@callback(

    Output("comp-secteur", "value"),
    Output("comp-annee1", "value"),
    Output("comp-annee2", "value"),
    Output("comp-region", "value"),
    Output("comp-departement", "value"),
    Output("comp-commune", "value"),
    Output("comp-indicateurs", "value"),
    Output("comparaison-restore-done", "data"),


    Input("comp-secteur", "options"),
    Input("reset-comparaison-btn", "n_clicks"),


    State("comparaison-store", "data"),
    State("comparaison-restore-done", "data"),


    prevent_initial_call=False
)
def restore_or_reset(
    options,
    reset_click,
    data,
    done
):

    trigger = ctx.triggered_id


    # ===============================
    # RESET
    # ===============================

    if trigger == "reset-comparaison-btn":

        return (

            dash.no_update,  # secteur reste

            None,            # année N-1
            None,            # année N

            None,            # région
            None,            # département
            None,            # commune

            None,            # indicateurs

            True
        )


    # ===============================
    # RESTAURATION
    # ===============================

    if trigger == "comp-secteur":

        if not options:
            raise dash.exceptions.PreventUpdate


        if not data:

            return (

                None,
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

            data.get("annee1"),

            data.get("annee2"),

            data.get("region"),

            data.get("departement"),

            data.get("commune"),

            data.get("indicateurs"),

            True
        )


    raise dash.exceptions.PreventUpdate

# =========================================================
# SAVE FILTERS
# =========================================================
@callback(
    Output("comparaison-store", "data"),

    Input("comp-secteur", "value"),
    Input("comp-annee1", "value"),
    Input("comp-annee2", "value"),
    Input("comp-region", "value"),
    Input("comp-departement", "value"),
    Input("comp-commune", "value"),
    Input("comp-indicateurs", "value"),

    prevent_initial_call=True
)
def save_filters(
    secteur,
    annee1,
    annee2,
    region,
    departement,
    commune,
    indicateurs
):

    return {

        "secteur": secteur,

        "annee1": annee1,

        "annee2": annee2,

        "region": region,

        "departement": departement,

        "commune": commune,

        "indicateurs": indicateurs

    }

# # =========================================================
# # RESTORE FILTERS
# # =========================================================
# @callback(

#     Output("comp-secteur", "value"),
#     Output("comp-annee1", "value"),
#     Output("comp-annee2", "value"),
#     Output("comp-region", "value"),
#     Output("comp-departement", "value"),
#     Output("comp-commune", "value"),
#     Output("comp-indicateurs", "value"),
#     Output("comparaison-restore-done", "data"),

#     Input("comp-secteur", "options"),

#     State("comparaison-store", "data"),
#     State("comparaison-restore-done", "data")

# )
# def restore_filters(
#     options,
#     data,
#     done
# ):

#     if done:

#         return (

#             dash.no_update,
#             dash.no_update,
#             dash.no_update,
#             dash.no_update,
#             dash.no_update,
#             dash.no_update,
#             dash.no_update,
#             True

#         )

#     if not data:

#         return (

#             None,
#             None,
#             None,
#             None,
#             None,
#             None,
#             None,
#             True

#         )

#     return (

#         data.get("secteur"),

#         data.get("annee1"),

#         data.get("annee2"),

#         data.get("region"),

#         data.get("departement"),

#         data.get("commune"),

#         data.get("indicateurs"),

#         True

#     )


def _get_base_data(secteur, annee1, annee2, regions, deps, communes, indicateurs):
    """Charge + filtre les données, retourne (df, ok). ok=False si rien à calculer."""

    if not secteur or not annee1 or not annee2 or not indicateurs:
        return None, False

    df = load_sector_data(secteur)

    if regions:
        df = df[df.region.isin(regions)]

    if deps:
        df = df[df.departement.isin(deps)]

    if communes:
        df = df[df.commune.isin(communes)]

    if df.empty:
        return None, False

    return df, True


# ==========================================================
# MODE KPI
# ==========================================================
@callback(

    Output("comparaison-kpi-container", "children"),

    Input("comp-secteur", "value"),
    Input("comp-annee1", "value"),
    Input("comp-annee2", "value"),
    Input("comp-region", "value"),
    Input("comp-departement", "value"),
    Input("comp-commune", "value"),
    Input("comp-indicateurs", "value"),

)
def render_kpi_mode(secteur, annee1, annee2, regions, deps, communes, indicateurs):

    df, ok = _get_base_data(secteur, annee1, annee2, regions, deps, communes, indicateurs)

    if not ok:
        return html.Div(
            "Sélectionnez un secteur, deux années et au moins un indicateur",
            className="text-center mt-4 fw-bold text-muted"
        )

    data = compute_comparaison_data(
        df, secteur, annee1, annee2, regions, deps, communes, indicateurs
    )

    if not data:
        return html.Div(
            "Aucune donnée disponible pour cette combinaison de filtres",
            className="text-center mt-4 fw-bold text-danger"
        )

    resultat_df = pd.DataFrame(data)

    zone_cols = ["region", "departement", "commune"]

    blocks = []

    for _, zone_key in resultat_df[zone_cols].drop_duplicates().iterrows():

        sous_df = resultat_df[
            (resultat_df.region == zone_key["region"]) &
            (resultat_df.departement == zone_key["departement"]) &
            (resultat_df.commune == zone_key["commune"])
        ]

        cards = []

        for _, row in sous_df.iterrows():

            couleur_evo = (
                "text-success" if row["evolution_valeur"] > 0
                else "text-danger" if row["evolution_valeur"] < 0
                else "text-muted"
            )

            cards.append(

                dbc.Col(

                    html.Div([

                        html.Div(
                            row["indicateur"].upper(),
                            className="kpi-title"
                        ),

                        html.Div(
                            f"{'+' if row['evolution_valeur'] > 0 else ''}"
                            f"{format_nombre(row['evolution_valeur'], row['type'])}",
                            className=f"kpi-value {couleur_evo}"
                        ),

                        html.Div(
                            row["tendance"] + (
                                f"  ({row['evolution_pct']:.2f} %)"
                                if pd.notna(row["evolution_pct"]) else ""
                            ),
                            className="kpi-sub"
                        ),

                        html.Div(
                            f"N-1 ({annee1}) : {format_nombre(row['valeur_n1'], row['type'])}"
                            f"   →   N ({annee2}) : {format_nombre(row['valeur_n'], row['type'])}",
                            className="kpi-context"
                        ),

                        html.Div(
                            f"Type : {'Taux / Ratio' if row['type'] == 'taux' else 'Valeur brute'}"
                            f"   •   Vides N-1 : {row['vides_n1']}   •   Vides N : {row['vides_n']}",
                            className="kpi-context"
                        ),

                    ], className="kpi-card"),

                    xs=12, sm=6, md=4, lg=3, xl=3

                )

            )

        blocks.append(

            html.Div([

                html.H5(
                    zone_label(zone_key, communes, deps),
                    className="zone-title"
                ),

                dbc.Row(cards, className="g-3")

            ], className="zone-block")

        )

    return blocks


# ==========================================================
# MODE GRAPHIQUES
# ==========================================================
@callback(

    Output("comparaison-graphs-container", "children"),

    Input("comp-secteur", "value"),
    Input("comp-annee1", "value"),
    Input("comp-annee2", "value"),
    Input("comp-region", "value"),
    Input("comp-departement", "value"),
    Input("comp-commune", "value"),
    Input("comp-indicateurs", "value"),

)
def render_graph_mode(secteur, annee1, annee2, regions, deps, communes, indicateurs):

    df, ok = _get_base_data(secteur, annee1, annee2, regions, deps, communes, indicateurs)

    if not ok:
        return html.Div(
            "Sélectionnez un secteur, deux années et au moins un indicateur",
            className="text-center mt-4 fw-bold text-muted"
        )

    data = compute_comparaison_data(
        df, secteur, annee1, annee2, regions, deps, communes, indicateurs
    )

    if not data:
        return html.Div(
            "Aucune donnée disponible pour cette combinaison de filtres",
            className="text-center mt-4 fw-bold text-danger"
        )

    resultat_df = pd.DataFrame(data)

    resultat_df["zone"] = resultat_df.apply(
        lambda row: zone_axis_label(row, communes, deps), axis=1
    )

    niveau_label = "Commune" if communes else ("Département" if deps else "Région")

    graphs = []

    for ind in indicateurs:

        sous_df = resultat_df[resultat_df.indicateur == ind]

        if sous_df.empty:
            continue

        typ = sous_df["type"].iloc[0]

        # ---- Un seul graphique fusionné : N-1, N, Évolution côte à côte ----
        lignes = []

        for _, row in sous_df.iterrows():

            lignes.append({
                "zone": row["zone"],
                "Série": str(annee1),
                "Valeur": row["valeur_n1"],
                "Vides": row["vides_n1"],
            })

            lignes.append({
                "zone": row["zone"],
                "Série": str(annee2),
                "Valeur": row["valeur_n"],
                "Vides": row["vides_n"],
            })

            lignes.append({
                "zone": row["zone"],
                "Série": "Évolution",
                "Valeur": row["evolution_valeur"],
                "Vides": row["vides_n1"] + row["vides_n"],
            })

        plot_df = pd.DataFrame(lignes)

        fig = px.bar(
            plot_df,
            x="zone",
            y="Valeur",
            color="Série",
            barmode="group",
            color_discrete_map={
                str(annee1): COULEUR_N1,
                str(annee2): COULEUR_N,
                "Évolution": COULEUR_EVOLUTION,
            },
            custom_data=["Série", "Vides"],
            text_auto=".2s"
        )

        fig.update_traces(
            hovertemplate=(
                f"<b>{niveau_label} : %{{x}}</b><br>"
                "Année : %{customdata[0]}<br>"
                "Valeur : %{y:,.2f}<br>"
                "Vides : %{customdata[1]}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            template="plotly_white",
            height=340,
            title=dict(
                text=f"<b>{ind}</b> — {'Moyenne' if typ == 'taux' else 'Somme'}",
                x=0.5, y=0.90, xanchor="center", font=dict(size=12)
            ),
            margin=dict(l=15, r=15, t=95, b=15),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=9), title_text=""
            ),
            xaxis=dict(title=niveau_label, tickfont=dict(size=9)),
            yaxis=dict(
                title="Taux moyen (%)" if typ == "taux" else "Valeur",
                tickfont=dict(size=9)
            )
        )

        graphs.append(

            dbc.Col(

                html.Div([

                    # =================================
                    # BOUTON EXCEL (même motif que graphiques.py)
                    # =================================
                    html.Div([

                        dbc.Button(
                            [
                                html.I(className="bi bi-file-earmark-excel-fill me-2"),
                                "Excel"
                            ],
                            id={
                                "type": "comp-excel-btn",
                                "index": ind
                            },
                            color="success",
                            size="sm"
                        )

                    ], className="d-flex justify-content-end mb-2"),

                    dcc.Graph(
                        id={
                            "type": "comp-graph",
                            "index": ind
                        },
                        figure=fig,
                        config={
                            "displayModeBar": True,
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": ind
                            }
                        }
                    ),

                ], style={
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "14px",
                    "padding": "8px",
                    "background": "white",
                    "boxShadow": "0 2px 6px rgba(0,0,0,0.05)"
                }),

                xs=12, sm=12, md=6, lg=6, xl=6

            )

        )

    return dbc.Row(graphs, className="g-3")


# ==========================================================
# EXPORT EXCEL PAR GRAPHIQUE (mode Graphiques)
# ==========================================================
@callback(

    Output("download-comp-graph-excel", "data"),

    Input({"type": "comp-excel-btn", "index": ALL}, "n_clicks"),

    State("comp-secteur", "value"),
    State("comp-annee1", "value"),
    State("comp-annee2", "value"),
    State("comp-region", "value"),
    State("comp-departement", "value"),
    State("comp-commune", "value"),

    prevent_initial_call=True
)
def export_comp_graph_excel(
    clicks,
    secteur,
    annee1,
    annee2,
    regions,
    deps,
    communes
):

    if not clicks or not any(clicks):
        return dash.no_update

    if not ctx.triggered_id:
        return dash.no_update

    indicateur = ctx.triggered_id["index"]

    df, ok = _get_base_data(
        secteur, annee1, annee2, regions, deps, communes, [indicateur]
    )

    if not ok:
        return dash.no_update

    data = compute_comparaison_data(
        df, secteur, annee1, annee2, regions, deps, communes, [indicateur]
    )

    if not data:
        return dash.no_update

    export_df = pd.DataFrame(data)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="Données")

    output.seek(0)

    return dcc.send_bytes(
        output.getvalue(),
        f"{indicateur}_comparaison.xlsx"
    )


# ==========================================================
# MODE TABLEAU
# ==========================================================
@callback(

    Output("comparaison-grid", "columnDefs"),
    Output("comparaison-grid", "rowData"),

    Input("comp-secteur", "value"),
    Input("comp-annee1", "value"),
    Input("comp-annee2", "value"),
    Input("comp-region", "value"),
    Input("comp-departement", "value"),
    Input("comp-commune", "value"),
    Input("comp-indicateurs", "value")

)
def render_table_mode(secteur, annee1, annee2, regions, deps, communes, indicateurs):

    df, ok = _get_base_data(secteur, annee1, annee2, regions, deps, communes, indicateurs)

    if not ok:
        return [], []

    data = compute_comparaison_data(
        df, secteur, annee1, annee2, regions, deps, communes, indicateurs
    )

    resultat = [
        {
            "Secteur": row["secteur"],
            "Région": row["region"],
            "Département": row["departement"],
            "Commune": row["commune"],
            "Indicateur": row["indicateur"],
            str(annee1): None if pd.isna(row["valeur_n1"]) else round(row["valeur_n1"], 2),
            str(annee2): None if pd.isna(row["valeur_n"]) else round(row["valeur_n"], 2),
            "Evolution valeur": None if pd.isna(row["evolution_valeur"]) else round(row["evolution_valeur"], 2),
            "Evolution %": None if row["evolution_pct"] is None or pd.isna(row["evolution_pct"]) else round(row["evolution_pct"], 2),
            "Tendance": row["tendance"],
        }
        for row in data
    ]

    colonnes = [
        {"field": "Secteur", "pinned": "left"}
    ]

    if communes:
        colonnes.extend([
            {"field": "Région"},
            {"field": "Département"},
            {"field": "Commune"}
        ])
    elif deps:
        colonnes.extend([
            {"field": "Région"},
            {"field": "Département"}
        ])
    elif regions:
        colonnes.append({"field": "Région"})
    else:
        colonnes.extend([
            {"field": "Région"},
            {"field": "Département"},
            {"field": "Commune"}
        ])

    colonnes.append({"field": "Indicateur"})

    style_evolution = {
        "styleConditions": [
            {
                "condition": "params.value > 0",
                "style": {"color": "green", "fontWeight": "bold"}
            },
            {
                "condition": "params.value < 0",
                "style": {"color": "red", "fontWeight": "bold"}
            }
        ]
    }

    colonnes.extend([

        {"field": str(annee1), "type": "numericColumn"},
        {"field": str(annee2), "type": "numericColumn"},

        {
            "field": "Evolution valeur",
            "type": "numericColumn",
            "cellStyle": style_evolution
        },

        {
            "field": "Evolution %",
            "type": "numericColumn",
            "cellStyle": style_evolution
        },

        {"field": "Tendance", "pinned": "right"}

    ])

    return colonnes, resultat


@callback(

    Output("download-comparaison", "data"),

    Input("export-comparaison-btn", "n_clicks"),

    State("comparaison-grid", "rowData"),

    prevent_initial_call=True

)
def export_excel(n, data):

    if not n:
        return dash.no_update

    if not data:
        return dash.no_update

    df = pd.DataFrame(data)

    return dcc.send_data_frame(
        df.to_excel,
        "Comparaison.xlsx",
        index=False
    )
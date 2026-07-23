import io
import dash
import pandas as pd

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    callback,
    no_update
)

import dash_bootstrap_components as dbc

from utils.data_loader import (
    get_all_sectors,
    load_sector_data,
    compute_kpi,
    format_value,
    count_missing
)



dash.register_page(__name__, path="/secteurs")

layout = html.Div([

# html.H2(
#     id="dynamic-title",
#     className="mb-3"
# ),

dcc.Download(id="download-kpi"),

dcc.Store(
    id="restore-done",
    data=False
),

dcc.Store(
    id="filters-store",
    storage_type="local"
),
# =====================================================
# BARRE STICKY
# =====================================================
html.Div([

    html.H2(
    id="dynamic-title",
    className="graph-title"
),

    # html.Div(
    #     id="filters-summary",
    #     className="filters-summary mb-3"
    # ),

    dbc.Row([

        dbc.Col([
            html.Div([
                    html.I(className="bi bi-grid-fill me-1"),
                    "Secteur"
                ], className="filter-title"),
            dcc.Dropdown(
                id="secteur-dd",
                clearable=False,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div([
                html.I(className="bi bi-calendar3 me-1"),
                "Année"
            ], className="filter-title"),
            dcc.Dropdown(
                id="annee-dd",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div([
                    html.I(className="bi bi-globe2 me-1"),
                    "Région"
                ], className="filter-title"),
            dcc.Dropdown(
                id="region-dd",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
                html.Div([
                    html.I(className="bi bi-buildings-fill me-1"),
                    "Département"
                ], className="filter-title"),
            dcc.Dropdown(
                id="departement-dd",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
                            html.Div([
                    html.I(className="bi bi-geo-alt-fill me-1"),
                    "Commune"
                ], className="filter-title"),
            dcc.Dropdown(
                id="commune-dd",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

        dbc.Col([
            html.Div([
                    html.I(className="bi bi-bar-chart-line-fill me-1"),
                    "Indicateur"
                ], className="filter-title"),
            dcc.Dropdown(
                id="indicateur-dd",
                multi=True,
                persistence=True,
                persistence_type="local"
            )
        ], xs=12, sm=6, md=4, lg=2),

    ], className="g-2"),

html.Div(
    [

        dbc.Button(
            [
                html.I(className="bi bi-arrow-counterclockwise me-2"),
                "éffacer filtres"
            ],
            id="reset-filters-btn-secteurs",
            color="warning",
            outline=True
        ),


        dbc.Button(
            [
                html.I(className="bi bi-download me-2"),
                "Télécharger KPI"
            ],
            id="download-kpi-btn",
            color="success"
        )

    ],

    className="d-flex justify-content-end gap-2 mt-3"

)
],
className="graph-toolbar"
),



# =====================================================
# KPI
# =====================================================
html.Div(
    id="kpi-container"
)
])

@callback(
    Output("secteur-dd", "options"),
    Input("secteur-dd", "id")
)
def load_secteurs(_):
    return [{"label": s, "value": s} for s in get_all_sectors()]

@callback(
    Output("dynamic-title", "children"),
    Input("secteur-dd", "value")
)
def update_title(secteur):

    if not secteur:
        return html.Div(
            "Indicateurs sectoriels",
            className="page-title"
        )

    return html.Div([
        html.Span(
            "Indicateurs sectoriels",
            className="page-title-main"
        ),
        html.Span(
            f" • {secteur}",
            className="page-title-sector"
        )
    ])



@callback(
    Output("indicateur-dd", "options"),
    Input("secteur-dd", "value")
)
def load_indicateurs(secteur):

    if not secteur:
        return []

    df = load_sector_data(secteur)

    exclude = ["annee", "region", "departement", "commune", "secteur"]

    cols = [c for c in df.columns if c not in exclude]

    return [{"label": c, "value": c} for c in cols]

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
        return no_update, no_update, no_update, no_update

    df = load_sector_data(secteur)

    # REGION
    regions_all = sorted(df["region"].dropna().unique())

    if regions:
        df = df[df["region"].isin(regions)]

    # DEPARTEMENT
    deps_all = sorted(df["departement"].dropna().unique())

    if departements:
        df = df[df["departement"].isin(departements)]

    # COMMUNE
    communes = sorted(df["commune"].dropna().unique())

    # ANNEE
    annees = sorted(df["annee"].dropna().unique())

    return (
        [{"label": i, "value": i} for i in annees],
        [{"label": i, "value": i} for i in regions_all],
        [{"label": i, "value": i} for i in deps_all],
        [{"label": i, "value": i} for i in communes],
    )

# @callback(
#     Output("filters-summary", "children"),

#     Input("annee-dd", "value"),
#     Input("region-dd", "value"),
#     Input("departement-dd", "value"),
#     Input("commune-dd", "value"),
# )
# def show_selected(annee, region, dep, com):

#     def format(label, value):
#         if not value:
#             return None

#         if isinstance(value, list):
#             value = ", ".join(map(str, value))

#         return html.Span(f"{label}: {value}", className="filter-badge")

#     return html.Div([
#         format("📅 Année", annee),
#         format("🌍 Région", region),
#         format("🏙️ Département", dep),
#         format("📍 Commune", com),
#     ], className="d-flex gap-2 flex-wrap")

from dash import ctx


# =====================================================
# RESTAURATION + RESET FILTRES
# =====================================================

@callback(
    Output("secteur-dd","value"),
    Output("annee-dd","value"),
    Output("region-dd","value"),
    Output("departement-dd","value"),
    Output("commune-dd","value"),
    Output("indicateur-dd","value"),

    Input("secteur-dd","options"),
    Input("reset-filters-btn-secteurs","n_clicks"),

    State("filters-store","data"),

    prevent_initial_call=False
)
def restore_or_reset(options, reset_clicks, data):

    trigger = ctx.triggered_id


    # ==========================
    # CAS RESET
    # ==========================
    if trigger == "reset-filters-btn-secteurs":

        return (
            dash.no_update,  # conserver secteur
            None,            # année
            None,            # région
            None,            # département
            None,            # commune
            None             # indicateur
        )


    # ==========================
    # CAS RESTAURATION
    # ==========================
    if trigger == "secteur-dd":

        if not options:
            raise dash.exceptions.PreventUpdate


        if not data:
            return (
                None,
                None,
                None,
                None,
                None,
                None
            )


        return (
            data.get("secteur"),
            data.get("annee"),
            data.get("region"),
            data.get("departement"),
            data.get("commune"),
            data.get("indicateur")
        )


    raise dash.exceptions.PreventUpdate


# ,allow_duplicate=True
@callback(
    Output("filters-store", "data"),

    Input("secteur-dd", "value"),
    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
    Input("indicateur-dd", "value"),
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

# @callback(
#     Output("secteur-dd", "value"),
#     Output("annee-dd", "value"),
#     Output("region-dd", "value"),
#     Output("departement-dd", "value"),
#     Output("commune-dd", "value"),
#     Output("indicateur-dd", "value"),

#     Input("filters-store", "data"),
# )
# def restore_filters(data):

#     if not data:
#         return None, None, None, None, None, None

#     return (
#         data.get("secteur"),
#         data.get("annee"),
#         data.get("region"),
#         data.get("departement"),
#         data.get("commune"),
#         data.get("indicateur"),
#     )

from dash import ctx

# =====================================================
# LIBELLÉ ZONE (Département : X    Commune : Y)
# =====================================================
def format_zone_label(data):

    deps = sorted(data["departement"].dropna().unique())
    coms = sorted(data["commune"].dropna().unique())

    departement = deps[0] if len(deps) == 1 else " / ".join(deps)
    commune = coms[0] if len(coms) == 1 else "Toutes"

    return f"Département : {departement} | Commune : {commune}"


@callback(
    Output("kpi-container", "children"),
    Input("secteur-dd", "value"),
    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
    Input("indicateur-dd", "value"),
)
def update_kpis(
    secteur,
    annees,
    regions,
    departements,
    communes,
    indicateurs
):

    # =========================
    # SECTEUR
    # =========================
    if not secteur:
        return html.Div(
            "Sélectionnez un secteur",
            className="text-center mt-4 fw-bold text-muted"
        )

    # =========================
    # DONNEES
    # =========================
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
        return html.Div(
            "Aucune donnée disponible",
            className="text-center mt-4 fw-bold text-danger"
        )

    if not indicateurs:
        return html.Div(
            "Veuillez sélectionnez un ou plusieurs indicateurs",
            className="text-center mt-4 fw-bold text-muted"
        )

    # =========================
    # DIMENSION DE COMPARAISON
    # =========================
    compare_dims = []

    if annees and len(annees) > 1:
        compare_dims.append("annee")

    if regions and len(regions) > 1:
        compare_dims.append("region")

    if departements and len(departements) > 1:
        compare_dims.append("departement")

    if communes and len(communes) > 1:
        compare_dims.append("commune")
    # =====================================================
    # MODE NORMAL
    # =====================================================
    if len(compare_dims) == 0:

        cards = []

        for ind in indicateurs:

            if ind not in df.columns:
                continue

            valeur, moyenne, nb_nan, typ = compute_kpi(df, ind)

            cards.append(

                dbc.Col(

                    html.Div([

                        html.Div(
                            ind.upper(),
                            className="kpi-title"
                        ),

                        html.Div(
                            format_value(valeur, typ),
                            className="kpi-value"
                        ),

                        html.Div(
                            f"Moyenne : {moyenne:,.2f}".replace(",", " ")
                            if typ == "brut"
                            else f"Moyenne : {moyenne:.2f} %",
                            className="kpi-sub"
                        ),

                        html.Div(
                            f"Type : {'Valeur brute' if typ=='brut' else 'Taux / Ratio'}",
                            className="kpi-context"
                        ),

                        html.Div(
                            f"Vides : {nb_nan}",
                            className="kpi-context"
                        )

                    ],
                    className="kpi-card"),

                    xs=12,
                    sm=6,
                    md=4,
                    lg=3,
                    xl=3

                )

            )

        return html.Div([

            html.H5(
                format_zone_label(df),
                className="zone-title"
            ),

            dbc.Row(cards, className="g-3 mt-2")

        ], className="zone-block")

    # =====================================================
    # MODE COMPARAISON
    # =====================================================
    blocks = []

    for key, group in df.groupby(compare_dims):

        cards = []

        for ind in indicateurs:

            if ind not in group.columns:
                continue

            valeur, moyenne, nb_nan, typ = compute_kpi(group, ind)

            cards.append(

                dbc.Col(

                    html.Div([

                        html.Div(
                            ind.upper(),
                            className="kpi-title"
                        ),

                        html.Div(
                            format_value(valeur, typ),
                            className="kpi-value"
                        ),

                        html.Div(
                            f"Moyenne : {moyenne:,.2f}".replace(",", " ")
                            if typ == "brut"
                            else f"Moyenne : {moyenne:.2f} %",
                            className="kpi-sub"
                        ),

                        html.Div(
                            f"Type : {'Valeur brute' if typ=='brut' else 'Taux / Ratio'}",
                            className="kpi-context"
                        ),

                        html.Div(
                            f"Vides : {nb_nan}",
                            className="kpi-context"
                        )

                    ],
                    className="kpi-card"),

                    xs=12,
                    sm=6,
                    md=4,
                    lg=3,
                    xl=3

                )

            )

        # ---- Titre du bloc ----
# ---- Titre du bloc (ordre fixe : Année | Département | Commune) ----
        if not isinstance(key, tuple):
            key = (key,)

        # ANNEE
        if "annee" in compare_dims:
            annee_val = key[compare_dims.index("annee")]
        else:
            annees_u = sorted(group["annee"].dropna().unique())
            annee_val = annees_u[0] if len(annees_u) == 1 else ("Toutes" if annees_u else "—")

        # DEPARTEMENT
        if "departement" in compare_dims:
            departement = key[compare_dims.index("departement")]
        else:
            deps = sorted(group["departement"].dropna().unique())
            departement = deps[0] if len(deps) == 1 else (" / ".join(deps) if deps else "—")

        # COMMUNE
        if "commune" in compare_dims:
            commune = key[compare_dims.index("commune")]
        else:
            coms = sorted(group["commune"].dropna().unique())
            commune = coms[0] if len(coms) == 1 else ("Toutes" if coms else "—")

        titre = f"Année : {annee_val} | Département : {departement} | Commune : {commune}"

        blocks.append(

            html.Div([

                html.H5(
                    titre,
                    className="zone-title"
                ),

                dbc.Row(cards, className="g-3"),
            ], className="zone-block")

        )
    return blocks

@callback(
    Output("download-kpi", "data"),

    Input("download-kpi-btn", "n_clicks"),

    State("secteur-dd", "value"),
    State("annee-dd", "value"),
    State("region-dd", "value"),
    State("departement-dd", "value"),
    State("commune-dd", "value"),
    State("indicateur-dd", "value"),

    prevent_initial_call=True
)
def export_kpis(
    n_clicks,
    secteur,
    annees,
    regions,
    departements,
    communes,
    indicateurs
):

    if not n_clicks:
        return dash.no_update

    if not secteur or not indicateurs:
        return dash.no_update

    import io
    import pandas as pd

    from utils.data_loader import (
        load_sector_data,
        get_indicator_type
    )

    df = load_sector_data(secteur).copy()

    # ==========================
    # FILTRES
    # ==========================
    if annees:
        df = df[df["annee"].isin(annees)]

    if regions:
        df = df[df["region"].isin(regions)]

    if departements:
        df = df[df["departement"].isin(departements)]

    if communes:
        df = df[df["commune"].isin(communes)]

    if df.empty:
        return dash.no_update

    # ==========================
    # DIMENSION
    # ==========================
    if communes:
        dimension = "commune"
    elif departements:
        dimension = "departement"
    elif regions:
        dimension = "region"
    elif annees and len(annees) > 1:
        dimension = "annee"
    else:
        dimension = None

    resultats = []

    # ==========================
    # CALCUL KPI
    # ==========================
    for ind in indicateurs:

        if ind not in df.columns:
            continue

        typ = get_indicator_type(ind)

        # -----------------------
        # PAS DE COMPARAISON
        # -----------------------
        if dimension is None:

            serie = df[ind]

            nb_nan = serie.isna().sum()

            nb_valeurs = serie.notna().sum()

            if typ == "taux":
                valeur = serie.mean(skipna=True)
            else:
                valeur = serie.sum(skipna=True)

            resultats.append({

                "indicateur": ind,
                "type": typ,
                "dimension": "Global",
                "modalite": "Tous",

                "valeur": valeur,

                "nb_valeurs": nb_valeurs,
                "nb_nan": nb_nan

            })

        # -----------------------
        # COMPARAISON
        # -----------------------
        else:

            for modalite, groupe in df.groupby(dimension):

                serie = groupe[ind]

                nb_nan = serie.isna().sum()

                nb_valeurs = serie.notna().sum()

                if typ == "taux":
                    valeur = serie.mean(skipna=True)
                else:
                    valeur = serie.sum(skipna=True)

                resultats.append({

                    "indicateur": ind,
                    "type": typ,

                    "dimension": dimension,
                    "modalite": modalite,

                    "valeur": valeur,

                    "nb_valeurs": nb_valeurs,
                    "nb_nan": nb_nan

                })

    final_df = pd.DataFrame(resultats)

    # ==========================
    # EXPORT EXCEL
    # ==========================
    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        final_df.to_excel(
            writer,
            sheet_name="KPIs",
            index=False
        )

    output.seek(0)

    return dcc.send_bytes(
        output.getvalue(),
        f"KPIs_{secteur}.xlsx"
    )
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

    html.H2(id="dynamic-title"),
    html.Div(id="filters-summary", className="filters-summary mt-2"),
# =========================
# FILTERS
# =========================
dbc.Row([

    dbc.Col([
        html.Div("📊 Secteur", className="filter-title"),
        dcc.Dropdown(
            id="secteur-dd",
            placeholder="Choisir un secteur",
            clearable=False,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

    dbc.Col([
        html.Div("📅 Année", className="filter-title"),
        dcc.Dropdown(
            id="annee-dd",
            placeholder="Toutes les années",
            multi=True,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

    dbc.Col([
        html.Div("🌍 Région", className="filter-title"),
        dcc.Dropdown(
            id="region-dd",
            placeholder="Toutes les régions",
            multi=True,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

    dbc.Col([
        html.Div("🏙️ Département", className="filter-title"),
        dcc.Dropdown(
            id="departement-dd",
            placeholder="Tous les départements",
            multi=True,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

    dbc.Col([
        html.Div("📍 Commune", className="filter-title"),
        dcc.Dropdown(
            id="commune-dd",
            placeholder="Toutes les communes",
            multi=True,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

    dbc.Col([
        html.Div("📈 Indicateurs", className="filter-title"),
        dcc.Dropdown(
            id="indicateur-dd",
            placeholder="Choisir indicateurs",
            multi=True,
            persistence=True,
            persistence_type="local"
        )
    ], width=2),

], className="filters-bar"),

    dcc.Download(id="download-kpi"),

    html.Div([

    dbc.Button(
        "📥 Télécharger KPI sélectionnés",
        id="download-kpi-btn",
        color="dark",
        className="mb-3"
    ),

], className="d-flex justify-content-end"),

    html.Div(id="kpi-container")

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
        return "📊 Analyse multi-sectorielle"

    return f"📊 Analyse multi-sectorielle - {secteur}"



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

@callback(
    Output("filters-summary", "children"),

    Input("annee-dd", "value"),
    Input("region-dd", "value"),
    Input("departement-dd", "value"),
    Input("commune-dd", "value"),
)
def show_selected(annee, region, dep, com):

    def format(label, value):
        if not value:
            return None

        if isinstance(value, list):
            value = ", ".join(map(str, value))

        return html.Span(f"{label}: {value}", className="filter-badge")

    return html.Div([
        format("📅 Année", annee),
        format("🌍 Région", region),
        format("🏙️ Département", dep),
        format("📍 Commune", com),
    ], className="d-flex gap-2 flex-wrap")

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

@callback(
    Output("secteur-dd", "value"),
    Output("annee-dd", "value"),
    Output("region-dd", "value"),
    Output("departement-dd", "value"),
    Output("commune-dd", "value"),
    Output("indicateur-dd", "value"),

    Input("filters-store", "data"),
)
def restore_filters(data):

    if not data:
        return None, None, None, None, None, None

    return (
        data.get("secteur"),
        data.get("annee"),
        data.get("region"),
        data.get("departement"),
        data.get("commune"),
        data.get("indicateur"),
    )

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
            "📊 Sélectionnez un secteur",
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
            "❌ Aucune donnée disponible",
            className="text-center mt-4 fw-bold text-danger"
        )

    if not indicateurs:
        return html.Div(
            "📈 Sélectionnez un ou plusieurs indicateurs",
            className="text-center mt-4 fw-bold text-muted"
        )

    # =========================
    # DIMENSION DE COMPARAISON
    # =========================
    compare_dim = None

    if annees and len(annees) > 1:
        compare_dim = "annee"

    elif regions and len(regions) > 1:
        compare_dim = "region"

    elif departements and len(departements) > 1:
        compare_dim = "departement"

    elif communes and len(communes) > 1:
        compare_dim = "commune"

    # =====================================================
    # MODE NORMAL
    # =====================================================
    if compare_dim is None:

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

        return dbc.Row(cards, className="g-3 mt-2")

    # =====================================================
    # MODE COMPARAISON
    # =====================================================
    blocks = []

    for key, group in df.groupby(compare_dim):

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

        blocks.append(

            html.Div([

                html.H5(
                    f"📊 {compare_dim.upper()} : {key}",
                    className="mt-4 mb-3 fw-bold"
                ),

                dbc.Row(cards, className="g-3")

            ])

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
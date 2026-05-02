from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# ==========================
# PAGES
# ==========================
from pages.secteurs import secteurs_layout
from pages.agriculture import agriculture_layout
from pages.aquaculture import aquaculture_layout

# ==========================
# APP INIT
# ==========================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server  # pour Render

# ==========================
# SIDEBAR PROPRE (SANS SECTEURS)
# ==========================
sidebar = html.Div([

    html.H3("Dashboard", style={"padding": "10px"}),

    html.Hr(),

    dcc.Link("🏠 Accueil", href="/", style={"display": "block", "padding": "8px"}),
    dcc.Link("📊 Secteurs", href="/secteurs", style={"display": "block", "padding": "8px"}),
    dcc.Link("🗺 Cartographie", href="/cartographie", style={"display": "block", "padding": "8px"}),
    dcc.Link("⚖ Comparaison", href="/comparaison", style={"display": "block", "padding": "8px"}),
    dcc.Link("📈 Graphiques", href="/graphiques", style={"display": "block", "padding": "8px"}),

], style={
    "width": "18%",
    "position": "fixed",
    "height": "100%",
    "backgroundColor": "#f8f9fa",
    "padding": "10px"
})

# ==========================
# LAYOUT GLOBAL
# ==========================
app.layout = html.Div([

    dcc.Location(id="url", refresh=False),

    sidebar,

    html.Div(
        id="page-content",
        style={
            "margin-left": "20%",
            "padding": "20px"
        }
    )

])

# ==========================
# ROUTING
# ==========================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):

    if pathname == "/" or pathname is None:
        return html.H2("🏠 Accueil Dashboard")

    if pathname == "/secteurs":
        return secteurs_layout

    if pathname == "/agriculture":
        return agriculture_layout

    if pathname == "/aquaculture":
        return aquaculture_layout

    if pathname == "/cartographie":
        return html.H2("🗺 Cartographie")

    if pathname == "/comparaison":
        return html.H2("⚖ Comparaison")

    if pathname == "/graphiques":
        return html.H2("📈 Graphiques")

    return html.H2("404 - Page introuvable")

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
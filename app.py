from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# ==========================
# IMPORT PAGES
# ==========================
from pages.secteurs import secteurs_layout
# tu ajouteras ensuite :
# from pages.cartographie import cartographie_layout
# from pages.comparaison import comparaison_layout
# from pages.graphiques import graphiques_layout

# ==========================
# APP INIT
# ==========================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server  # pour Render / déploiement

# ==========================
# SIDEBAR
# ==========================
sidebar = html.Div(
    [
        html.H2("Dashboard", className="text-white"),

        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/", active="exact"),
                dbc.NavLink("Secteurs", href="/secteurs", active="exact"),
                dbc.NavLink("Cartographie", href="/cartographie", active="exact"),
                dbc.NavLink("Comparaison", href="/comparaison", active="exact"),
                dbc.NavLink("Graphiques", href="/graphiques", active="exact"),
            ],
            vertical=True,
            pills=True
        )
    ],
    style={
        "padding": "20px",
        "background-color": "#2c3e50",
        "height": "100vh",
        "color": "white"
    }
)

# ==========================
# LAYOUT GLOBAL
# ==========================
app.layout = html.Div([
    dcc.Location(id="url"),

    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(html.Div(id="page-content"), width=10)
    ])
])

# ==========================
# ROUTING CALLBACK
# ==========================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):

    if pathname == "/":
        return html.Div([
            html.H1("Accueil Dashboard"),
            html.P("Bienvenue sur le dashboard multi-secteurs.")
        ])

    elif pathname == "/secteurs":
        return secteurs_layout

    elif pathname == "/cartographie":
        return html.Div([
            html.H2("Cartographie"),
            html.P("Section en cours de développement")
        ])

    elif pathname == "/comparaison":
        return html.Div([
            html.H2("Comparaison"),
            html.P("Analyse comparative des secteurs")
        ])

    elif pathname == "/graphiques":
        return html.Div([
            html.H2("Graphiques"),
            html.P("Visualisations avancées")
        ])

    return html.H1("404 - Page introuvable")


# ==========================
# RUN SERVER
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
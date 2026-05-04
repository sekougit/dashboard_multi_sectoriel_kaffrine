import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

server = app.server

# SIDEBAR MODERNE
sidebar = html.Div(
    [
        html.H2("Dashboard", className="text-white"),
        html.Hr(),

        dbc.Nav([
            dbc.NavLink("🏠 Accueil", href="/", active="exact"),
            dbc.NavLink("📊 Secteurs", href="/secteurs", active="exact"),
            dbc.NavLink("📈 Graphiques", href="/graphiques", active="exact"),
            dbc.NavLink("🗺️ Cartographie", href="/cartographie", active="exact"),
            dbc.NavLink("⚖️ Comparaison", href="/comparaison", active="exact"),
            dbc.NavLink("📑 Statistiques", href="/statistiques", active="exact"),
        ], vertical=True, pills=True),
    ],
    className="sidebar"
)

content = html.Div(dash.page_container, className="content")

app.layout = html.Div([sidebar, content])

if __name__ == "__main__":
    app.run(debug=True)
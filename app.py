import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

# =========================
# SIDEBAR
# =========================
sidebar = html.Div([
    html.H3("📊 Dashboard", className="text-white"),
    html.Hr(),

    dbc.Nav([
        dbc.NavLink("🏠 Accueil", href="/", active="exact"),
        dbc.NavLink("📊 Secteurs", href="/secteurs", active="exact"),
        dbc.NavLink("📈 Graphiques", href="/graphiques"),
        dbc.NavLink("🗺️ Cartographie", href="/cartographie"),
        dbc.NavLink("⚖️ Comparaison", href="/comparaison"),
        dbc.NavLink("📑 Statistiques", href="/statistiques"),
    ], vertical=True, pills=True)

], className="sidebar")

content = html.Div(dash.page_container, className="content")

app.layout = html.Div([
    # 🔥 STORE GLOBAL (PERSISTENCE)
    dcc.Store(id="filters-store", storage_type="local"),

    sidebar,
    content
])

if __name__ == "__main__":
    app.run(debug=True)
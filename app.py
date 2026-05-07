import dash
from dash import html, dcc, Input, Output, State, callback
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
sidebar = html.Div(
    [
        html.H3("📊 Dashboard", className="sidebar-title"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("🏠 Accueil", href="/", active="exact"),
                dbc.NavLink("📊 Secteurs", href="/secteurs", active="exact"),
                dbc.NavLink("📈 Graphiques", href="/graphiques", active="exact"),
                dbc.NavLink("🗺️ Cartographie", href="/cartographie", active="exact"),
                dbc.NavLink("⚖️ Comparaison", href="/comparaison", active="exact"),
                dbc.NavLink("📑 Statistiques", href="/statistiques", active="exact"),
            ],
            vertical=True,
            pills=True,
            className="nav-links"
        ),
    ],
    id="sidebar",
    className="sidebar expanded"
)


# =========================
# CONTENT
# =========================
content = html.Div(
    dash.page_container,
    id="page-content",
    className="content expanded"
)


# =========================
# LAYOUT GLOBAL
# =========================
app.layout = html.Div([

    # TOPBAR
    html.Div([
        html.Button("☰", id="toggle-btn", n_clicks=0, className="toggle-btn"),
        html.H4("Dashboard Analytique", className="app-title"),
    ], className="topbar"),

    # STORE GLOBAL
    dcc.Store(id="filters-store", storage_type="local"),
    dcc.Store(id="graph-store", storage_type="local"),

    # MAIN
    html.Div([
        sidebar,
        content
    ], className="main-container")

])


# =========================
# TOGGLE SIDEBAR
# =========================
@callback(
    Output("sidebar", "className"),
    Input("toggle-btn", "n_clicks"),
    State("sidebar", "className"),
)
def toggle_sidebar(n, current):

    if not n:
        return "sidebar expanded"

    if "collapsed" in current:
        return "sidebar expanded"

    return "sidebar collapsed"


if __name__ == "__main__":
    app.run(debug=True)
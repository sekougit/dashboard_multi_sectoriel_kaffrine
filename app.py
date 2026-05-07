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
# SIDEBAR CONTENT
# =========================
sidebar_content = html.Div([

    html.Div([
        html.H3(
            "📊 Dashboard",
            className="sidebar-title"
        ),
    ], className="sidebar-header"),

    html.Hr(),

    dbc.Nav([

        dbc.NavLink(
            [
                html.Span("🏠"),
                html.Span(" Accueil", className="link-text")
            ],
            href="/",
            active="exact"
        ),

        dbc.NavLink(
            [
                html.Span("📊"),
                html.Span(" Secteurs", className="link-text")
            ],
            href="/secteurs",
            active="exact"
        ),

        dbc.NavLink(
            [
                html.Span("📈"),
                html.Span(" Graphiques", className="link-text")
            ],
            href="/graphiques",
            active="exact"
        ),

        dbc.NavLink(
            [
                html.Span("🗺️"),
                html.Span(" Cartographie", className="link-text")
            ],
            href="/cartographie",
            active="exact"
        ),

        dbc.NavLink(
            [
                html.Span("⚖️"),
                html.Span(" Comparaison", className="link-text")
            ],
            href="/comparaison",
            active="exact"
        ),

        dbc.NavLink(
            [
                html.Span("📑"),
                html.Span(" Statistiques", className="link-text")
            ],
            href="/statistiques",
            active="exact"
        ),

    ],
    vertical=True,
    pills=True,
    className="nav-links")

])


# =========================
# DESKTOP SIDEBAR
# =========================
desktop_sidebar = html.Div(
    sidebar_content,
    id="sidebar",
    className="sidebar expanded"
)


# =========================
# MOBILE DRAWER
# =========================
mobile_drawer = dbc.Offcanvas(
    sidebar_content,
    id="mobile-drawer",
    title="📊 Navigation",
    is_open=False,
    placement="start",
    className="mobile-drawer"
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
# APP LAYOUT
# =========================
app.layout = html.Div([

    # TOPBAR
    html.Div([

        html.Button(
            "☰",
            id="toggle-btn",
            n_clicks=0,
            className="toggle-btn"
        ),

        html.H4(
            "Dashboard Analytique",
            className="app-title"
        )

    ], className="topbar"),

    # STORES
    dcc.Store(
        id="filters-store",
        storage_type="local"
    ),

    dcc.Store(
        id="graph-store",
        storage_type="local"
    ),

    # MOBILE DRAWER
    mobile_drawer,

    # MAIN
    html.Div([

        desktop_sidebar,

        content

    ], className="main-container")

])


# =========================
# DESKTOP SIDEBAR TOGGLE
# =========================
@callback(
    Output("sidebar", "className"),
    Output("page-content", "className"),

    Input("toggle-btn", "n_clicks"),

    State("sidebar", "className"),

    prevent_initial_call=True
)
def toggle_sidebar(n, current):

    if "collapsed" in current:

        return (
            "sidebar expanded",
            "content expanded"
        )

    return (
        "sidebar collapsed",
        "content collapsed"
    )


# =========================
# MOBILE DRAWER TOGGLE
# =========================
@callback(
    Output("mobile-drawer", "is_open"),
    Input("toggle-btn", "n_clicks"),
    State("mobile-drawer", "is_open"),
    prevent_initial_call=True
)
def toggle_drawer(n, is_open):

    return not is_open


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
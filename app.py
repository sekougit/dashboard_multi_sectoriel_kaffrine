import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from auth import init_auth
from login import login_bp

import dash_ag_grid as dag

from flask import request, redirect
from flask_login import current_user

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        <link rel="icon" type="image/png" href="/assets/mon_icone.png">
        <link rel="apple-touch-icon" href="/assets/mon_icone_180.png">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''



server = app.server

init_auth(server)

server.register_blueprint(login_bp)

# ==========================================================
# PROTECTION DES PAGES
# ==========================================================
@server.before_request
def protect_dash():

    path = request.path

    # ==========================
    # Routes publiques
    # ==========================
    public_routes = [
        "/login",
        "/logout",
        "/favicon.ico"
    ]

    if path in public_routes:
        return

    # ==========================
    # Ressources Dash
    # ==========================
    if (
        path.startswith("/assets/")
        or path.startswith("/_dash-")
        or path.startswith("/_favicon")
        or path.startswith("/_reload-hash")
        or path.startswith("/_alive")
    ):
        return

    # ==========================
    # Utilisateur connecté ?
    # ==========================
    if current_user.is_authenticated:
        return

    # ==========================
    # Sinon -> Login
    # ==========================
    return redirect("/login")


# =========================
# SIDEBAR CONTENT
# =========================
sidebar_content = html.Div([

    html.Div([
        html.H3(
                [
        html.I(className="bi bi-speedometer2 me-2"),
        "Dashboard"
            ],
            className="sidebar-title"
        ),
    ], className="sidebar-header"),

    html.Hr(),

    dbc.Nav([

        dbc.NavLink(
            [
    html.I(className="bi bi-house-door-fill me-2"),
    "Accueil"
                ],
            href="/",
            active="exact"
        ),

        dbc.NavLink(
            [
    html.I(className="bi bi-grid-3x3-gap-fill me-2"),
    "Secteurs"
            ],
            href="/secteurs",
            active="exact"
        ),

        dbc.NavLink(
            [
    html.I(className="bi bi-bar-chart-line-fill me-2"),
    "Graphiques"
            ],
            href="/graphiques",
            active="exact"
        ),

        dbc.NavLink(
            [
    html.I(className="bi bi-geo-alt-fill me-2"),
    "Cartographie"
                        ],
            href="/cartographie",
            active="exact"
        ),

        dbc.NavLink(
                        [
                html.I(className="bi bi-bar-chart-steps me-2"),
                "Comparaison"
            ],
            href="/comparaison",
            active="exact"
        ),

        dbc.NavLink(
                        [
                html.I(className="bi bi-clipboard-data-fill me-2"),
                "Statistiques"
            ],
            href="/statistiques",
            active="exact"
        ),

    ],
    vertical=True,
    pills=True,
    className="nav-links"),

html.Form(

    action="/logout",
    method="get",

    children=[

        dbc.Button(
            [
                html.I(className="bi bi-box-arrow-right me-2"),
                "Déconnexion"
            ],
            type="submit",
            color="danger",
            className="w-100"
        )

    ]

)

],
style={
    "display": "flex",
    "flexDirection": "column",
    "height": "100%"
})

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

    html.Div([

        html.Button(
            "☰",
            id="toggle-btn",
            n_clicks=0,
            className="toggle-btn"
        ),

        html.H4(
            "Dashboard Multi-Sectoriel - Kaffrine",
            className="app-title"
        ),

    ], className="topbar-left"),

    html.Div(
        id="user-profile",
        className="user-profile"
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
# USER PROFILE
# =========================
@callback(
    Output("user-profile", "children"),
    Input("graph-store", "id")
)
def update_user_profile(_):

    if not getattr(current_user, "is_authenticated", False):
        return ""

    initials = "".join(
        nom[0].upper()
        for nom in current_user.fullname.split()
    )

    return [

        html.Div(
            initials,
            className="user-avatar"
        ),

        html.Div([

            html.Div(
                current_user.fullname,
                className="user-fullname"
            ),

            html.Div(
                current_user.direction,
                className="user-direction"
            )

        ])

    ]


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
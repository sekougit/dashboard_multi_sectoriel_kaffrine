import dash
from dash import html

dash.register_page(__name__, path="/cartographie")

layout = html.Div([
    html.H1("cartographie"),
    html.P("Bienvenue sur la partie cartographie")
])
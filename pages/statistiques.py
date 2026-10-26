import dash
from dash import html

dash.register_page(__name__, path="/statistiques")

layout = html.Div([
    html.H1("Statistiques"),
    html.P("Bienvenue sur la partie statistiques")
])
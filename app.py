from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from pages.agriculture import agriculture_layout

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

app.layout = dbc.Container([

    html.H1(
        "Dashboard Territorial Agriculture",
        className="text-center my-4"
    ),

    agriculture_layout

], fluid=True)


if __name__ == '__main__':
    app.run(debug=True)

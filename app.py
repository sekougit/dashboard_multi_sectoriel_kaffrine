from dash import Dash, html

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard Territorial Kaffrine")
])

if __name__ == "__main__":
    app.run_server(debug=True)
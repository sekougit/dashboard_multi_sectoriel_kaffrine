import dash
from dash import html
from utils.data_loader import load_sector_data
from utils.filters import filter_data
from utils.kpi_calculator import compute_kpis

dash.register_page(__name__, path="/sante")

df = load_sector_data("SANTE")

layout = html.Div([
    html.H1("Secteur SANTE"),

    html.Div(id="kpi-sante")
])
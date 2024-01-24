import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend import navbar, navbar3

dash.register_page(__name__, path_template='/history')


layout = html.Div([
    navbar.navbar,
    navbar3.navbar
])
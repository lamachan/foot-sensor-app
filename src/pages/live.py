import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend import navbar, navbar2

dash.register_page(__name__, path_template='/live')


layout = html.Div([
    navbar.navbar,
    navbar2.navbar,
])
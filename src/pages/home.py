import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend import navbar

dash.register_page(__name__, path_template='/')

layout = html.Div(children=[
    navbar.navbar,
    html.H1('Hello to Foot Sensor App'),
])
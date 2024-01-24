import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div([
    html.H1("404 - Page Not Found"),
    html.P("The requested page does not exist."),
    dcc.Link("Go to Home", href="/")
])
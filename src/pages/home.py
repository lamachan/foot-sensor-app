import dash
from dash import html, dcc

dash.register_page(__name__, path_template='/')

layout = html.Div([
    html.H1('Homepage'),
    html.Div([
        html.Div(
            dcc.Link('Current sensor measurements', href='/current')
        )
    ])
])
import dash
from dash import html, dcc

dash.register_page(__name__, path_template="/current")


layout = html.Div([
    html.H1('Homepage of /current'),
    html.Div([
        html.Div(
            dcc.Link(f"Patient no. {i}", href=f'{i}')
        ) for i in range(1,7)
    ])
])
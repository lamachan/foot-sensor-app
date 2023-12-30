import dash
from dash import html, dcc

dash.register_page(__name__, path_template='/history')


layout = html.Div([
    html.H1('Homepage of /history'),
    html.Div([
        html.Div(
            dcc.Link(f'Patient no. {i}', href=f'/history/{i}')
        ) for i in range(1,7)
    ])
])
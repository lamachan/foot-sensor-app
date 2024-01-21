import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend import navbar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash.register_page(__name__, path_template='/')

layout = html.Div(children=[
    navbar.navbar,
    html.H1('Hello to Foot Sensor App'),
])

if __name__ == '__main__':
    app.run_server(debug=True)

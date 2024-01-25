import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend import navbar
from feet_sensors import FeetSensors

dash.register_page(__name__, path_template='/')

layout = html.Div(children=[
    navbar.navbar,
    dbc.Container(
        fluid=True,
        children=[
            dbc.Row(
                [
                    dbc.Col([
                        html.H1('Foot Sensor App'),
                        html.P("Authors: Daria Danieluk, Weronika Zbierowska")
                    ], width={"size": 6, "offset": 3}, style={"textAlign": "center"})
                ]),
            dbc.Row(
                [
                    dbc.Col(
                        FeetSensors(
                            id='example-feet-sensors',
                            L0=1023,
                            L1=634,
                            L2=2,
                            R0=55,
                            R1=63,
                            R2=977,
                            anomaly_L0=False,
                            anomaly_L1=False,
                            anomaly_L2=False,
                            anomaly_R0=True,
                            anomaly_R1=True,
                            anomaly_R2=True
                        ), width='auto'),
                ], justify="center"),
        ]
    )
])
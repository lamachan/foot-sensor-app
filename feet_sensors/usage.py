import feet_sensors
from dash import Dash, callback, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    feet_sensors.FeetSensors(
        id='feet-sensors',
        L0=1023,
        L1=1023,
        L2=100,
        R0=0,
        R1=10,
        R2=655,
        anomaly_L0=False,
        anomaly_L1=True,
        anomaly_L2=False,
        anomaly_R0=False,
        anomaly_R1=True,
        anomaly_R2=False,
    )
])


# @callback(Output('output', 'children'), Input('input', 'value'))
# def display_output(value):
#     return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)

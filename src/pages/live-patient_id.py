import dash
from dash import html, dcc, callback, Input, Output, State
import redis
import json
import pandas as pd
from feet_sensors import FeetSensors

import dash_bootstrap_components as dbc
from frontend import navbar

def title(patient_id=None):
    return f'Patient {patient_id} - live'

dash.register_page(__name__, path_template='/live/<patient_id>', title=title)

redis_host = 'localhost'
redis_port = 6379
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

REGISTERED_PATIENTS = ['1', '2', '3', '4', '5', '6']

def layout(patient_id=None):
    if patient_id not in REGISTERED_PATIENTS:
        return html.Div(
            f'Patient ID: {patient_id} is invalid.'
        )

    # valid patient_id
    return html.Div([
        dcc.Location(id='url', refresh=False),

        navbar.navbar,

        dbc.Container(fluid=True, children=[
            dbc.Row([
                load_patient_data(patient_id),
                dbc.Col([
                    FeetSensors(
                        id='feet-sensors',
                        L0=0,
                        L1=0,
                        L2=0,
                        R0=0,
                        R1=0,
                        R2=0,
                        anomaly_L0=False,
                        anomaly_L1=False,
                        anomaly_L2=False,
                        anomaly_R0=False,
                        anomaly_R1=False,
                        anomaly_R2=False
                    ),
                ])
            ], style={'margin-top': '10px', 'margin-bottom': '10px'}),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='L0-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                    dcc.Graph(
                        id='L1-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                    dcc.Graph(
                        id='L2-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                ], width=6),

                dbc.Col([
                    dcc.Graph(
                        id='R0-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                    dcc.Graph(
                        id='R1-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                    dcc.Graph(
                        id='R2-live-graph',
                        style={'width': '100%', 'height': '18vh', 'margin-bottom': '10px'}
                    ),
                ], width=6),
            ], style={'margin-bottom': '10px'}),

            dcc.Interval(
                id='interval-component',
                interval=1000,
                n_intervals=0
            )
        ], style={'height': '80vh'})
    ], style={'height': '80vh'})
    
# load patient's personal information and all avaliable data from a redis list
def load_patient_data(patient_id):
    data = fetch_all_data(patient_id)
    
    if data:
        row_list = [
            [
                row['time'],
                row['data']['firstname'],
                row['data']['lastname'],
                int(str(row['data']['trace']['id'])[:-8]),
                int(str(row['data']['trace']['id'])[-8:])
            ] + [
                s['anomaly'] for s in row['data']['trace']['sensors']
            ] + [
                s['value'] for s in row['data']['trace']['sensors']
            ]
            for row in data
        ]
        df = pd.DataFrame(row_list, columns='time firstname lastname trace_id_id trace_id_date anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())
        json_data = df.to_json(orient='split')
    
    return dbc.Col([
        dcc.Store(id='patient-data-store', data=json_data),
        html.P([
            html.Strong("Name: "), f"{data[0]['data']['firstname']} {data[0]['data']['lastname']}",
        ], style={'fontSize': '20px'}),
        html.P([
            html.Strong("Birth year: "), f"{data[0]['data']['birthdate']}",
        ], style={'fontSize': '20px'}),
        html.P([
            html.Strong("Disability: "), f"{data[0]['data']['disabled']}",
        ], style={'fontSize': '20px'}),
    ], width=6, style={'margin': 'auto'}) if data else dbc.Col(html.Div("Patient information not found."))

# fetch all data avaliable in the redis list
def fetch_all_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    all_data = redis_client.lrange(data_key, 0, -1)
    if all_data:
        parsed_data = [json.loads(entry) for entry in all_data]
        return parsed_data
    return None

# fetch the newest data record from a redis list
def fetch_new_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    if latest_data:
        return json.loads(latest_data)
    return None

# update the graphs and the feet diagram every 1 second
@callback(
    [Output('L0-live-graph', 'figure'),
    Output('L1-live-graph', 'figure'),
    Output('L2-live-graph', 'figure'),
    Output('R0-live-graph', 'figure'),
    Output('R1-live-graph', 'figure'),
    Output('R2-live-graph', 'figure'),
    Output('feet-sensors', 'anomaly_L0'),
    Output('feet-sensors', 'anomaly_L1'),
    Output('feet-sensors', 'anomaly_L2'),
    Output('feet-sensors', 'anomaly_R0'),
    Output('feet-sensors', 'anomaly_R1'),
    Output('feet-sensors', 'anomaly_R2'),
    Output('feet-sensors', 'L0'),
    Output('feet-sensors', 'L1'),
    Output('feet-sensors', 'L2'),
    Output('feet-sensors', 'R0'),
    Output('feet-sensors', 'R1'),
    Output('feet-sensors', 'R2'),
    Output('patient-data-store', 'data')],

    [Input('interval-component', 'n_intervals')],

    [State('url', 'pathname'),
    State('patient-data-store', 'data')]
)
def update_graph(n, pathname, patient_data):
    patient_id = int(pathname.split('/')[-1])

    # update patient_data Store
    if patient_data:
        if n > 0:
            data = fetch_new_data(patient_id)

            if data:
                row_list = [
                    data['time'],
                    data['data']['firstname'],
                    data['data']['lastname'],
                    str(data['data']['trace']['id'])[:-8],
                    str(data['data']['trace']['id'])[-8:]
                ] + [
                    s['anomaly'] for s in data['data']['trace']['sensors']
                ] + [
                    s['value'] for s in data['data']['trace']['sensors']
                ]
                new_data_df = pd.DataFrame([row_list], columns='time firstname lastname trace_id_id trace_id_date anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())
                
                current_data_df = pd.read_json(patient_data, orient='split')
                df = pd.concat([current_data_df, new_data_df], ignore_index=True)
                if len(df) > 600:
                    rows_to_remove = len(df) - 600
                    df = df.iloc[rows_to_remove:]

                patient_data = df.to_json(orient='split')
            else:
                return [{'data': [], 'layout': {}}] * 6, [False] * 6, [0] * 6, patient_data
        else:
            df = pd.read_json(patient_data, orient='split')
    else:
        return [{'data': [], 'layout': {}}] * 6, [False] * 6, [0] * 6, patient_data

    # update graphs
    updated_figures = []
    for sensor in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2']:
        all_data_trace = {
                            'x': df['time'],
                            'y': df[sensor],
                            'type': 'scatter',
                            'mode': 'lines',
                            'name': f'{sensor} (Normal)',
                            'line': {'color': '#0912bf'},
                            'showlegend': False
                        }

        # split anomaly traces
        anomaly_indices = df[df[f'anomaly_{sensor}'] == True].index.tolist()
        anomaly_traces = []

        if anomaly_indices:
            streaks = []
            current_streak = []
            for i in range(len(anomaly_indices) - 1):
                if anomaly_indices[i + 1] - anomaly_indices[i] == 1:
                    current_streak.append(anomaly_indices[i])
                else:
                    current_streak.append(anomaly_indices[i])
                    streaks.append(current_streak)
                    current_streak = []
            current_streak.append(anomaly_indices[-1])
            streaks.append(current_streak)

            for streak in streaks:
                trace = {
                            'x': df.loc[streak, 'time'],
                            'y': df.loc[streak, sensor],
                            'type': 'scatter',
                            'mode': 'lines',
                            'name': f'{sensor} (Anomaly)',
                            'line': {'color': '#bf0912', 'width': 2},
                            'showlegend': False
                        }
                anomaly_traces.append(trace)
        
        fig = {
            'data': [all_data_trace, *anomaly_traces],
            'layout': {
                'title': f'{sensor}',
                'xaxis': dict(
                    title='Time',
                    tickmode='auto',
                    nticks=10,
                    tickfont=dict(size=8),
                    titlefont=dict(size=10)
                ),
                'yaxis': dict(
                    title='Pressure',
                    range=[0,1100],
                    tickfont=dict(size=8),
                    titlefont=dict(size=10),
                ),
                'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
                'uirevision': True
            }
        }
        updated_figures.append(fig)

    # update feet diagram
    anomaly_L0, anomaly_L1, anomaly_L2, anomaly_R0, anomaly_R1, anomaly_R2, L0, L1, L2, R0, R1, R2 = df.iloc[-1, 5:].values

    return *updated_figures, anomaly_L0, anomaly_L1, anomaly_L2, anomaly_R0, anomaly_R1, anomaly_R2, L0, L1, L2, R0, R1, R2, patient_data
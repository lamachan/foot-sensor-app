import dash
from dash import html, dcc, callback, Input, Output, State
import redis
import json
import pandas as pd
import feet_sensors

from frontend import navbar, navbar2

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

    return html.Div([
        dcc.Location(id='url', refresh=False),
        navbar.navbar,
        navbar2.navbar,

        load_patient_data(patient_id),

        # left foot line graphs
        html.Div([
            dcc.Graph(
                id='L0-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
            dcc.Graph(
                id='L1-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
            dcc.Graph(
                id='L2-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),

        # right foot line graphs
        html.Div([
            dcc.Graph(
                id='R0-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
            dcc.Graph(
                id='R1-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
            dcc.Graph(
                id='R2-live-graph',
                style={'width': '100%', 'height': '200px'}
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),

        feet_sensors.FeetSensors(
            id='feet-sensors',
            L0=0,
            L1=30,
            L2=100,
            R0=2,
            R1=55,
            R2=1000,
            anomaly_L0=False,
            anomaly_L1=True,
            anomaly_L2=False,
            anomaly_R0=False,
            anomaly_R1=True,
            anomaly_R2=False,
        ),

        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
        )
    ])
    
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
        print('FETCHED ALL DATA')
        print(df)
        json_data = df.to_json(orient='split')
    
        return html.Div([
            dcc.Store(id='patient-data-store', data=json_data),
            #html.H3(f"Patient ID: {patient_id}"),
            html.P(f"Name: {data[0]['data']['firstname']} {data[0]['data']['lastname']}"),
            html.P(f"Birth year: {data[0]['data']['birthdate']}"),
            html.P(f"Disability: {data[0]['data']['disabled']}")
        ])
    else:
        return html.Div("Patient information not found.")

# fetch all data from a redis list
def fetch_all_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    all_data = redis_client.lrange(data_key, 0, -1)
    if all_data:
        parsed_data = [json.loads(entry) for entry in all_data]
        return parsed_data
    return None

# fetch the last data entry from a redis list
def fetch_new_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    # latest_data = redis_client.lrange(data_key, -5, -1)
    if latest_data:
        return json.loads(latest_data)
        # parsed_data =[json.loads(entry) for entry in latest_data]
        # return parsed_data
    return None

@callback(
    [Output('L0-live-graph', 'figure'),
    Output('L1-live-graph', 'figure'),
    Output('L2-live-graph', 'figure'),
    Output('R0-live-graph', 'figure'),
    Output('R1-live-graph', 'figure'),
    Output('R2-live-graph', 'figure'),
    Output('patient-data-store', 'data')],
    [Input('interval-component', 'n_intervals')],
    [State('url', 'pathname'),
    State('patient-data-store', 'data')]
)
def update_graph(n, pathname, patient_data):
    print(f'Entering the callback function., n={n}')
    # print(f'pathname={pathname}, patient_data={patient_data}')
    patient_id = int(pathname.split('/')[-1])

    if patient_data:
        if n > 0:
            # row_json = fetch_new_data(patient_id)
            data = fetch_new_data(patient_id)

            if data:
                # row_list = [
                #     [
                #         row['time'],
                #         row['data']['firstname'],
                #         row['data']['lastname'],
                #         int(str(row['data']['trace']['id'])[:-8]),
                #         int(str(row['data']['trace']['id'])[-8:])
                #     ] + [
                #         s['anomaly'] for s in row['data']['trace']['sensors']
                #     ] + [
                #         s['value'] for s in row['data']['trace']['sensors']
                #     ]
                #     for row in data
                # ]
                # new_data_df = pd.DataFrame(row_list, columns='time firstname lastname trace_id_id trace_id_date anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())
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
                print(df)

                patient_data = df.to_json(orient='split')
            else:
                return [{'data': [], 'layout': {}}] * 6, patient_data
        else:
            df = pd.read_json(patient_data, orient='split')
    else:
        return [{'data': [], 'layout': {}}] * 6, patient_data

    # missing trace_id - IDK
    # all_trace_ids = pd.DataFrame({'trace_id_id': range(df['trace_id_id'].min(), df['trace_id_id'].max() + 1)})
    # result_df = pd.merge(all_trace_ids, df, on='trace_id_id', how='left')
    # print(result_df)

    # create updated figures for each sensor
    updated_figures = []
    for sensor in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2']:
        all_data_trace = {
                            'x': df['time'],
                            # 'x': df['trace_id_id'],
                            'y': df[sensor],
                            'type': 'scatter',
                            'mode': 'lines',
                            'name': f'{sensor} (Normal)',
                            'showlegend': False
                        }

        anomaly_indices = df[df[f'anomaly_{sensor}'] == True].index.tolist()
        anomaly_traces = []

        if anomaly_indices:
            # find and seperate anomaly streaks
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

            # create a trace for each anomaly streak
            for streak in streaks:
                trace = {
                            'x': df.loc[streak, 'time'],
                            # 'x': df.loc[streak, 'trace_id_id'],
                            'y': df.loc[streak, sensor],
                            'type': 'scatter',
                            'mode': 'lines',
                            'name': f'{sensor} (Anomaly)',
                            'line': {'color': 'red', 'width': 2},
                            'showlegend': False
                        }
                anomaly_traces.append(trace)
        
        fig = {
            'data': [all_data_trace, *anomaly_traces],
            'layout': {
                'title': f'{sensor}',
                'xaxis': dict(
                    title='Time',
                    tickangle=45,
                    tickmode='auto',
                    nticks=10,
                    tickfont=dict(size=8)
                ),
                'yaxis': dict(
                    title='Value',
                    range=[0,1100]
                ),
                'margin': {'l': 40, 'r': 10, 't': 40, 'b': 40},
                'height': 200,
                'uirevision': True
            }
        }
        updated_figures.append(fig)

    return *updated_figures, patient_data
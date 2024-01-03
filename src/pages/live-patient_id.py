import dash
from dash import html, dcc, callback, Input, Output, State
import redis
import json
import pandas as pd

def title(patient_id=None):
    return f'Patient {patient_id} - live'

dash.register_page(__name__, path_template='/live/<patient_id>', title=title)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# dictionary to store DataFrames for each patient
patient_data = {}

REGISTERED_PATIENTS = ['1', '2', '3', '4', '5', '6']

def layout(patient_id=None):
    if patient_id not in REGISTERED_PATIENTS:
        return html.Div(
            f'Patient ID: {patient_id} is invalid.'
        )

    # correct patient_id
    return html.Div([
        dcc.Location(id='url', refresh=False),

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

        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        )
    ])
    
# fetching static patient info
# def update_patient_info(patient_id):
#     row_json = fetch_new_data(patient_id)
    
#     if row_json:
#         return html.Div([
#             html.H3(f"Patient ID: {patient_id}"),
#             html.P(f"Name: {row_json['data']['firstname']} {row_json['data']['lastname']}"),
#             html.P(f"Birth year: {row_json['data']['birthdate']}"),
#             html.P(f"Disability: {row_json['data']['disabled']}")
#         ])
#     else:
#         return html.Div("Patient information not found.")
    
def load_patient_data(patient_id):
    global patient_data

    data = fetch_all_data(patient_id)
    
    if data:
        row_list = [
            [
                row['time'],
                row['data']['firstname'],
                row['data']['lastname'],
                row['data']['trace']['id']
            ] + [
                s['anomaly'] for s in row['data']['trace']['sensors']
            ] + [
                s['value'] for s in row['data']['trace']['sensors']
            ]
            for row in data
        ]
        patient_data[int(patient_id)] = pd.DataFrame(row_list, columns='time firstname lastname trace_id anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())
        print(patient_data[int(patient_id)])
        print(int(patient_id) in patient_data)
    
        return html.Div([
            html.H3(f"Patient ID: {patient_id}"),
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
        parsed_data =[json.loads(entry) for entry in all_data]
        return parsed_data
    return None

# fetch the last data entry from a redis list
def fetch_new_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    if latest_data:
        return json.loads(latest_data)
    return None

# update the graphs every second with new data
@callback(
    [Output('L0-live-graph', 'figure'),
    Output('L1-live-graph', 'figure'),
    Output('L2-live-graph', 'figure'),
    Output('R0-live-graph', 'figure'),
    Output('R1-live-graph', 'figure'),
    Output('R2-live-graph', 'figure')],
    [Input('interval-component', 'n_intervals')],
    [State('url', 'pathname')]
)
def update_graph(n, pathname):
    print('Entering the callback function.')
    global patient_data
    print(patient_data)

    patient_id = int(pathname.split('/')[-1])
    row_json = fetch_new_data(patient_id)

    if row_json:
        # convert the new data into a DataFrame containing 1 observation
        row_list = [
            row_json['time'],
            row_json['data']['firstname'],
            row_json['data']['lastname'],
            row_json['data']['trace']['id']
        ] + [
            s['anomaly'] for s in row_json['data']['trace']['sensors']
        ] + [
            s['value'] for s in row_json['data']['trace']['sensors']
        ]
        row_df = pd.DataFrame([row_list], columns='time firstname lastname trace_id anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

        if patient_id not in patient_data:
            # create an empty DataFrame if it's the 1st time this patient's live record has been accessed
            print(patient_data[patient_id])
            print('CREATING NEW DF!')
            patient_data[patient_id] = pd.DataFrame(columns='time firstname lastname trace_id anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())    

        df = patient_data[patient_id]
        df = pd.concat([df, row_df], ignore_index=True)
        if len(df) > 600:
            df = df.iloc[1:]

        patient_data[patient_id] = df
        print(df)

        updated_figures = []
        # Loop through the column names to update each graph
        for sensor in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2']:
            # Filter anomaly data where anomaly is True
            anomaly_indices = df[df[f'anomaly_{sensor}'] == True].index.tolist()
            
            fig = {
                'data': [
                    {
                        'x': df['time'],
                        'y': df[sensor],
                        'type': 'scatter',
                        'mode': 'lines',
                        'name': f'{sensor} (Normal)',
                        'showlegend': False
                    }, {
                        'x': df.loc[anomaly_indices, 'time'],
                        'y': df.loc[anomaly_indices, sensor],
                        'type': 'scatter',
                        'mode': 'lines',
                        'name': f'{sensor} (Anomaly)',
                        'line': {'color': 'red', 'width': 2},
                        'showlegend': False
                    }
                ],
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
                    'height': 200
                }
            }
            updated_figures.append(fig)

        # Return all updated figures for the graphs
        return updated_figures
    else:
        return [{'data': [], 'layout': {}}] * 6
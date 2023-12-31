import dash
from dash import html, dcc, callback, Input, Output, State
import redis
import json
import pandas as pd

def title(patient_id=None):
    return f'Patient {patient_id} - live'

dash.register_page(__name__, path_template='/live/<patient_id>', title=title)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Dictionary to store DataFrames for each patient
patient_data = {}

REGISTERED_PATIENTS = ['1', '2', '3', '4', '5', '6']

def layout(patient_id=None):
    if patient_id not in REGISTERED_PATIENTS:
        return html.Div(
            f'Patient ID: {patient_id} is invalid.'
        )

    return html.Div([
        dcc.Location(id='url', refresh=False),

        update_patient_info(patient_id),

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
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),  # Left column

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
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}), # Right column

        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ])
    
def update_patient_info(patient_id):
    row_json = fetch_data(patient_id)
    
    if row_json:
        return html.Div([
            html.H3(f"Patient ID: {patient_id}"),
            html.P(f"Name: {row_json['data']['firstname']} {row_json['data']['lastname']}"),
            html.P(f"Birth year: {row_json['data']['birthdate']}"),
            html.P(f"Disability: {row_json['data']['disabled']}")
        ])
    else:
        return html.Div("Patient information not found.")

# Function to fetch data from Redis based on the endpoint
def fetch_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    if latest_data:
        return json.loads(latest_data)
    return None

# Update graph with fetched data for different patients
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
    patient_id = int(pathname.split('/')[-1])  # Extract patient ID from the pathname
    row_json = fetch_data(patient_id)

    if row_json:
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
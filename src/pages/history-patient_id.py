import dash
from dash import html, dcc, callback, Input, Output, State
import redis
import json
import pandas as pd
import dash_bootstrap_components as dbc
from frontend import navbar, navbar2

def title(patient_id=None):
    return f'Patient {patient_id} - history'

dash.register_page(__name__, path_template='/history/<patient_id>', title=title)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Dictionary to store DataFrames for each patient
patient_data = {}
# current_streak_id = {}

REGISTERED_PATIENTS = ['1', '2', '3', '4', '5', '6']

def layout(patient_id=None):
    if patient_id not in REGISTERED_PATIENTS:
        return html.Div(
            f'Patient ID: {patient_id} is invalid.'
        )

    return html.Div([
        navbar.navbar,
        navbar2.navbar,

        dcc.Store('memory'),

        load_patient_data(patient_id)
    ])
    
def load_patient_data(patient_id):
    # global patient_data
    # global current_streak_id

    data = fetch_anomaly_data(patient_id)
    
    if data:
        row_list = [
            [
                row['streak_id'],
                row['timestamp'].split()[0],
                row['timestamp'].split()[1].split('.')[0],
                row['data']['firstname'],
                row['data']['lastname'],
                row['data']['trace']['id']
            ] + [s['value'] for s in row['data']['trace']['sensors']]
            for row in data
        ]
        patient_data[patient_id] = pd.DataFrame(row_list, columns='streak_id date time firstname lastname trace_id L0 L1 L2 R0 R1 R2'.split())
        print(patient_data[patient_id])
        
        return html.Div([
            dcc.Location(id='url', refresh=False),

            html.Div([
                html.P(f"Patient ID: {patient_id}"),
                html.P(f"Name: {data[0]['data']['firstname']} {data[0]['data']['lastname']}"),
                html.P(f"Birth year: {data[0]['data']['birthdate']}"),
                html.P(f"Disability: {data[0]['data']['disabled']}"),
                html.P(id='anomaly-date'),
                dbc.Button("Newest", color="primary", className="me-1", id='newest-button', n_clicks=0, disabled=True),
                dbc.Button("Newer", color="primary", className="me-1", id='newer-button', n_clicks=0, disabled=True),
                dbc.Button("Older", color="primary", className="me-1", id='older-button', n_clicks=0),
                dbc.Button("Oldest", color="primary", className="me-1", id='oldest-button', n_clicks=0),
                #html.Button('Newest', id='newest-button', n_clicks=0, disabled=True),
                #html.Button('Newer', id='newer-button', n_clicks=0, disabled=True),
                #html.Button('Older', id='older-button', n_clicks=0),
                #html.Button('Oldest', id='oldest-button', n_clicks=0)
            ]),
            html.Div([
                dcc.Graph(
                    id='L0-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
                dcc.Graph(
                    id='L1-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
                dcc.Graph(
                    id='L2-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),  # Left column

            html.Div([
                dcc.Graph(
                    id='R0-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
                dcc.Graph(
                    id='R1-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
                dcc.Graph(
                    id='R2-anomaly-graph',
                    style={'width': '100%', 'height': '200px'}
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}) # Right column
        ])
    else:
        return html.Div(f'No history of anomalies found for patient {patient_id}.')

# Function to fetch data from Redis based on the endpoint
def fetch_anomaly_data(patient_id):
    data_key = f'patient-{patient_id}-anomalies'
    data = redis_client.lrange(data_key, 0, -1)
    if data:
        parsed_data = [json.loads(entry) for entry in data]
        # print(parsed_data)
        return parsed_data
    return None

@callback(
    Output('anomaly-date', 'children'),
    Output('L0-anomaly-graph', 'figure'),
    Output('L1-anomaly-graph', 'figure'),
    Output('L2-anomaly-graph', 'figure'),
    Output('R0-anomaly-graph', 'figure'),
    Output('R1-anomaly-graph', 'figure'),
    Output('R2-anomaly-graph', 'figure'),
    Output('newest-button', 'disabled'),
    Output('newer-button', 'disabled'),
    Output('older-button', 'disabled'),
    Output('oldest-button', 'disabled'),
    Output('memory', 'data'),

    [Input('newest-button', 'n_clicks'),
    Input('newer-button', 'n_clicks'),
    Input('older-button', 'n_clicks'),
    Input('oldest-button', 'n_clicks')],

    [State('L0-anomaly-graph', 'figure'),
    State('url', 'pathname'),
    State('memory', 'data')]
)
def update_graph(newest_clicks, newer_clicks, older_clicks, oldest_clicks, figure, pathname, data):
    patient_id = pathname.split('/')[-1]
    df = patient_data[patient_id]
    max_streak_id = df['streak_id'].max()

    data = data or {
        'current_streak_id': max_streak_id
    }

    # Determine which button was clicked and adjust the streak_id accordingly
    if dash.ctx.triggered_id == 'newest-button':
        data['current_streak_id'] = max_streak_id
    if dash.ctx.triggered_id == 'newer-button':
        data['current_streak_id'] = min(max_streak_id, data['current_streak_id'] + 1)
    if dash.ctx.triggered_id == 'older-button':
        data['current_streak_id'] = max(1, data['current_streak_id'] - 1)
    if dash.ctx.triggered_id == 'oldest-button':
        data['current_streak_id'] = 1

    newest_diabled = data['current_streak_id'] == max_streak_id
    newer_diabled = data['current_streak_id'] == max_streak_id
    older_diabled = data['current_streak_id'] == 1
    oldest_diabled = data['current_streak_id'] == 1
    buttons_disabled = [newest_diabled, newer_diabled, older_diabled, oldest_diabled]

    # Fetch data based on the updated streak_id from df
    streak_data = df[df['streak_id'] == data['current_streak_id']]
    print(streak_data)

    anomaly_date = f"Anomaly date: {streak_data.iloc[0]['date']}"

    updated_figures = []
    # Loop through the column names to update each graph
    for sensor in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2']:
        fig = {
            'data': [{
                'x': streak_data['time'],
                'y': streak_data[sensor],
                'type': 'scatter',
                'mode': 'lines',
                'name': f'{sensor} (Anomaly)',
                'line': {'color': 'red', 'width': 2},
                'showlegend': False
            }],
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

    # Return all updated figures for the graphs, button states and data
    return anomaly_date, *updated_figures, *buttons_disabled, data
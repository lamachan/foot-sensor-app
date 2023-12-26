import dash
from dash import dcc, html, Output, Input, State
import plotly.graph_objs as go
import redis
import json
import pandas as pd

app = dash.Dash(__name__)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Dictionary to store DataFrames for each patient
patient_data = {}

# Define Dash layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(id='additional-info-div'),

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


# Update additional patient information callback
@app.callback(
    Output('additional-info-div', 'children'),
    [Input('url', 'pathname')]
)
def update_patient_info(pathname):
    patient_id = int(pathname.split('/')[-1])  # Extract patient ID from the pathname
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    row_json = json.loads(latest_data)
    
    if row_json:
        # row_list = [row_json['firstname'], row_json['lastname'], row_json['birthdate'], row_json['disabled']]
        # row_df = pd.DataFrame([row_list], columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

        return html.Div([
            html.H3(f"Patient ID: {patient_id}"),
            html.P(f"Name: {row_json['firstname']} {row_json['lastname']}"),
            html.P(f"Birth year: {row_json['birthdate']}"),
            html.P(f"Disability: {row_json['disabled']}")
        ])
    else:
        return html.Div("Patient information not found.")

# Function to fetch data from Redis based on the endpoint
def fetch_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    if patient_id not in patient_data:
        # Fetch all data from Redis if patient_data doesn't have the patient's data
        print('FETCHING ALL DATA')
        all_data = [json.loads(data) for data in redis_client.lrange(data_key, 0, -1)]
        return all_data
    else:
        # Fetch only the last data point if patient_data has the patient's data
        print('FETCHING 1 ROW OF DATA')
        latest_data = redis_client.lindex(data_key, -1)
        if latest_data:
            return [json.loads(latest_data)]
    return None

# Update graph with fetched data for different patients
@app.callback(
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
    data = fetch_data(patient_id)
    
    if data:
        row_list = [[row['birthdate'], row['disabled'], row['firstname'], row['id'], row['lastname'], row['trace']['id'], row['trace']['name']]
                + [s['anomaly'] for idx, s in enumerate(row['trace']['sensors'])]
                + [s['value'] for idx, s in enumerate(row['trace']['sensors'])]
                for row in data]
        # print(row_list)
        new_df = pd.DataFrame(row_list, columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

        # Update patient_data with new data
        if patient_id not in patient_data:
            print('DOES NOT EXIST, SETTING AS NEW')
            patient_data[patient_id] = new_df
        else:
            # Append only the last data point to the existing patient_data
            print('CONCAT')
            patient_data[patient_id] = pd.concat([patient_data[patient_id], new_df], ignore_index=True)

        if len(patient_data[patient_id]) > 600:
            print('OVER 600')
            patient_data[patient_id] = patient_data[patient_id].iloc[1:]

        # Get the updated DataFrame for the patient
        df = patient_data[patient_id]
        print(df)

        updated_figures = []

        # Loop through the column names to update each graph
        for sensor in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2']:
            fig = {
                'data': [
                    {'x': df.index, 'y': df[sensor], 'type': 'line', 'name': sensor}
                ],
                'layout': {
                    'title': f'{sensor} - Patient {patient_id}',
                    'xaxis': dict(title='Time'),
                    'yaxis': dict(title='Value')
                }
            }
            
            updated_figures.append(fig)

        return updated_figures
    else:
        return [{'data': [], 'layout': {}}] * 6  # Return empty figures for all graphs if no data found

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html
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
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Function to fetch data from Redis based on the endpoint
def fetch_data(patient_id):
    data_key = f'patient-{patient_id}-data'
    latest_data = redis_client.lindex(data_key, -1)
    if latest_data:
        return json.loads(latest_data)
    return None

# Update graph with fetched data for different patients
@app.callback(
    dash.dependencies.Output('live-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')],
    [dash.dependencies.State('url', 'pathname')]
)
def update_graph(n, pathname):
    patient_id = int(pathname.split('/')[-1])  # Extract patient ID from the pathname
    row_json = fetch_data(patient_id)

    if row_json:
        row_list = [row_json['birthdate'], row_json['disabled'], row_json['firstname'], row_json['id'], row_json['lastname'], row_json['trace']['id'], row_json['trace']['name']] + [s['anomaly'] for idx, s in enumerate(row_json['trace']['sensors'])] + [s['value'] for idx, s in enumerate(row_json['trace']['sensors'])]
        row_df = pd.DataFrame([row_list], columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

        if patient_id not in patient_data:
            print('CREATING NEW DF!')
            patient_data[patient_id] = pd.DataFrame(columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

        df = patient_data[patient_id]
        df = pd.concat([df, row_df], ignore_index=True)
        if len(df) > 600:
            df = df.iloc[1:]

        patient_data[patient_id] = df
        print(df)

        x = df.index
        y = df['L0']

        trace = go.Scatter(
            x=x,
            y=y,
            mode='lines'
        )

        layout = go.Layout(
            title=f'Real-time Data Graph - Patient {patient_id}',
            xaxis=dict(
                title='Time'
            ),
            yaxis=dict(
                title='Value'
            )
        )

        return {'data': [trace], 'layout': layout}
    else:
        return {'data': [], 'layout': {}}

if __name__ == '__main__':
    app.run_server(debug=True)
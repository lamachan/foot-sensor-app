import dash
from dash import dcc, html
import plotly.graph_objs as go
import redis
import json
import pandas as pd

app = dash.Dash(__name__)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

df = pd.DataFrame(columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

# Define Dash layout
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Update graph with fetched data
@app.callback(
    dash.dependencies.Output('live-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global df
    # Fetch the stored data from Redis
    latest_data = redis_client.lindex('my_data_list', -1)

    row_json = json.loads(latest_data)

    row_list = [row_json['birthdate'], row_json['disabled'], row_json['firstname'], row_json['id'], row_json['lastname'], row_json['trace']['id'], row_json['trace']['name']] + [s['anomaly'] for idx, s in enumerate(row_json['trace']['sensors'])] + [s['value'] for idx, s in enumerate(row_json['trace']['sensors'])]
    row_df = pd.DataFrame([row_list], columns='birthdate disabled firstname id lastname trace_id name anomaly_L0 anomaly_L1 anomaly_L2 anomaly_R0 anomaly_R1 anomaly_R2 L0 L1 L2 R0 R1 R2'.split())

    df = pd.concat([df, row_df], ignore_index=True)

    if len(df) > 600:
        df = df.iloc[1:]

    print(df)

    # Create x and y coordinates for the line graph
    x = df.index  # Use DataFrame index as x-axis
    y = df['L0']

    # Create a Plotly trace for the line graph
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines'
    )

    # Define the layout for the graph
    layout = go.Layout(
        title='Real-time Data Graph',
        xaxis=dict(
            title='Time'
        ),
        yaxis=dict(
            title='Value'
        )
    )

    return {'data': [trace], 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import html
import dash_bootstrap_components as dbc

import threading
import requests
import redis
import time
import json
from datetime import datetime

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,  external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    dash.page_container
])

def fetch_data_from_api(api_url, redis_client):
    while True:
        try:
            patient_id = api_url[-1]
            response = requests.get(api_url, timeout=0.5)
            
            data = response.json()
            timestamped_data = {'time': str(datetime.now().strftime('%H:%M:%S')), 'data': data}
            
            # store 10 minutes of live data in a redis list 'patient-[idx]-data'
            redis_client.rpush(f'patient-{patient_id}-data', json.dumps(timestamped_data))
            redis_client.ltrim(f'patient-{patient_id}-data', -600, -1)

            # detect anomaly streak and store it with the correct streak_id in a redis list 'patient-[idx]-anomalies'
            anomalies = [s['anomaly'] for s in data['trace']['sensors']]
            if any(anomalies):
                if not previous_anomaly[i-1]:
                    next_anomaly_streak_id[i-1] += 1
                    previous_anomaly[i-1] = True

                anomaly_data = {'streak_id': next_anomaly_streak_id[i-1], 'timestamp': str(datetime.now()), 'data': data}
                print(anomaly_data)
                redis_client.rpush(f'patient-{patient_id}-anomalies', json.dumps(anomaly_data))
            else:
                print(f'patient {patient_id} no anomaly')
                previous_anomaly[i-1] = False

        except requests.Timeout as e:
            print(f'Timeout for patient {patient_id}: {e}')
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching and storing data for patient {patient_id}: {e}")
            time.sleep(1)
        time.sleep(1)

if __name__ == '__main__':
    redis_host = 'localhost'
    redis_port = 6379
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    api_endpoints = [f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}' for i in range(1,7)]

    next_anomaly_streak_id = list(range(6))
    previous_anomaly = list(range(6))
    for i in range(1,7):
        redis_client.delete(f'patient-{i}-data')

        last_anomaly_data = redis_client.lindex(f'patient-{i}-anomalies', -1)
        if last_anomaly_data:
            next_anomaly_streak_id[i-1] = json.loads(last_anomaly_data)['streak_id']
        else:
            next_anomaly_streak_id[i-1] = 0

        previous_anomaly[i-1] = False

    print(next_anomaly_streak_id)
    print(previous_anomaly)

    threads = []
    for endpoint in api_endpoints:
        thread = threading.Thread(target=fetch_data_from_api, args=(endpoint, redis_client))
        threads.append(thread)

    for thread in threads:
        thread.start()

    app.run_server(debug=True)
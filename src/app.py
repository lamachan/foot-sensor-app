import dash
from dash import html
import dash_bootstrap_components as dbc

import threading
import requests
import redis
import time
import json
from datetime import datetime

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    dash.page_container
])

# fetching data for 1 patient every 1 second and storing it in redis lists
def fetch_data_from_api(api_url, redis_client, next_anomaly_streak_id, previous_anomaly):
    while True:
        try:
            patient_id = api_url[-1]
            response = requests.get(api_url, timeout=0.5)
            
            data = response.json()
            timestamped_data = {'time': str(datetime.now().strftime('%H:%M:%S')), 'data': data}
            
            redis_client.rpush(f'patient-{patient_id}-data', json.dumps(timestamped_data))
            redis_client.ltrim(f'patient-{patient_id}-data', -600, -1)

            # detect anomaly trace
            anomalies = [s['anomaly'] for s in data['trace']['sensors']]
            if any(anomalies):
                if not previous_anomaly:
                    next_anomaly_streak_id += 1
                    previous_anomaly = True

                anomaly_data = {'streak_id': next_anomaly_streak_id, 'timestamp': str(datetime.now()), 'data': data}
                redis_client.rpush(f'patient-{patient_id}-anomalies', json.dumps(anomaly_data))
            else:
                previous_anomaly = False

        except requests.Timeout as e:
            print(f'Timeout for patient {patient_id}: {e}')
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching and storing data for patient {patient_id}: {e}")
            time.sleep(1)
        else:
            time.sleep(1)

if __name__ == '__main__':
    # prepare redis DB
    redis_host = 'localhost'
    redis_port = 6379
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

    next_anomaly_streak_id = {}
    previous_anomaly = {}

    for patient_id in range(1, 7):
        redis_client.delete(f'patient-{patient_id}-data')

        last_anomaly_data = redis_client.lindex(f'patient-{patient_id}-anomalies', -1)
        if last_anomaly_data:
            next_anomaly_streak_id[patient_id] = json.loads(last_anomaly_data)['streak_id']
        else:
            next_anomaly_streak_id[patient_id] = 0

        previous_anomaly[patient_id] = False

    # set up threads for each patient
    threads = []
    for patient_id in range(1, 7):
        thread = threading.Thread(target=fetch_data_from_api, args=(
            f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient_id}',
            redis_client,
            next_anomaly_streak_id[patient_id],
            previous_anomaly[patient_id]
        ))
        threads.append(thread)

    for thread in threads:
        thread.start()

    app.run_server(debug=False, host="0.0.0.0", port=8080)
import time
from datetime import datetime
import requests
import redis
import json

# initialize Redis database
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
# redis_client.flushdb()
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

# fetching live and anomaly data from the API for all 6 patients
def fetch_and_store_data():
    while True:
        for i in range(1,7):
            try:
                response = requests.get(f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}', timeout=0.1)
                
                data = response.json()
                timestamped_data = {'time': str(datetime.now().strftime('%H:%M:%S')), 'data': data}
                
                # store 10 minutes of live data in a redis list 'patient-[idx]-data'
                redis_client.rpush(f'patient-{i}-data', json.dumps(timestamped_data))
                redis_client.ltrim(f'patient-{i}-data', -600, -1)

                # detect anomaly streak and store it with the correct streak_id in a redis list 'patient-[idx]-anomalies'
                anomalies = [s['anomaly'] for s in data['trace']['sensors']]
                if any(anomalies):
                    if not previous_anomaly[i-1]:
                        next_anomaly_streak_id[i-1] += 1
                        previous_anomaly[i-1] = True

                    anomaly_data = {'streak_id': next_anomaly_streak_id[i-1], 'timestamp': str(datetime.now()), 'data': data}
                    print(anomaly_data)
                    redis_client.rpush(f'patient-{i}-anomalies', json.dumps(anomaly_data))
                else:
                    print(f'patient {i} no anomaly')
                    previous_anomaly[i-1] = False

            except requests.Timeout as e:
                print(f'Timeout for patient {i}: {e}')
                time.sleep(0.01)
            except Exception as e:
                print(f"Error fetching and storing data for patient {i}: {e}")
                time.sleep(1)
        # wait for less than a second (about 1 s including the fetching) for the next fetch
        time.sleep(0.5)
       
fetch_and_store_data()
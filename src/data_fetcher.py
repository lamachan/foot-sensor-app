import time
from datetime import datetime
import requests
import redis
import json

# Initialize Redis connection
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

# Function to fetch data from a website and store it in Redis
def fetch_and_store_data():
    while True:
        # print(f'Time before fetch: {time.time()}')
        for i in range(1,7):
            try:
                # Make a request to the website to fetch data
                response = requests.get(f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}', timeout=0.1)
                
                # Extract the data from the response (assuming JSON format here)
                data = response.json()
                timestamped_data = {'time': str(datetime.now().strftime('%H:%M:%S')), 'data': data}
                
                # Store the data in a Redis list (right-push)
                redis_client.rpush(f'patient-{i}-data', json.dumps(timestamped_data))
                # print(f'Patient {i} fetched')
                
                # Trim the list to keep only the last 600 elements (10 minutes worth of data)
                redis_client.ltrim(f'patient-{i}-data', -600, -1)

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
                # If an error occurs, wait for 1 second before retrying
                time.sleep(1)
        # print(f'Time after fetch: {time.time()}')
        # Wait for 1 second before fetching data again
        time.sleep(0.8)
       
# Start fetching and storing data in Redis
fetch_and_store_data()
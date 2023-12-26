import time
import requests
import redis
import json

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Function to fetch data from a website and store it in Redis
def fetch_and_store_data():
    while True:
        try:
            for i in range(1,7):
                # Make a request to the website to fetch data
                response = requests.get(f'http://tesla.iem.pw.edu.pl:9080/v2/monitor/{i}')
                
                # Extract the data from the response (assuming JSON format here)
                data = response.json()
                print(data)
                
                # Store the data in a Redis list (right-push)
                redis_client.rpush(f'patient-{i}-data', json.dumps(data))
                
                # Trim the list to keep only the last 600 elements (10 minutes worth of data)
                redis_client.ltrim(f'patient-{i}-data', -600, -1)
            
            # Wait for 1 second before fetching data again
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching and storing data for patient {i}: {e}")
            # If an error occurs, wait for 1 second before retrying
            time.sleep(1)

# Start fetching and storing data in Redis
fetch_and_store_data()
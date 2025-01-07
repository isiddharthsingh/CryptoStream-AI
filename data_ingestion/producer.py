import json
import time
from confluent_kafka import Producer
import requests

# Load configurations
with open('config.json') as f:
    config = json.load(f)

API_URL = config['api_url']
KAFKA_TOPIC = config['kafka_topic']
KAFKA_SERVER = config['kafka_server']
COINS = config['coins']  

# Configure Kafka Producer
conf = {'bootstrap.servers': KAFKA_SERVER}
producer = Producer(conf)

def fetch_data(coin):
    """Fetch price data for a given coin."""
    url = API_URL.format(coin=coin)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data for {coin} from Coinbase API")

def delivery_report(err, msg):
    """Delivery report handler called on successful or failed message delivery."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_messages():
    while True:
        for coin in COINS:  # Loop through all supported coins
            try:
                # Fetch data for the current coin
                data = fetch_data(coin)
                message = {
                    "data": {
                        "amount": data["data"]["amount"],
                        "base": coin,
                        "currency": "USD"
                    }
                }

                # Send the message to Kafka
                producer.produce(KAFKA_TOPIC, key=None, value=json.dumps(message), callback=delivery_report)
                producer.flush()
                print(f"Produced: {message}")

            except Exception as e:
                print(f"Error fetching data for {coin}: {e}")

        # Wait before the next fetch
        time.sleep(10)

if __name__ == "__main__":
    produce_messages()
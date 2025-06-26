import requests
import json
import time
from kafka import KafkaProducer
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Binance API URL for ETHUSDT
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

#kafka config
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Change this to your Kafka broker address

#Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS,
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def fetch_eth_price():
    '''Fetch ETH current price from Binance API'''
    try:
        response = requests.get(BINANCE_API_URL)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        return {
            "symbol": data["symbol"],
            "price": float(data['price']),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"[ERROR] failed to fetch ETH price: {e}")
        return None
    
def run_producer():
    '''Run the Kafka producer to send ETH price data'''
    print("[INFO] Starting Kafka prodcuer for ETH price")
    while True:
        eth_price_data = fetch_eth_price()
        if eth_price_data:
            print(f"[INFO] Sending data: {eth_price_data}")
            producer.send(KAFKA_TOPIC, eth_price_data)
        time.sleep(15) # Sleep for 15 sec before next fetch

if __name__ == "__main__":
    try:
        run_producer()
    except KeyboardInterrupt:
        print("[INFO] Stopping Kafka producer")
    finally:
        producer.flush()
        producer.close()
        print("[INFO] Kafka producer stopped")
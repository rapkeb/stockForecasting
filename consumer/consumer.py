from confluent_kafka import Consumer
import requests


# Kafka Configuration
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'interaction-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['user-interactions'])

def send_to_db(message):
    url = 'http://db:80/write_user_interaction'  # Replace with your service's URL
    payload = {"message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Message sent to DB service: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to DB service: {e}")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    # Process the message
    message = msg.value().decode('utf-8')
    print(f"Received message: {message}")
    send_to_db(message)

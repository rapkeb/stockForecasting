from confluent_kafka import Consumer
import requests
import threading
import time


def create_consumer(group_id, topic):
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])
    return consumer

def consume_messages(consumer, topic):
    def send_to_db(message, topic):
        url = 'http://db:80/write_user_interaction'
        current_time = time.time()
        payload = {"message": message, "topic": topic, "time": current_time}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print(f"Message sent to DB service: {message}, Topic: {topic}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to DB service: {e}")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        message = msg.value().decode('utf-8')
        print(f"Received message: {message}")
        send_to_db(message, topic)

# Creating consumers for different topics
topics = ['shares', 'login', 'buy']
group_ids = ['shares-consumer-group', 'login-consumer-group', 'buy-consumer-group']

for group_id, topic in zip(group_ids, topics):
    consumer = create_consumer(group_id, topic)
    threading.Thread(target=consume_messages, args=(consumer, topic)).start()
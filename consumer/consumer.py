from confluent_kafka import Consumer

# Kafka Configuration
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'interaction-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['user-interactions'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    # Process the message
    print(f"Received message: {msg.value().decode('utf-8')}")
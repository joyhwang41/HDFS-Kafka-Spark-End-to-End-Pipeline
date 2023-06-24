from kafka import KafkaProducer, KafkaConsumer


# Initialize the Kafka Consumer


# Initialize the Kafka consumer
consumer = KafkaConsumer(bootstrap_servers='localhost:9092', group_id='my_group')

# Subscribe to a Kafka topic
topic = 'all_info'
consumer.subscribe([topic])

# Consume messages from the topic
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")

# Close the consumer


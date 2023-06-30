from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
# LOG_FILE = '16GBFile.log-001'
LOG_FILE = '../hw2/40MBFile.log'



def create_producer():
    while True:
        try:
            return KafkaProducer(bootstrap_servers='kafka:9092')
        except NoBrokersAvailable:
            print("Kafka broker is not available, retrying in 5 seconds...")
            time.sleep(5)

producer = create_producer()
with open(LOG_FILE, 'r') as file:
    for line in file:
        producer.send('log', line)
        print(f'sending log == > {line}')
        time.sleep(0.1)  # Pause to avoid overloading Kafka

producer.close()

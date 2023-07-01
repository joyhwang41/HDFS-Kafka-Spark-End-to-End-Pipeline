from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
# LOG_FILE = '16GBFile.log-001'
LOG_FILE = './40MBFile.log'



def create_producer():
    while True:
        try:
            return KafkaProducer(bootstrap_servers='kafka:9092')
        except NoBrokersAvailable:
            print("Kafka broker is not available, retrying in 5 seconds...")
            time.sleep(5)

producer = create_producer()
with open(LOG_FILE, 'r') as file:
    print(f'starting reading file')
    while log:= file.readline():
        log = log.encode('utf-8')
        producer.send('log', log)
        print(f'sending log == > {log}')
        time.sleep(0.1)  # Pause to avoid overloading Kafka

producer.close()

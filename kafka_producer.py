from kafka import KafkaProducer
from data_generator import generate_log
from main import FILE_PATH
from time import sleep


producer = KafkaProducer(bootstrap_servers='localhost:9092')
log_gen  = generate_log(FILE_PATH)


def main():
    
    # Send a message to a Kafka topic
    topic = 'all_info'

    while message:=next(log_gen):
        byte_message = message.encode('utf-8')
        producer.send(topic, value=byte_message)
        print(f'producing {message=}')
        sleep(5)

    producer.flush()  # Wait until all messages are sent
    producer.close()  # Close the producer
        

if __name__ == "__main__":
    main()

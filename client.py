import pika
import json
import random
import time

RABBITMQ_HOST = 'localhost'
RABBITMQ_EXCHANGE = 'status_exchange'
RABBITMQ_ROUTING_KEY = 'status_topic'

def main():
    credentials = pika.PlainCredentials("user", "password")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

    while True:
        status = random.randint(0, 6)
        message = json.dumps({"status": status})
        channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key=RABBITMQ_ROUTING_KEY, body=message)
        print(f"Published message: {message}")
        time.sleep(1)

    connection.close()

if __name__ == "__main__":
    main()

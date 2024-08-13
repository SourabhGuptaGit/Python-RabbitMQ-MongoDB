import pika
import json
import pymongo
from pymongo import MongoClient
import datetime

RABBITMQ_HOST = 'localhost'
RABBITMQ_EXCHANGE = 'status_exchange'
RABBITMQ_ROUTING_KEY = 'status_topic'
RABBITMQ_USER = 'user'       # Replace with your RabbitMQ username
RABBITMQ_PASSWORD = 'password'  # Replace with your RabbitMQ password

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "status_collection"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def callback(ch, method, properties, body):
    message = json.loads(body)
    message["timestamp"] = datetime.datetime.utcnow()
    collection.insert_one(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Stored message: {message}")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the exchange and the queue
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)
    queue_name = channel.queue_declare(queue='', exclusive=True).method.queue

    # Bind the queue to the exchange with the routing key
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=queue_name, routing_key=RABBITMQ_ROUTING_KEY)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()

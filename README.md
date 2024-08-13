# MQTT Messaging System with RabbitMQ and MongoDB

## Overview

This project implements a client-server system that uses MQTT messaging via RabbitMQ and stores the data in MongoDB. The system is designed to publish, process, and query IoT data effectively. It consists of three primary components:

- **`client.py`**: Publishes MQTT messages to RabbitMQ.
- **`server.py`**: Consumes MQTT messages from RabbitMQ and stores them in MongoDB.
- **`api.py`**: Provides an HTTP API to query the stored data in MongoDB.

## Architecture

### 1. **Client (`client.py`)**

**Functionality**:
- Connects to RabbitMQ and publishes MQTT messages to a specified topic.
- Generates random `status` values between 0 and 6 and sends them as JSON messages.

**Components**:
- **RabbitMQ Connection**: Establishes a connection to RabbitMQ using the provided credentials.
- **Exchange Declaration**: Declares an exchange named `status_exchange` of type `topic`.
- **Message Publishing**: Publishes JSON-encoded messages to the `status_topic` routing key.

**Workflow**:
1. Connect to RabbitMQ.
2. Declare the exchange if it doesn't exist.
3. Generate a random status value.
4. Publish the message to the exchange.
5. Repeat every second.

### 2. **Server (`server.py`)**

**Functionality**:
- Subscribes to the RabbitMQ exchange and processes incoming messages.
- Stores messages in MongoDB with an additional timestamp field for tracking.

**Components**:
- **RabbitMQ Subscription**: Connects to RabbitMQ, declares the exchange, and binds a temporary queue to it.
- **Message Processing**: Reads messages from RabbitMQ and inserts them into MongoDB.
- **MongoDB Storage**: Uses the `pymongo` library to insert messages into a MongoDB collection.

**Workflow**:
1. Connect to RabbitMQ.
2. Declare and bind the queue to the `status_exchange`.
3. Consume messages from the queue.
4. Parse and store messages in MongoDB with timestamps.
5. Acknowledge message receipt.

### 3. **API (`api.py`)**

**Functionality**:
- Provides a RESTful API endpoint to retrieve the count of messages by status within a specified time range.

**Components**:
- **Flask API**: Creates an HTTP endpoint to handle GET requests.
- **MongoDB Query**: Uses MongoDB’s aggregation framework to count messages by status within the given time range.

**Workflow**:
1. Accept `start` and `end` query parameters in ISO 8601 format.
2. Query MongoDB using an aggregation pipeline.
3. Return a JSON response with status counts.

## Setup with Docker

To run RabbitMQ and MongoDB using Docker, use the following commands:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:management
docker run -d --name mongodb -p 27017:27017 mongo

import os

import pika

USER = os.getenv("RABBITMQ_DEFAULT_USER")
PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
BROKER_HOSTNAME = os.getenv("BROKER_HOSTNAME")
WEB_HOSTNAME = os.getenv("WEB_HOSTNAME")

QUEUE_NAME = os.getenv("RABBIT_QUEUE_NAME")

CONNECTION_URL = f'amqp://{USER}:{PASSWORD}@{BROKER_HOSTNAME}:5672/%2f'


def publish_task(task: str):
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION_URL))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=task.encode('utf-8'))
    channel.close()
    connection.close()
import os, sys

import json

import pika
import requests


USER = os.getenv("RABBITMQ_DEFAULT_USER")
PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
BROKER_HOSTNAME = os.getenv("BROKER_HOSTNAME")
WEB_HOSTNAME = os.getenv("WEB_HOSTNAME")
WEB_PORT = os.getenv("WEB_PORT")

QUEUE_NAME = os.getenv("RABBIT_QUEUE_NAME")

CONNECTION_URL = f'amqp://{USER}:{PASSWORD}@{BROKER_HOSTNAME}:5672/%2f'


def handle_message(ch, method, properties, body):
    body_str = body.decode('utf-8')
    link_json = json.loads(body_str)
    
    response = requests.get(link_json['url'], timeout=10)
    status = response.status_code
    
    payload = {'id': int(link_json['id']), 'status': str(status)}
    payload_json = json.dumps(payload)
    
    requests.put(f'http://{WEB_HOSTNAME}:{WEB_PORT}/links/', data=payload_json)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION_URL))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=handle_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
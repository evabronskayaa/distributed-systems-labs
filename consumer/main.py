import os, sys
from typing import Optional

import json

import pika
import requests

import redis


USER = os.getenv("RABBITMQ_DEFAULT_USER")
PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS") 
BROKER_HOSTNAME = os.getenv("BROKER_HOSTNAME")
QUEUE_NAME = os.getenv("RABBIT_QUEUE_NAME")

WEB_HOSTNAME = os.getenv("WEB_HOSTNAME")
WEB_PORT = os.getenv("WEB_PORT")

CACHE_HOSTNAME = os.getenv("CACHE_HOSTNAME")
CACHE_PORT = os.getenv("CACHE_PORT")




CONNECTION_URL = f'amqp://{USER}:{PASSWORD}@{BROKER_HOSTNAME}:5672/%2f'
print(CONNECTION_URL)

redis_cache = redis.Redis(host=CACHE_HOSTNAME, port=int(CACHE_PORT), db=0)


def get_link_status(link: str) -> str:
    key = f"url-{link}"
    status = get_status_from_cache(key)
    if status is None:
        status = fetch_status_from_inet(link)
        update_status_in_cache(key, status)
    return status


def get_status_from_cache(key: str) -> Optional[str]:
    value = redis_cache.get(key)
    return None if value is None else value.decode("utf-8")


def update_status_in_cache(key: str, status_code: str) -> None:
    res = redis_cache.set(name=key, value=status_code)
    print(res)


def fetch_status_from_inet(link: str) -> str:
    response = requests.get(link, timeout=10)
    status = str(response.status_code)
    return status


def handle_message(ch, method, properties, body):
    body_str = body.decode('utf-8')
    link_json = json.loads(body_str)
    status = get_link_status(link_json['url'])
    print(status)

    payload = {'id': int(link_json['id']), 'status': str(status)}
    payload_json = json.dumps(payload)

    requests.put(f'http://{WEB_HOSTNAME}:{WEB_PORT}/links/', data=payload_json)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(CONNECTION_URL))
    print(connection)
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
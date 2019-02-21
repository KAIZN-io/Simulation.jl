import logging
import json
import pika

from values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS


logger = logging.getLogger(__name__)

def on(event_name):
    def decorator(callback):

        def callback_wrapper(ch, method, properties, body):
            data = json.loads(body)
            callback(ch, method, properties, body)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(
            exchange=EXCHANGE_EVENTS,
            queue=queue_name,
            routing_key=event_name
        )

        channel.basic_consume(callback_wrapper, queue=queue_name)

        channel.start_consuming()

    return decorator

def emit(event_name, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

    channel.basic_publish(
        exchange=EXCHANGE_EVENTS,
        routing_key=event_name,
        body=json.dumps(data)
    )

    connection.close()


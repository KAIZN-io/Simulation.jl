import eventlet
eventlet.monkey_patch()

import logging
import json
import pika
import datetime

from values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS, RFC3339_DATE_FORMAT


logger = logging.getLogger(__name__)

def on(event_name, durable_for_service_name = None):
    def decorator(callback):
        def callback_wrapper(ch, method, properties, body):
            data = json.loads(body)
            callback(ch, method, properties, body)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

        if durable_for_service_name:
            service_scoped_queue_name = durable_for_service_name + '_' + event_name
            result = channel.queue_declare(queue=service_scoped_queue_name)

            channel.basic_qos(prefetch_count=1)
        else:
            result = channel.queue_declare(exclusive=True)

        queue_name = result.method.queue

        channel.queue_bind(
            exchange=EXCHANGE_EVENTS,
            queue=queue_name,
            routing_key=event_name
        )

        channel.basic_consume(callback_wrapper, queue=queue_name)

        eventlet.spawn(channel.start_consuming)

        print('Registered function \'' + callback.__name__ + '\' as listener for event \'' + event_name + '\' on queue \'' + result.method.queue + '\'')

    return decorator

def emit(event_name, data):

    event = {
        'emitted_at': datetime.datetime.utcnow().strftime(RFC3339_DATE_FORMAT),
        'payload': data
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

    channel.basic_publish(
        exchange=EXCHANGE_EVENTS,
        routing_key=event_name,
        body=json.dumps(event)
    )

    connection.close()


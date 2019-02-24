import eventlet
eventlet.monkey_patch()

import logging
import json
import pika
import datetime

from values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS, RFC3339_DATE_FORMAT


logger = logging.getLogger(__name__)

def on(event_name, durable_for_service_name = None):
    """
    The `on` decorator for listening to events

    This function should be used as a decorator to execute the decorated function, whenever
    the passed event occurs.

    It serves just to collect the event name and the service name.

    The actual decorator is defined below and will just be returned by this function.
    """

    def decorator(callback):
        """
        The actual decorating function

        This function takes another function `callback` and decorates it.
        We open an connection to our message broker, set up a queue and then start and
        async `basic_consume`.
        The event name will be used as the routing key for binding the setup queue to the
        `events` exchange.

        When passed `durable_for_service_name` we do not create an anonymous queue, but a
        named one. The name will be the passed service name plus the event name. This way
        we make sure other containers of the same service can connect to the same queue,
        while still having separated queues for each event and thus no need to manually
        distinguish the events here.
        This might not be the most efficient solution, but a robust one. With a selfmade
        event mapper the potential for errors rises significantly. I might add such code in
        the future, but only with intensive testing.
        """

        # The callback executet when we receive a message from the broker
        def callback_wrapper(ch, method, properties, body):

            # try to parse the message as JSON, if it fails, discard
            try:
                data = json.loads(body)
            except ValueError as e:
                # discard the message from the queue
                ch.basic_nack(delivery_tag = method.delivery_tag, requeue = False)
                print(str(e))
                return

            callback(ch, method, properties, data)

        # Establish connection to the message broker
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
        channel = connection.channel()

        # Declare the one and only `events` exchange
        channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

        if durable_for_service_name:
            # When passed a service name, create a name for the queue and create it
            service_scoped_queue_name = durable_for_service_name + '_' + event_name
            result = channel.queue_declare(queue=service_scoped_queue_name)

            # Also tweak the qos to make sure every worker gets a piece of the cake
            channel.basic_qos(prefetch_count=1)
        else:
            # When no service name is specified, we just create an anonymous and exclusive queue
            result = channel.queue_declare(exclusive=True)

        # Either way, we get the name of the queue like this
        queue_name = result.method.queue

        # We bind the queue to the `events` exchange using the event name as routing key
        channel.queue_bind(
            exchange=EXCHANGE_EVENTS,
            queue=queue_name,
            routing_key=event_name
        )

        # Set the callback and for the queue and start to consume asynchronously
        channel.basic_consume(callback_wrapper, queue=queue_name)
        eventlet.spawn(channel.start_consuming)

        print('Registered function \'' + callback.__name__ + '\' as listener for event \'' + event_name + '\' on queue \'' + result.method.queue + '\'')

    # We need to return the decorator, otherwise nothing will work
    return decorator

def emit(event):
    """
    Emit an event via the RabbitMQ message broker

    Calling this function connects to the mesage broker and emits the data unter the specified
    event name. The event name is used as a routing key for the `events` exchange.
    The passed data will be wrapped in a dict that contains some additional informations about
    the event.

    All data must be JSON serializeable.
    """

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

    channel.basic_publish(
        exchange=EXCHANGE_EVENTS,
        routing_key=event['type'],
        body=json.dumps(event)
    )

    connection.close()


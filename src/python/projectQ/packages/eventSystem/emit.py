import logging
import pika

from values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS
from eventSystem.Event import Event


logger = logging.getLogger(__name__)

def emit(event):
    """
    Emit an event via the RabbitMQ message broker

    Calling this function connects to the mesage broker and emits the data unter the specified
    event name. The event name is used as a routing key for the `events` exchange.
    The passed data will be wrapped in a dict that contains some additional informations about
    the event.

    All data must be JSON serializeable.
    """

    assert isinstance(event, Event)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_EVENTS, exchange_type='topic')

    channel.basic_publish(
        exchange=EXCHANGE_EVENTS,
        routing_key=event.get_routing_key(),
        body=event.to_str()
    )

    connection.close()


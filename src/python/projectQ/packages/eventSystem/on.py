import eventlet
import pika

from projectQ.packages.values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS
from projectQ.packages.eventSystem.Event import Event
from projectQ.packages.eventSystem.RobustConsumer import RobustConsumer


def on(event_class, durable_for_service_name = None):
    """
    The `on` decorator for listening to events

    This function should be used as a decorator to execute the decorated function, whenever
    the passed event occurs.

    It serves just to collect the event name and the service name.

    The actual decorator is defined below and will just be returned by this function.
    """

    assert issubclass(event_class, Event)
    assert isinstance(durable_for_service_name, str) or durable_for_service_name is None

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
                event = event_class.from_str(body)
            except ValueError as e:
                # discard the message from the queue
                ch.basic_nack(delivery_tag = method.delivery_tag, requeue = False)
                print(str(e))
                return

            callback(ch, method, properties, event, event.get_payload())

        if durable_for_service_name:
            # When passed a service name, create a name for the queue and create it
            queue = durable_for_service_name + '_' + event_class.get_routing_key()
        else:
            # When no service name is specified, we just create an anonymous and exclusive queue
            queue = None

        consumer = RobustConsumer(callback_wrapper, event_class, queue)

        eventlet.spawn_n(consumer.start)

        print('Registered function \'' + callback.__name__ + '\' as listener for event \'' + event_class.get_routing_key() + '\' on queue \'' + str(queue) + '\'')

    # We need to return the decorator, otherwise nothing will work
    return decorator


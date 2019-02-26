import eventlet
eventlet.monkey_patch()

import pika

from values import HN_MESSAGE_BROKER, EXCHANGE_EVENTS
from eventSystem.Event import Event


class RobustConsumer:
    """
    The RobustConsumer automatically reconnects to the message broker in case of an error.

    The structure of this consumer orients itself on the async consumer example give by pika.
    This makes the structure somewhat bloated. But you can more or less simply read it from
    top to bottom as the data will flow this way as well.
    """
    def __init__(self, callback, event_class, queue=None, prefetch_count=1, reconnect_timeout=5):
        assert callable(callback)
        assert issubclass(event_class, Event)
        assert isinstance(queue, str) or queue is None
        assert isinstance(prefetch_count, int)
        assert isinstance(reconnect_timeout, int)

        print('init')
        self._callback = callback
        self._event_class = event_class
        self._queue = queue

        self._connection = None
        self._prefetch_count = prefetch_count
        self._reconnect_timeout = reconnect_timeout

    def _connect(self):
        print('Connecting...')
        self._connection = pika.SelectConnection(
            parameters             = pika.ConnectionParameters(host=HN_MESSAGE_BROKER),
            on_open_callback       = self._on_connection_opened,
            on_open_error_callback = self._on_connection_open_error,
            on_close_callback      = self._on_connection_closed
        )

    def _on_connection_opened(self, connection):
        print('Connected.')
        self._open_channel()

    def _on_connection_open_error(self, connection, reason):
        print('Connection closed, reason: ' + str(reason) + '. Reconnecting in 5 seconds.')
        self._reconnect()

    def _on_connection_closed(self, connnection, reason, hea):
        print('Connection closed, reason: ' + str(reason) + '. Reconnecting in 5 seconds.')
        self._reconnect()

    def _reconnect(self):
        print('Retrying...')
        self.stop()
        eventlet.sleep(self._reconnect_timeout)
        self.start()

    def _open_channel(self):
        print('Opening channel...')
        self._channel = self._connection.channel(
            on_open_callback=self._on_channel_opened
        )

    def _on_channel_opened(self, channel):
        print('Channel opened.')
        if self._queue:
            self._set_qos()
        else:
            self._declare_exchange()

    def _set_qos(self):
        print('Setting QoS...')
        self._channel.basic_qos(
            prefetch_count = self._prefetch_count,
            callback       = self._on_qos_set
        )

    def _on_qos_set(self, frame):
        print('QoS set.')
        self._declare_exchange()

    def _declare_exchange(self):
        print('Declaring exchange...')
        self._channel.exchange_declare(
            exchange      = EXCHANGE_EVENTS,
            exchange_type = 'topic',
            callback      = self._on_exchange_declared
        )

    def _on_exchange_declared(self, frame):
        print('Exchange declared.')
        self._declare_queue()

    def _declare_queue(self):
        print('Declaring queue...')
        if self._queue:
            self._channel.queue_declare(
                queue    = self._queue,
                callback = self._on_queue_declared
            )
        else:
            self._channel.queue_declare(
                exclusive = True,
                callback  = self._on_queue_declared
            )

    def _on_queue_declared(self, frame):
        print('Queue delcared.')
        self._queue = frame.method.queue
        self._bind_queue()

    def _bind_queue(self):
        print('Binding queue...')
        self._channel.queue_bind(
            exchange    = EXCHANGE_EVENTS,
            queue       = self._queue,
            routing_key = self._event_class.get_routing_key(),
            callback    = self._on_queue_bound
        )

    def _on_queue_bound(self, frame):
        print('Queue bound.')
        self._start_consuming()

    def _start_consuming(self):
        print('Consuming...')
        self._channel.basic_consume(
            self._callback,
            queue    = self._queue
        )

    def start(self):
        self._connect()
        self._connection.ioloop.start()

    def stop(self):
        self._connection.ioloop.stop()


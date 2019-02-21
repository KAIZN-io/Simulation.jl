import os
import logging
import pika
import json

from values import HN_MESSAGE_BROKER, QUEUE_SCHEDULED_SIMULATIONS, QUEUE_SIMULATION_RESULTS


EXCHANGE_EVENTS = 'events'

logger = logging.getLogger(__name__)

def scheduleSimulation(simulation):
    enqueue(simulation.to_json_str(), QUEUE_SCHEDULED_SIMULATIONS)
    logger.info("Simulation scheduled, id: " + str(simulation.id))

def publishSimulationResult(result):
    enqueue(json.dumps(result), QUEUE_SIMULATION_RESULTS)
    logger.info("Published simulation results for id: " + str(result['simulation_id']))

def enqueue(msg, queue):
    assert isinstance(msg, str)
    assert isinstance(queue, str)

    # open a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
    # get a channel, this can be used for multiplexing the connection, but that is
    # something we don't need rightnow
    channel = connection.channel()

    # create a queue on the server. Theoretically we wouldn't need to do this everytime,
    # but this way we make sure the queue exists
    channel.queue_declare(queue=queue)

    # Send a message to the 'hello' queue
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=msg
    )

    logger.info("Sent message \"" + msg + "\" to queue \"" + queue + "\"")


    # close the connection to make sure the message gets flushed to the server
    connection.close()

def listen(queue):
    print(queue)
    def decorator(callback):
        print(callback)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=HN_MESSAGE_BROKER))
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=queue)

        channel.start_consuming()

    return decorator

def on(event_name):
    print(event_name)
    def decorator(callback):
        print(callback)

        def callback_wrapper(ch, method, properties, body):
            data = json.loads(body)
            logger.info("Event \"" + event_name + "\" received, data: \"" + str(data) + "\"")
            print("Event \"" + event_name + "\" received, data: \"" + str(data) + "\"")
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
        body=data
    )

    logger.info("Emitted event \"" + event_name + "\" with data \"" + data + "\"")
    print("Emitted event \"" + event_name + "\" with data \"" + data + "\"")

    connection.close()


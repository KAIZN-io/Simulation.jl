import os
import logging
import pika
import json


QUEUE_SCHEDULED_SIMULATIONS = os.environ.get('QUEUE_SCHEDULED_SIMULATIONS')
QUEUE_SIMULATION_RESULTS    = os.environ.get('QUEUE_SIMULATION_RESULTS')

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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='task-queue'))
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

def listen(callback, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='task-queue'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue)

    channel.start_consuming()


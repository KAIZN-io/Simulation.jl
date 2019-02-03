import os
import pika
import time
import simplejson as json

import message_queue as mq
from db import sessionScope, Ex, Pd


QUEUE_SIMULATION_RESULTS = os.environ['QUEUE_SIMULATION_RESULTS']

def process_simulation_result(ch, method, properties, body):
    print("Simulation result received")
    print(body)
    # parse the JSON to python dict, so one can work with it
    simulation_results = json.loads(body)
    print("Simulation id: " + str(simulation_results['simulation_id']))

    # store the received simulations results in the database
    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == simulation_results['simulation_id']) \
                .one()

        for pd in simulation_results['pds']:
            ex.pds.append(Pd.from_dict(pd))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

print("Waiting for simulation results...")
mq.listen(process_simulation_result, QUEUE_SIMULATION_RESULTS)


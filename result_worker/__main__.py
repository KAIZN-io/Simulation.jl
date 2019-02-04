import os
import pika
import simplejson as json
from datetime import datetime

import message_queue as mq
from db import sessionScope, Ex, Pd
from values import RFC3339_DATE_FORMAT


QUEUE_SIMULATION_RESULTS = os.environ['QUEUE_SIMULATION_RESULTS']

def process_simulation_result(ch, method, properties, body):
    print("Simulation result received")
    # parse the JSON to python dict, so one can work with it
    simulation_results = json.loads(body)
    print("Simulation id: " + str(simulation_results['simulation_id']))

    # store the received simulations results in the database
    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == simulation_results['simulation_id']) \
                .one()

        ex.started_at = datetime.strptime(simulation_results['started_at'], RFC3339_DATE_FORMAT)
        ex.finished_at = datetime.strptime(simulation_results['finished_at'], RFC3339_DATE_FORMAT)
        ex.extrt = simulation_results['extrt']
        ex.exdose = simulation_results['exdose']
        ex.exstdtc_array = simulation_results['exstdtc_array']

        for pd in simulation_results['pds']:
            ex.pds.append(Pd.from_dict(pd))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

print("Waiting for simulation results...")
mq.listen(process_simulation_result, QUEUE_SIMULATION_RESULTS)


import json
from datetime import datetime
import eventlet

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, QUEUE_SIMULATION_RESULTS
from db import sessionScope, Ex, Pd


@mq.on('simulation.*.scheduled')
def processSimulationResult(ch, method, properties, body):
    event = json.loads(body)
    simulation = event['payload']

    print(str(simulation['id']) + ' - Persisting scheduled...')

    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == simulation['id']) \
                .one()

        # adding data
        ex.scheduled_at = datetime.strptime(event['emitted_at'], RFC3339_DATE_FORMAT)

    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(simulation['id']) + ' - Done persisting scheduled.')

@mq.on('simulation.*.started')
def processSimulationResult(ch, method, properties, body):
    event = json.loads(body)
    simulation = event['payload']

    print(str(simulation['id']) + ' - Persisting started...')

    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == simulation['id']) \
                .one()

        # adding data
        ex.started_at = datetime.strptime(event['emitted_at'], RFC3339_DATE_FORMAT)

    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(simulation['id']) + ' - Done persisting started.')

@mq.on('simulation.*.finished')
def processSimulationResult(ch, method, properties, body):
    event = json.loads(body)
    simulation = event['payload']

    print(str(simulation['id']) + ' - Persisting finished...')

    # store the received simulations results in the database
    with sessionScope() as session:
        # fetching original simulation
        ex = session.query(Ex) \
                .filter(Ex.id == simulation['id']) \
                .one()

        # adding data
        ex.finished_at   = datetime.strptime(event['emitted_at'], RFC3339_DATE_FORMAT)
        ex.extrt         = simulation['extrt']
        ex.exdose        = simulation['exdose']
        ex.exstdtc_array = simulation['exstdtc_array']
        ex.image_path    = simulation['image_path']

        # adding simulation results
        for pd in simulation['pds']:
            ex.pds.append(Pd.from_dict(pd))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(simulation['id']) + ' - Done persisting finished.')

print( 'Worker initialized, waiting for events...' )

while True:
    eventlet.sleep(1)


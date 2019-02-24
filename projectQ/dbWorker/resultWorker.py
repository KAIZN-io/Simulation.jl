import json
from datetime import datetime
import eventlet

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, SERVICE_DB_WORKER
from db import sessionScope, Ex, Pd


@mq.on('simulation.*.scheduled', SERVICE_DB_WORKER)
def processSimulationScheduled(ch, method, properties, body):
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

@mq.on('simulation.*.started', SERVICE_DB_WORKER)
def processSimulationStart(ch, method, properties, body):
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

@mq.on('simulation.*.finished', SERVICE_DB_WORKER)
def processSimulationFinished(ch, method, properties, body):
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

# Do something to prevent the process from ending...
# With the asynchronous listeners from messageQueue, nothing else will keep the process open
while True:
    eventlet.sleep(1)


import json
from datetime import datetime
import eventlet

from eventSystem import on, SimulationScheduled, SimulationStarted, SimulationFinished, SimulationFailed
from values import RFC3339_DATE_FORMAT, SERVICE_DB_WORKER
from db import sessionScope, Ex, Pd


@on(SimulationScheduled, SERVICE_DB_WORKER)
def processSimulationScheduled(ch, method, properties, event, payload):

    print(str(payload['id']) + ' - Persisting scheduled...')

    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == payload['id']) \
                .one()

        # adding data
        ex.scheduled_at = event.get_emitted_at()

    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(payload['id']) + ' - Done persisting scheduled.')

@on(SimulationStarted, SERVICE_DB_WORKER)
def processSimulationStarted(ch, method, properties, event, payload):

    print(str(payload['id']) + ' - Persisting started...')

    with sessionScope() as session:
        ex = session.query(Ex) \
                .filter(Ex.id == payload['id']) \
                .one()

        # adding data
        ex.started_at = event.get_emitted_at()

    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(payload['id']) + ' - Done persisting started.')

@on(SimulationFinished, SERVICE_DB_WORKER)
def processSimulationFinished(ch, method, properties, event, payload):

    print(str(payload['id']) + ' - Persisting finished...')

    # store the received simulation results in the database
    with sessionScope() as session:
        # fetching original simulation
        ex = session.query(Ex) \
                .filter(Ex.id == payload['id']) \
                .one()

        # adding data
        ex.finished_at   = event.get_emitted_at()
        ex.extrt         = payload['extrt']
        ex.exdose        = payload['exdose']
        ex.exstdtc_array = payload['exstdtc_array']
        ex.image_path    = payload['image_path']

        # adding simulation results
        for pd in payload['pds']:
            ex.pds.append(Pd.from_dict(pd))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(payload['id']) + ' - Done persisting finished.')

@on(SimulationFailed, SERVICE_DB_WORKER)
def processSimulationFailed(ch, method, properties, event, payload):

    print(str(payload['id']) + ' - Persisting failed...')

    # store the received simulations results in the database
    with sessionScope() as session:
        # fetching original simulation
        ex = session.query(Ex) \
                .filter(Ex.id == payload['id']) \
                .one()

        # adding data
        ex.failed_at = event.get_emitted_at()

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(payload['id']) + ' - Done persisting failed.')

print( 'Worker initialized, waiting for events...' )

# Do something to prevent the process from ending...
# The event system uses ansychronous listners which wont keep the process running
while True:
    eventlet.sleep(1)


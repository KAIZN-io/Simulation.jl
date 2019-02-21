import json
from datetime import datetime

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, QUEUE_SIMULATION_RESULTS
from db import sessionScope, Ex, Pd


print("Waiting for simulation results...")
@mq.on('simulation.*.finished')
def processSimulationResult(ch, method, properties, body):
    # parse the JSON to python dict, so one can work with it
    simulation_result = json.loads(body)
    print("Simulation results received, id: " + str(simulation_result['id']))

    # store the received simulations results in the database
    print('Writing results to database...')
    with sessionScope() as session:
        # fetching original simulation
        ex = session.query(Ex) \
                .filter(Ex.id == simulation_result['id']) \
                .one()

        # adding data
        ex.started_at    = datetime.strptime(simulation_result['started_at'], RFC3339_DATE_FORMAT)
        ex.finished_at   = datetime.strptime(simulation_result['finished_at'], RFC3339_DATE_FORMAT)
        ex.extrt         = simulation_result['extrt']
        ex.exdose        = simulation_result['exdose']
        ex.exstdtc_array = simulation_result['exstdtc_array']
        ex.image_path    = simulation_result['image_path']

        # adding simulation results
        for pd in simulation_result['pds']:
            ex.pds.append(Pd.from_dict(pd))

        # emit event that the simulations was persisted
        event_name = 'simulation.' + ex.getTypeAsString() + '.results-persisted'
        mq.emit(event_name, {'id': ex.id })

    # confirm that the message was received and processed
    print('Acknowledging that the results were received and processed...')
    ch.basic_ack(delivery_tag = method.delivery_tag)


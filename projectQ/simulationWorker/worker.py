import json
from datetime import datetime

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, QUEUE_SCHEDULED_SIMULATIONS, QUEUE_SIMULATION_RESULTS
from simulationWorker.simulate import simulate


print("Waiting for simulations")
@mq.on('simulation.*.scheduled')
def processSimulation(ch, method, properties, body):
    simulationData = json.loads(body)
    print('Simulation received, id: ' + str(simulationData['id']))

    print('Simulating...')

    # save the started at time
    started_at = datetime.utcnow()

    # emit event that the simulations ist started
    event_name = 'simulation.' + simulationData['type'] + '.started'
    mq.emit(event_name, {
        'id': simulationData['id'],
        'started_at': started_at.strftime(RFC3339_DATE_FORMAT),
    })

    # simulate
    result = simulate(simulationData)

    # note time when the simulation was finished
    finished_at = datetime.utcnow()

    print('Publishing results...')

    # emit event that the simulations ist started
    event_name = 'simulation.' + simulationData['type'] + '.finished'
    mq.emit(event_name, {
        'id': simulationData['id'],
        'started_at': started_at.strftime(RFC3339_DATE_FORMAT),
        'finished_at': finished_at.strftime(RFC3339_DATE_FORMAT),
        'extrt': result['extrt'],
        'exdose': result['exdose'],
        'exstdtc_array': result['exstdtc_array'],
        'image_path': result['image_path'],
        'pds': result['pds']
    })

    # confirm that the message was received and processed
    print('Acknowledging that the simulation was received and processed...')
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print('Done')


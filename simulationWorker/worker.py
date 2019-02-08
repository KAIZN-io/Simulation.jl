import json
from datetime import datetime

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, QUEUE_SCHEDULED_SIMULATIONS, QUEUE_SIMULATION_RESULTS
from simulationWorker.simulate import simulate


def processSimulation(ch, method, properties, body):
    simulationData = json.loads(body)
    print('Simulation received, id: ' + str(simulationData['id']))

    print('Simulating...')
    started_at = datetime.utcnow()
    result = simulate(simulationData)
    finished_at = datetime.utcnow()

    print('Publishing results...')
    mq.publishSimulationResult({
        'simulation_id': simulationData['id'],
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

print("Waiting for simulations")
mq.listen(processSimulation, QUEUE_SCHEDULED_SIMULATIONS)



import eventlet
import json

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, QUEUE_SCHEDULED_SIMULATIONS, QUEUE_SIMULATION_RESULTS
from simulationWorker.simulate import simulate


@mq.on('simulation.*.scheduled')
def processSimulation(ch, method, properties, body):
    event = json.loads(body)
    simulation = event['payload']

    print(str(simulation['id']) + ' - Starting simulation, type: ' + simulation['type'])

    # emit event that the simulations ist started
    event_name = 'simulation.' + simulation['type'] + '.started'
    mq.emit(event_name, {
        'id': simulation['id'],
    })

    # simulate
    result = simulate(simulation)

    print(str(simulation['id']) + ' - Simulation finished.')

    event_name = 'simulation.' + simulation['type'] + '.finished'
    mq.emit(event_name, {
        'id': simulation['id'],
        'extrt': result['extrt'],
        'exdose': result['exdose'],
        'exstdtc_array': result['exstdtc_array'],
        'image_path': result['image_path'],
        'pds': result['pds']
    })

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(simulation['id']) + ' - Done.')

print( 'Worker initialized, waiting for simulation...' )

while True:
    eventlet.sleep(1)


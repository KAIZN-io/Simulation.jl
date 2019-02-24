import eventlet
import json

import messageQueue as mq
from values import RFC3339_DATE_FORMAT, SERVICE_SIMULATION_WORKER
from simulationWorker.simulate import simulate


@mq.on('simulation.*.scheduled', SERVICE_SIMULATION_WORKER)
def processSimulationScheduled(ch, method, properties, body):
    event = json.loads(body)
    simulation = event['payload']

    print(str(simulation['id']) + ' - Starting simulation, type: ' + simulation['type'])

    # emit event that the simulations ist started
    event_name = 'simulation.' + simulation['type'] + '.started'
    mq.emit(event_name, {
        'id': simulation['id'],
    })

    # simulate
    try:
        result = simulate(simulation)
    except Exception:
        print(str(simulation['id']) + ' - Simulation failed!')
        event_name = 'simulation.' + simulation['type'] + '.failed'
        mq.emit(event_name, {
            'id': simulation['id'],
        })
        # discard the message from the queue
        ch.basic_nack(delivery_tag = method.delivery_tag, requeue = False)
        return

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

# Do something to prevent the process from ending...
# With the asynchronous listeners from messageQueue, nothing else will keep the process open
while True:
    eventlet.sleep(1)


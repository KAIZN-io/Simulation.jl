import eventlet
import json

from messageQueue import mq, eventCreators, eventTypes
from values import RFC3339_DATE_FORMAT, SERVICE_SIMULATION_WORKER
from simulationWorker.simulate import simulate


@mq.on(eventTypes.SIMULATION_SCHEDULED, SERVICE_SIMULATION_WORKER)
def processSimulationScheduled(ch, method, properties, event):
    simulation = event['payload']

    print(str(simulation['id']) + ' - Starting simulation, type: ' + simulation['type'])

    # emit event that the simulations ist started
    mq.emit(eventCreators.simulationStarted( simulation['id'] ))

    # simulate
    try:
        result = simulate(simulation)
    except Exception as error:
        print(str(simulation['id']) + ' - Simulation failed!')

        mq.emit(eventCreators.simulationFailed( simulation['id'], str( error ) ))

        # discard the message from the queue
        ch.basic_nack(delivery_tag = method.delivery_tag, requeue = False)
        return

    print(str(simulation['id']) + ' - Simulation finished.')

    mq.emit(eventCreators.simulationFinished( {
        'id': simulation['id'],
        'extrt': result['extrt'],
        'exdose': result['exdose'],
        'exstdtc_array': result['exstdtc_array'],
        'image_path': result['image_path'],
        'pds': result['pds']
    } ))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(simulation['id']) + ' - Done.')

print( 'Worker initialized, waiting for simulation...' )

# Do something to prevent the process from ending...
# With the asynchronous listeners from messageQueue, nothing else will keep the process open
while True:
    eventlet.sleep(1)


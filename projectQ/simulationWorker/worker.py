import eventlet
import json

from eventSystem import on, emit, SimulationScheduled, SimulationStarted, SimulationFinished, SimulationFailed
from values import RFC3339_DATE_FORMAT, SERVICE_SIMULATION_WORKER
from simulationWorker.simulate import simulate


@on(SimulationScheduled, SERVICE_SIMULATION_WORKER)
def processSimulationScheduled(ch, method, properties, event, payload):
    print(str(payload['id']) + ' - Starting simulation, type: ' + payload['type'])

    # emit event that the simulations ist started
    emit(SimulationStarted.create(payload['id']))

    # simulate
    try:
        result = simulate(payload)
    except Exception as error:
        print(str(payload['id']) + ' - Simulation failed!')

        emit(SimulationFailed(payload['id'], str( error )))

        # discard the message from the queue
        ch.basic_nack(delivery_tag = method.delivery_tag, requeue = False)
        return

    print(str(payload['id']) + ' - Simulation finished.')

    emit(SimulationFinished({
        'id': payload['id'],
        'extrt': result['extrt'],
        'exdose': result['exdose'],
        'exstdtc_array': result['exstdtc_array'],
        'image_path': result['image_path'],
        'pds': result['pds']
    }))

    # confirm that the message was received and processed
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(str(payload['id']) + ' - Done.')

print( 'Worker initialized, waiting for simulation...' )

# Do something to prevent the process from ending...
# The event system uses ansychronous listners which wont keep the process running
while True:
    eventlet.sleep(1)


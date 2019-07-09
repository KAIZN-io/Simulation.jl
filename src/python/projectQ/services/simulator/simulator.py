import eventlet
import traceback

from projectQ.packages.eventSystem import on, emit, SimulationScheduled, SimulationStarted, SimulationFinished, SimulationFailed
from projectQ.packages.values import RFC3339_DATE_FORMAT, SERVICE_SIMULATOR
from projectQ.packages.simulation import simulate


def run():
    @on(SimulationScheduled, SERVICE_SIMULATOR)
    def processSimulationScheduled(ch, method, properties, event, payload):
        print(str(payload['id']) + ' - Starting simulation, type: ' + payload['type'])

        # emit event that the simulations ist started
        emit(SimulationStarted.create(payload['id']))

        # simulate
        try:
            result = simulate(payload)
        except Exception as error:
            error_str = str(error)
            traceback_str = traceback.format_exc()

            print(str(payload['id']) + ' - Simulation failed! Error: ' + error_str)
            print(traceback_str)

            emit(SimulationFailed.create(payload['id'], error_str, traceback_str))

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


import datetime
from schema import Schema, Use

from db import Ex
from values import RFC3339_DATE_FORMAT
import messageQueue.eventTypes as types


def getBaseEvent():
    return {
        'emitted_at': datetime.datetime.utcnow().strftime(RFC3339_DATE_FORMAT),
    }

def simulationScheduled(simulation):
    assert isinstance(simulation, Ex)

    return {
        'type': types.SIMULATION_SCHEDULED,
        'payload': simulation.to_dict(json_ready=True),
        **getBaseEvent()
    }

def simulationStarted(simulation_id):
    assert isinstance(simulation_id, int)

    return {
        'type': types.SIMULATION_STARTED,
        'payload': {
            'id': simulation_id
        },
        **getBaseEvent()
    }

def simulationFinished(simulation_data):
    assert Schema({
        'id': Use(int),
        'extrt': Use(str),
        'exdose': Use(str),
        'exstdtc_array': [Use(str)],
        'image_path': Use(str),
        'pds': [Use(dict)]
    }).validate(simulation_data)

    return {
        'type': types.SIMULATION_FINISHED,
        'payload': simulation_data,
        **getBaseEvent()
    }

def simulationFailed(simulation_id, error_message):
    assert isinstance(simulation_id, int)
    assert isinstance(error_message, str)

    return {
        'type': types.SIMULATION_FAILED,
        'payload': {
            'id': simulation_id,
            'error_message': error_message
        },
        **getBaseEvent()
    }


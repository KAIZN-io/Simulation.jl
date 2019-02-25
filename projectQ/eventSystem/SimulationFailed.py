from schema import Schema, Use, Optional

from eventSystem.Event import Event


class SimulationFailed(Event):
    routing_key = 'simulation.failed'

    payload_schema = Schema({
        'id': Use(int),
        'error': Schema({
            'message': Use(str),
            Optional('traceback'): Use(str)
        })
    })

    @classmethod
    def create(cls, simulation_id, error, traceback=None):
        event_dict = {
            'id': simulation_id,
            'error': {
                'message': error,
            }
        }

        if traceback:
            event_dict['error']['traceback'] = traceback

        return cls(event_dict)


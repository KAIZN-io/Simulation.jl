from schema import Schema, Use

from eventSystem.Event import Event


class SimulationStarted(Event):
    routing_key = 'simulation.started'

    payload_schema = Schema({
        'id': Use(int)
    })

    @classmethod
    def create(cls, simulation_id):
        return cls({
            'id': simulation_id
        })


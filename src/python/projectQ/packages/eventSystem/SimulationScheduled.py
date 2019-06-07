from projectQ.packages.eventSystem.Event import Event
from projectQ.packages.db import Ex

class SimulationScheduled(Event):
    routing_key = 'simulation.scheduled'

    payload_schema = Ex.get_dict_schema()

    @classmethod
    def create(cls, simulation):
        assert isinstance(simulation, Ex)

        return cls(simulation.to_dict(json_ready=True))

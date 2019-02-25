from schema import Schema, Use

from messageQueue.events import Event


class SimulationFinished(Event):
    routing_key = 'simulation.finished'

    payload_schema = Schema({
        'id': Use(int),
        'extrt': Use(str),
        'exdose': Use(int),
        'exstdtc_array': [Use(int)],
        'image_path': Use(str),
        'pds': [Use(dict)]
    })


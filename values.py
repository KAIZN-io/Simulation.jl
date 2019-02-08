import os
from enum import Enum


QUEUE_SCHEDULED_SIMULATIONS = os.environ.get('QUEUE_SCHEDULED_SIMULATIONS')
QUEUE_SIMULATION_RESULTS    = os.environ.get('QUEUE_SIMULATION_RESULTS')

RFC3339_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# all supported models as an enum, so that our database can work with that
class SimulationTypes(Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'


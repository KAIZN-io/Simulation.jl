from enum import Enum

RFC3339_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# all supported models as an enum, so that our database can work with that
class SimulationTypes(Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'


from enum import Enum


# all supported models as an enum, so that our database can work with that
class SimulationModel(Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'


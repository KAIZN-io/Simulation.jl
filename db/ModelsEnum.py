from enum import Enum


# all supported models as an enum, so that our database can work with that
# TODO: find are clearer name for this. Maybe `SimulationModels`
class Models(Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'

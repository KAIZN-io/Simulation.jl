import os
from enum import Enum


# host names, as defined in the `docker-compose.yml`
HN_MESSAGE_BROKER = 'messageBroker'
HN_DB = 'db'

# Get the DEBUG value and convert it to a boolean value
DEBUG = os.environ.get('DEBUG') == '1'

# Get database related values
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# get exchages
EXCHANGE_EVENTS = os.environ.get('EXCHANGE_EVENTS')

# get the service names
SERVICE_SIMULATION_WORKER = os.environ.get('SERVICE_SIMULATION_WORKER')
SERVICE_DB_WORKER = os.environ.get('SERVICE_DB_WORKER')

# set the root dir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# the default date format used for encoding and decoding messages
RFC3339_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# all supported models as an enum, so that our database can work with that
class SimulationTypes(Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'


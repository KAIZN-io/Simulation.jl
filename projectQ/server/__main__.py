import os
import threading
import time
import datetime
import logging
import json
from flask_socketio import SocketIO
from flask_restful import Api

from server.app import app
from server.routings import routes
from server.api import Simulation, SimulationList
from values import DEBUG, RFC3339_DATE_FORMAT
from db.base import base, ThreadScopedSession
import messageQueue as mq


logger = logging.getLogger(__name__)

# this check prevents double initialization in debug mode with code relaoding enabled
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    """Initialize Database"""
    logger.info("Creating database schemas")
    # Create tables if they do not yet exist.
    session = ThreadScopedSession()
    base.metadata.create_all(session.getEngine())

    """Create folders"""
    if not os.path.isdir('SimulationPictures'):
        logger.info("Created folder `SimulationPictures`")
        os.mkdir('SimulationPictures')
else:
    logger.debug("Not main thread, skipping initialization")

# add routes to the flask app
logger.info("Registering routes")
app.register_blueprint(routes)

# register api resources
api = Api(app)
api.add_resource(Simulation, '/api/simulation/<int:id>')
api.add_resource(SimulationList, '/api/simulation/list')

# reset the PYTHONPATH. This is a workaround to make importing modules work again when using the reloader
os.environ['PYTHONPATH'] = os.getcwd()

# actually start the server
socket = SocketIO(app, logger=logger)

@mq.on('simulation.*.scheduled')
def notify_clients(ch, method, properties, body):
    socket.emit( "simulation.scheduled", json.loads(body))

@mq.on('simulation.*.started')
def notify_clients(ch, method, properties, body):
    socket.emit( "simulation.started", json.loads(body))

@mq.on('simulation.*.finished')
def notify_clients(ch, method, properties, body):
    socket.emit( "simulation.finished", json.loads(body))

socket.run(app, host='0.0.0.0', debug=DEBUG)

logger.info("Server initialized")


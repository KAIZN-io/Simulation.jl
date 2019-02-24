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
from messageQueue import mq, eventTypes


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

# create the SocketIO socket for live communication with the web app
socket = SocketIO(app, logger=logger)

# Map serverside events to the socket so that the web app will receive them as well
@mq.on(eventTypes.SIMULATION_SCHEDULED)
def notify_clients(ch, method, properties, event):
    socket.emit( eventTypes.SIMULATION_SCHEDULED, event)
    ch.basic_ack(delivery_tag = method.delivery_tag)

@mq.on(eventTypes.SIMULATION_STARTED)
def notify_clients(ch, method, properties, event):
    socket.emit( eventTypes.SIMULATION_STARTED, event)
    ch.basic_ack(delivery_tag = method.delivery_tag)

@mq.on(eventTypes.SIMULATION_FINISHED)
def notify_clients(ch, method, properties, event):
    socket.emit( eventTypes.SIMULATION_FINISHED, event)
    ch.basic_ack(delivery_tag = method.delivery_tag)

@mq.on(eventTypes.SIMULATION_FAILED)
def notify_clients(ch, method, properties, event):
    socket.emit( eventTypes.SIMULATION_FAILED, event)
    ch.basic_ack(delivery_tag = method.delivery_tag)

# actually start the server
socket.run(app, host='0.0.0.0', debug=DEBUG)

logger.info("Server initialized")


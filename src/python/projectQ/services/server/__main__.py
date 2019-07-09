import os
import threading
import time
import datetime
import logging
import json
from flask_socketio import SocketIO
from flask_restful import Api

# I need to be imported here, because otherwise the logging does not work
from projectQ.services.server.app import app

from projectQ.packages.values import DEBUG, RFC3339_DATE_FORMAT, RESULT_IMAGE_DIR, STATIC_DIR
from projectQ.packages.db.base import base, ThreadScopedSession
from projectQ.packages.eventSystem import on, SimulationScheduled, SimulationStarted, SimulationFinished, SimulationFailed

from projectQ.services.server.routings import routes
from projectQ.services.server.api import Simulation, SimulationList


logger = logging.getLogger(__name__)

# this check prevents double initialization in debug mode with code relaoding enabled
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    """Initialize Database"""
    logger.info("Creating database schemas")
    # Create tables if they do not yet exist.
    session = ThreadScopedSession()
    base.metadata.create_all(session.getEngine())

    """Create folders"""
    if not os.path.isdir(STATIC_DIR):
        os.mkdir(STATIC_DIR)
        logger.info('Created folder ' + STATIC_DIR)
    if not os.path.isdir(RESULT_IMAGE_DIR):
        os.mkdir(RESULT_IMAGE_DIR)
        logger.info('Created folder ' + RESULT_IMAGE_DIR)
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
@on(SimulationScheduled)
def notify_clients(ch, method, properties, event, payload):
    socket.emit(event.get_routing_key(), event.to_dict(json_ready=True))
    ch.basic_ack(delivery_tag = method.delivery_tag)

@on(SimulationStarted)
def notify_clients(ch, method, properties, event, payload):
    socket.emit(event.get_routing_key(), event.to_dict(json_ready=True))
    ch.basic_ack(delivery_tag = method.delivery_tag)

@on(SimulationFinished)
def notify_clients(ch, method, properties, event, payload):
    socket.emit(event.get_routing_key(), event.to_dict(json_ready=True))
    ch.basic_ack(delivery_tag = method.delivery_tag)

@on(SimulationFailed)
def notify_clients(ch, method, properties, event, payload):
    socket.emit(event.get_routing_key(), event.to_dict(json_ready=True))
    ch.basic_ack(delivery_tag = method.delivery_tag)

# actually start the server
socket.run(app, host='0.0.0.0', debug=DEBUG)

logger.info("Server initialized")


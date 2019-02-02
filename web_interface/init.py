import os
import logging

from app import app
from db.base import base, ThreadScopedSession
from initializeModel import initializeDb
from routings import routes


logger = logging.getLogger(__name__)

# this check prevents double initialization in debug mode with code relaoding enabled
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    """Initialize Database"""
    logger.info("Creating database schemas")
    # Create tables if they do not yet exist.
    session = ThreadScopedSession()
    base.metadata.create_all(session.getEngine())

    # fill in initial values into the database
    initializeDb()

    """Create folders"""
    if not os.path.isdir('SimulationPictures'):
        logger.info("Created folder `SimulationPictures`")
        os.mkdir('SimulationPictures')

    # add routes to the flask app
    logger.info("Registering routes")
    app.register_blueprint(routes)

    logger.info("App initialized")
else:
    logger.debug("Not main thread, skipping initialization")

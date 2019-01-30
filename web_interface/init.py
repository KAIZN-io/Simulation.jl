import os

from app import app
from db.base import base, ThreadScopedSession
from initializeModel import initializeDb
from routings import routes


"""Initialize Database"""
# Create tables if they do not yet exist.
session = ThreadScopedSession()
base.metadata.create_all(session.getEngine())

# fill in initial values into the database
initializeDb()

"""Create folders"""
if not os.path.isdir('SimulationPictures'):
    os.mkdir('SimulationPictures')

# add routes to the flask app
app.register_blueprint(routes)


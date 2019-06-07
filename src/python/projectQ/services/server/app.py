import os
from flask import Flask
from logging.config import dictConfig

from projectQ.packages.values import DEBUG, STATIC_DIR


"""Configure logging"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(process)d - %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG' if DEBUG else 'INFO',
        'handlers': ['wsgi']
    }
})

"""initialize flask app"""
# setup flask
app = Flask(
    'ProjectQ',
    template_folder=os.path.dirname(os.path.abspath(__file__)) + '/templates',
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

# initialize logger
app.logger

app.logger.debug("Logger initialized")


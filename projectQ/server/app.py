from flask import Flask
from logging.config import dictConfig

from values import DEBUG


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
    template_folder='server/templates',
    static_folder='server/static',
    static_url_path='/static'
)

# initialize logger
app.logger

app.logger.debug("Logger initialized")


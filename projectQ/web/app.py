from flask import Flask
from logging.config import dictConfig

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
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

"""initialize flask app"""
# setup flask
app = Flask(
    'ProjectQ',
    template_folder='web/templates',
    static_url_path='/pictures',
    static_folder='SimulationPictures'
)

# initialize logger
app.logger

app.logger.info("Logger initialized")


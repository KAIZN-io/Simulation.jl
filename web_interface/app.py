from flask import Flask


"""initialize flask app"""
# setup flask
app = Flask(
    'ProjectQ',
    template_folder='web_interface/templates',
    static_url_path='/pictures',
    static_folder='SimulationPictures'
)


import logging
from pprint import pformat
from flask_restful import Resource
from sqlalchemy import desc

from db import sessionScope, Ex


logger = logging.getLogger(__name__)

class Simulation(Resource):
    @classmethod
    def get(cls, id):
        with sessionScope() as session:
            ex = session.query(Ex) \
                    .filter(Ex.id == id) \
                    .one() \
                    .to_dict(True)
            logger.info(pformat(ex))

            return ex

class SimulationList(Resource):
    @classmethod
    def get(cls):
        with sessionScope() as session:
            simulations = session.query(Ex) \
                    .order_by(desc(Ex.created_at)) \
                    .all()

            return [simulation.to_brief_dict(True) for simulation in simulations]

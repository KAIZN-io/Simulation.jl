from flask_restful import Resource
from sqlalchemy import desc

from db import sessionScope, Ex


class Simulation(Resource):
    @classmethod
    def get(cls, id):
        with sessionScope() as session:
            return session.query(Ex) \
                    .filter(Ex.id == id) \
                    .one() \
                    .to_dict(True)

class SimulationList(Resource):
    @classmethod
    def get(cls):
        with sessionScope() as session:
            simulations = session.query(Ex) \
                    .order_by(desc(Ex.created_at)) \
                    .all()

            return [simulation.to_brief_dict(True) for simulation in simulations]

from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, REAL, DOUBLE_PRECISION
import datetime

from db.base import base
from values import SimulationTypes


# Ex stands for 'Exposure' of an organism with a substance
class Ex(base):
    __tablename__ = 'ex'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    name = Column(String)
    image_path = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    # every ex has exactly one model
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship('Model', back_populates='exs')

    # every ex has exactly one set of initial_values
    initial_values_id = Column(Integer, ForeignKey('initial_values.id'))
    initial_values = relationship('InitialValues', back_populates='exs')

    # every ex has exactly one set of parameters
    parameters_id = Column(Integer, ForeignKey('parameters.id'))
    parameters = relationship('Parameters', back_populates='exs')

    # every ex has multiple results in the pd table
    pd = relationship('Pd', back_populates='exs')

    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String)
    excat = Column(String)
    # TODO: Why is this unique?
    extrt = Column(String, unique=True, nullable=False)
    exdose = Column(REAL)
    exdosu = Column(String)
    exstdtc_array = Column(ARRAY(DOUBLE_PRECISION))
    simulation_start = Column(DOUBLE_PRECISION)
    simulation_stop = Column(DOUBLE_PRECISION)
    co = Column(String)


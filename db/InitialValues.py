from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
import datetime

from db.base import base
from values import SimulationTypes


class InitialValues(base):
    __tablename__ = 'initial_values'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this initial value was used
    exs = relationship('Ex', back_populates='initial_values')

    type = Column(Enum(SimulationTypes))
    testcd = Column(String, unique=True)
    test = Column(String)
    orres = Column(DOUBLE_PRECISION)
    orresu = Column(String)
    co = Column(String)


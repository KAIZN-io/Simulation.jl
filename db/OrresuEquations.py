from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
import datetime

from db.base import base
from values import SimulationTypes

class OrresuEquations(base):
    __tablename__ = 'orresu_equations'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(Enum(SimulationTypes))
    testcd = Column(String, nullable=False, unique=True)
    test = Column(String)
    orresu = Column(String)


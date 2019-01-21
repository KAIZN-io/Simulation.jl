from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
import datetime

from db.base import base
from values import SimulationModel

#TODO: more meaningful name
class Pd(base):
    __tablename__ = 'pd'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(SimulationModel))
    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String, unique=True)
    pdseq = Column(Integer, unique=True, nullable=False)
    pdtestcd = Column(String, unique=True, nullable=False)
    pdtest = Column(String)
    pdorres = Column(DOUBLE_PRECISION)
    pdorresu = Column(String)
    pddtc = Column(DOUBLE_PRECISION, unique=True)
    co = Column(String)


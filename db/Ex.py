from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, REAL, DOUBLE_PRECISION
import datetime

from db.base import base
from values import SimulationModel


#TODO: again this name is rather non self explanatory, is that a table of my ex girlfriends?
class Ex(base):
    __tablename__ = 'ex'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(SimulationModel))
    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String)
    exseq = Column(Integer, unique=True, nullable=False)
    excat = Column(String)
    extrt = Column(String, unique=True, nullable=False)
    exdose = Column(REAL)
    exdosu = Column(String)
    exstdtc_array = Column(ARRAY(DOUBLE_PRECISION))
    simulation_start = Column(DOUBLE_PRECISION)
    simulation_stop = Column(DOUBLE_PRECISION)
    co = Column(String)
    model_version = Column(Integer)
    initvalues_version = Column(Integer)
    parameter_version = Column(String)
    namepicture = Column(String)


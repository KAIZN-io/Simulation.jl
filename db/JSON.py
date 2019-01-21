from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
import datetime

from db.base import base
from values import SimulationModel


#TODO: find a more meaningful name for this table, what does this json do?
class JSON(base):
    __tablename__ = 'json'

    seq = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(SimulationModel))
    model_version = Column(JSON)
    adding_changes = Column(JSON)
    deleting_changes = Column(JSON)


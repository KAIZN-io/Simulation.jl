from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
import datetime

from db.base import base
from values import SimulationModel


class Model(base):
    __tablename__ = 'model'

    seq = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(SimulationModel))
    model_version = Column(JSON)
    adding_changes = Column(JSON)
    deleting_changes = Column(JSON)


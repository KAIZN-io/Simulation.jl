from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
import datetime

from db.base import base
from values import SimulationTypes


class Model(base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    name = Column(String)
    description = Column(String)
    type = Column(Enum(SimulationTypes))
    display_version = Column(String)

    json = Column(JSON)
    json_added = Column(JSON)
    json_deleted = Column(JSON)


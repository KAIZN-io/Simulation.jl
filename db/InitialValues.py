from sqlalchemy import Column, String, DateTime, Integer, Enum, UniqueConstraint
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

    type = Column(Enum(SimulationTypes))
    version = Column(Integer)
    testcd = Column(String, nullable=False)
    test = Column(String)
    orres = Column(DOUBLE_PRECISION)
    orresu = Column(String)
    co = Column(String)

    __table_args__ = (
        UniqueConstraint('type', 'version', 'testcd', name='InitialValues_testcd_unique_per_type_and_version'),
    )


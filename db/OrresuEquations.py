from sqlalchemy import Column, String, DateTime, Integer, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import datetime

from db.base import base
from values import SimulationTypes

class OrresuEquations(base):
    __tablename__ = 'orresu_equations'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    type = Column(Enum(SimulationTypes))
    version = Column(Integer)
    testcd = Column(String, nullable=False)
    test = Column(String)
    orresu = Column(String)

    __table_args__ = (
        UniqueConstraint('type', 'version', 'testcd', name='OrresuEquiations_testcd_unique_per_type_and_version'),
    )


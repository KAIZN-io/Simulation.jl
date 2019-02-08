from sqlalchemy import Column, String, DateTime, Integer, Float, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime

from db.base import base
from values import SimulationTypes

# Pd = PharmacoDynamics
class Pd(base):
    __tablename__ = 'pd'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    ex_id = Column(Integer, ForeignKey('ex.id'))
    ex = relationship('Ex', back_populates='pds')

    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String)
    # Substance
    pdtestcd = Column(String, nullable=False)
    pdtest = Column(String)
    # value
    pdorres = Column(Float)
    pdorresu = Column(String)
    # time in simulation
    pddtc = Column(Float)
    co = Column(String)

    __table_args__ = (
        UniqueConstraint('ex_id', 'pdtestcd', 'pddtc',  name='Pd_uc'),
    )

    @classmethod
    def from_dict(cls, pd_dict):
        return Pd(
            studyid  = pd_dict.get('studyid'),
            domain   = pd_dict.get('domain'),
            usubjid  = pd_dict.get('usubjid'),
            pdtestcd = pd_dict['pdtestcd'],
            pdtest   = pd_dict.get('pdtest'),
            pdorres  = pd_dict.get('pdorres'),
            pdorresu = pd_dict.get('pdorresu'),
            pddtc    = pd_dict.get('pddtc'),
            co       = pd_dict.get('co'),
        )


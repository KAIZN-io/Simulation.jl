from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
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
    pdtestcd = Column(String, nullable=False)
    pdtest = Column(String)
    pdorres = Column(DOUBLE_PRECISION)
    pdorresu = Column(String)
    pddtc = Column(DOUBLE_PRECISION)
    co = Column(String)

    __table_args__ = (
        UniqueConstraint('ex_id', 'usubjid', 'pdtestcd', 'pddtc',  name='Pd_uc'),
    )

    @classmethod
    def from_dict(pd_dict):
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


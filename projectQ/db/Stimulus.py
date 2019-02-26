from sqlalchemy import Column, String, DateTime, Integer, Float, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from schema import Schema, Use
import datetime

from db.base import base


class Stimulus(base):
    __tablename__ = 'stimulus'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this model was used
    ex_id = Column(Integer, ForeignKey('ex.id'))
    ex = relationship('Ex', back_populates='stimuli')

    substance = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    targets = Column(ARRAY(String))
    timings = Column(ARRAY(Integer))
    active = Column(Boolean)

    __table_args__ = (
        UniqueConstraint('ex_id', 'substance', 'amount', 'unit', 'targets', 'timings', name='Stimulus_uniqe_per_simulation'),
    )

    @classmethod
    def get_dict_schema(cls):
        return Schema({
            'substance': Use(str),
            'amount': Use(float),
            'unit': Use(str),
            'targets': [Use(str)],
            'timings': [Use(int)],
            'active': Use(bool)
        })

    def to_dict(self):
        return {
            'substance': self.substance,
            'amount': self.amount,
            'unit': self.unit,
            'targets': self.targets,
            'timings': self.timings,
            'active': self.active
        }


from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, ARRAY
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
    amount = Column(DOUBLE_PRECISION, nullable=False)
    unit = Column(String, nullable=False)
    targets = Column(ARRAY(String))
    timings = Column(ARRAY(Integer))
    active = Column(Boolean)

    __table_args__ = (
        UniqueConstraint('ex_id', 'substance', 'amount', 'unit', 'targets', 'timings', name='Stimulus_uniqe_per_simulation'),
    )

    def to_dict(self):
        return {
            'substance': self.substance,
            'amount': float(self.amount),
            'unit': self.unit,
            'targets': self.targets,
            'timings': self.timings,
            'active': self.active
        }


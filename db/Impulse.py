from sqlalchemy import Column, String, DateTime, Integer, Float, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime

from db.base import base


class Impulse(base):
    __tablename__ = 'impulse'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this model was used
    ex_id = Column(Integer, ForeignKey('ex.id'))
    ex = relationship('Ex', back_populates='impulses')

    substance = Column(String, nullable=False)
    start = Column(Float, nullable=False)
    stop = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('ex_id', 'substance', 'start', 'stop', name='Impulse_uniqe_per_simulation'),
    )

    def to_dict(self):
        return {
            'substance': self.substance,
            'start': self.start,
            'stop': self.stop
        }


import datetime
import logging
from sqlalchemy import Column, String, DateTime, Integer, Float, Enum, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from values import SimulationTypes
from db.base import base
from db.initialData import initialDataList


logger = logging.getLogger(__name__)

class ParameterSet(base):
    __tablename__ = 'parameter_set'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this model was used
    exs = relationship('Ex', back_populates='parameter_set')

    # the previous version of this set
    parent_id = Column(Integer, ForeignKey('parameter_set.id'))
    # references to all descending versions of this set
    children = relationship('ParameterSet')

    # reference to all values in this set
    values = relationship('Parameter', back_populates='set')

    name = Column(String)
    description = Column(String)
    type = Column(Enum(SimulationTypes), nullable=False)
    display_version = Column(String)
    version = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('type', 'version', name='ParameterSet_version_unique_per_type'),
    )

    @classmethod
    def initialize(cls, session):
        for modelData in initialDataList:
            logger.info('Initializing ' + modelData.getType().name + ' parameters...')

            parameterSet = ParameterSet(
                type = modelData.getType(),
                version = 1,
            )

            for parameter in modelData.getParameters():
                parameterSet.values.append(
                    Parameter(
                        testcd = parameter.testcd,
                        orres  = parameter.orres,
                        orresu = parameter.orresu,
                        co     = parameter.comment
                    )
                )

            session.add(parameterSet)

class Parameter(base):
    __tablename__ = 'parameter'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # the id of the set this value belonges to
    set_id = Column(Integer, ForeignKey('parameter_set.id'), nullable=False)
    set = relationship('ParameterSet', back_populates='values')

    # name
    testcd = Column(String, nullable=False)
    #value
    orres = Column(Float)
    # unit
    orresu = Column(String)
    test = Column(String)
    co = Column(String)

    __table_args__ = (
        UniqueConstraint('set_id', 'testcd', name='Parameter_testcd_unique_per_set'),
    )

    def to_dict(self):
        return {
            'testcd': self.testcd,
            'orres': self.orres,
            'orresu': self.orresu
        }


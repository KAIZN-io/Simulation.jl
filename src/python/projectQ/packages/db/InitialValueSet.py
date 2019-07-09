import datetime
import logging
from sqlalchemy import Column, String, DateTime, Integer, Float, Enum, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from schema import Schema, Use

from projectQ.packages.values import SimulationTypes
from projectQ.packages.db.base import base
from projectQ.packages.db.initialData import initialDataList


logger = logging.getLogger(__name__)

class InitialValueSet(base):
    __tablename__ = 'initial_value_set'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this model was used
    exs = relationship('Ex', back_populates='initial_value_set')

    # the previous version of this set
    parent_id = Column(Integer, ForeignKey('initial_value_set.id'))
    # references to all descending versions of this set
    children = relationship('InitialValueSet')

    # reference to all values in this set
    values = relationship('InitialValue', back_populates='set', order_by="asc(InitialValue.precedence)")

    name = Column(String)
    description = Column(String)
    type = Column(Enum(SimulationTypes), nullable=False)
    display_version = Column(String)
    version = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('type', 'version', name='InitialValueSet_version_unique_per_type'),
    )

    @classmethod
    def initialize(cls, session):
        for modelData in initialDataList:
            logger.info('Initializing ' + modelData.getType().name + ' values...')

            initialValueSet = InitialValueSet(
                type = modelData.getType(),
                version = 1,
            )

            for value in modelData.getInitialValues():
                initialValueSet.values.append(
                    InitialValue(
                        testcd     = value.testcd,
                        orres      = value.orres,
                        orresu     = value.orresu,
                        precedence = value.precedence,
                        comment    = value.comment
                    )
                )

            session.add(initialValueSet)

class InitialValue(base):
    __tablename__ = 'initial_value'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # the id of the set this value belonges to
    set_id = Column(Integer, ForeignKey('initial_value_set.id'), nullable=False)
    set = relationship('InitialValueSet', back_populates='values')

    # name of the variable
    testcd = Column(String, nullable=False)
    # value or equation describing the variable
    orres = Column(String)
    # unit of the value
    orresu = Column(String)

    # inidcation whether this var should be processed earlier or later
    # generally, fixed values need to be processed before equations
    precedence = Column(Integer)

    # comment
    comment = Column(String)

    __table_args__ = (
        UniqueConstraint('set_id', 'testcd', name='InitialValue_testcd_unique_per_set'),
    )

    @classmethod
    def get_dict_schema(cls):
        return Schema({
            'testcd': Use(str),
            'orres': Use(str),
            'orresu': Use(str),
            'precedence': Use(int),
            'comment': Use(str),
        })

    def to_dict(self):
        return {
            'testcd': self.testcd,
            'orres': self.orres,
            'orresu': self.orresu,
            'precedence': self.precedence,
            'comment': self.comment
        }



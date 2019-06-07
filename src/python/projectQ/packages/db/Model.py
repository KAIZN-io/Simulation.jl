import json
import datetime
import logging
from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON

from projectQ.packages.db.base import base
from projectQ.packages.values import SimulationTypes, ROOT_DIR


logger = logging.getLogger(__name__)

class Model(base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    # uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # references to all exposures where this model was used
    exs = relationship('Ex', back_populates='model')

    # the previous version of this model
    parent_model_id = Column(Integer, ForeignKey('model.id'))
    child_models = relationship('Model')

    name = Column(String)
    description = Column(String)
    type = Column(Enum(SimulationTypes))
    display_version = Column(String)
    version = Column(Integer, nullable=False)

    json = Column(JSON)
    json_added = Column(JSON)
    json_deleted = Column(JSON)

    __table_args__ = (
        UniqueConstraint('type', 'version',  name='Model_version_unique_per_type'),
    )

    @classmethod
    def initialize(cls, session):
        for type in SimulationTypes:
            logger.info('Initializing ' + type.value + '...')

            session.add(Model(
                type = type,
                name = 'initial ' + type.name + 'model',
                description = 'The initial ' + type.name + ' model, hardcoded into the code base.',
                version = 1,
                display_version = '1.0.0',
                json = cls._getInitialModelJson(type)
            ))

    @classmethod
    def _getInitialModelJson(cls, type):
        assert isinstance(type, SimulationTypes)

        path = ROOT_DIR + '/db/initialData/json/' + type.name + '.json'

        try:
            fileHandle = open(path)
            modelJson = json.load(fileHandle)
        except IOError as e:
            logger.error('Could not load module json file: ' + str(e))
        except ValueError as e:
            logger.error('Could not decode JSON: ' + str(e))

        return modelJson


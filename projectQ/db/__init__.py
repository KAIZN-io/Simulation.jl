import logging
from sqlalchemy import event

import db.initialData
from db.base import base, ThreadScopedSession, sessionScope
from db.Ex import Ex
from db.Pd import Pd
from db.Model import Model
from db.InitialValueSet import InitialValueSet, InitialValue
from db.ParameterSet import ParameterSet, Parameter
from db.Impulse import Impulse
from db.Stimulus import Stimulus
from db.OrresuEquations import OrresuEquations


logger = logging.getLogger(__name__)

def initializeDatabase(target, connection, **kw):
    if kw['tables']:
        logger.info('Inserting initial data...')
        with sessionScope() as session:
            Model.initialize(session)
            InitialValueSet.initialize(session)
            ParameterSet.initialize(session)

event.listen(base.metadata, 'after_create', initializeDatabase)


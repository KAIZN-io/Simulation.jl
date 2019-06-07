import logging
from sqlalchemy import event

import projectQ.packages.db.initialData
from projectQ.packages.db.base import base, ThreadScopedSession, sessionScope
from projectQ.packages.db.Ex import Ex
from projectQ.packages.db.Pd import Pd
from projectQ.packages.db.Model import Model
from projectQ.packages.db.InitialValueSet import InitialValueSet, InitialValue
from projectQ.packages.db.ParameterSet import ParameterSet, Parameter
from projectQ.packages.db.Impulse import Impulse
from projectQ.packages.db.Stimulus import Stimulus
from projectQ.packages.db.OrresuEquations import OrresuEquations


logger = logging.getLogger(__name__)

def initializeDatabase(target, connection, **kw):
    if kw['tables']:
        logger.info('Inserting initial data...')
        with sessionScope() as session:
            Model.initialize(session)
            InitialValueSet.initialize(session)
            ParameterSet.initialize(session)

event.listen(base.metadata, 'after_create', initializeDatabase)


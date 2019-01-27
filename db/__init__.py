from db.base import base, ThreadScopedSession, sessionScope
from db.Ex import Ex
from db.Pd import Pd
from db.Model import Model
from db.InitialValueSet import InitialValueSet, InitialValue
from db.ParameterSet import ParameterSet, Parameter
from db.OrresuEquations import OrresuEquations


# Create tables if they do not yet exist.
session = ThreadScopedSession()
base.metadata.create_all(session.getEngine())


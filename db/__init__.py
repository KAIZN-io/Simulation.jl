from db.base import db, base
from db.Ex import Ex
from db.Pd import Pd
from db.Model import Model
from db.InitialValue import InitialValue
from db.Parameter import Parameter
from db.OrresuEquation import OrresuEquation


# Create tables if they do not yet exist.
base.metadata.create_all(db)


from sqlalchemy import create_engine
from sqlalchemy import Column, String, JSON, DateTime, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID, ARRAY, REAL, DOUBLE_PRECISION
import enum
import datetime


db = create_engine('postgresql://postgres@db_postgres/simulation_results')
base = declarative_base()

# all supported models as an enum, so that our database can work with that
class Models(enum.Enum):
    combined = 'combined_models'
    hog = 'hog'
    ion = 'ion'
    volume = 'volume'

#TODO: find a more meaningful name for this table, what does this json do?
class JSON(base):
    __tablename__ = 'json'

    seq = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    model_version = Column(JSON)
    adding_changes = Column(JSON)
    deleting_changes = Column(JSON)

#TODO: again this name is rather non self explanatory, is that a table of my ex girlfriends?
class Ex(base):
    __tablename__ = 'ex'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String)
    exseq = Column(Integer, unique=True, nullable=False)
    excat = Column(String)
    extrt = Column(String, unique=True, nullable=False)
    exdose = Column(REAL)
    exdosu =Column(String)
    exstdtc_array = Column(ARRAY(DOUBLE_PRECISION))
    simulation_start = Column(DOUBLE_PRECISION)
    simulation_stop = Column(DOUBLE_PRECISION)
    co = Column(String)
    model_version = Column(Integer)
    initvalues_version = Column(Integer)
    parameter_version = Column(String)
    namepicture = Column(String)

#TODO: more meaningful name
class Pd(base):
    __tablename__ = 'pd'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    studyid = Column(String)
    domain = Column(String)
    usubjid = Column(String, unique=True)
    pdseq = Column(Integer, unique=True, nullable=False)
    pdtestcd = Column(String, unique=True, nullable=False)
    pdtest = Column(String)
    pdorres = Column(DOUBLE_PRECISION)
    pdorresu = Column(String)
    pddtc = Column(DOUBLE_PRECISION, unique=True)
    co = Column(String)

class InitialValue(base):
    __tablename__ = 'initial_values'

    seq = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    testcd = Column(String, unique=True)
    test = Column(String)
    orres = Column(DOUBLE_PRECISION)
    orresu = Column(String)
    co = Column(String)

class Parameter(base):
    __tablename__ = 'parameters'

    seq = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    testcd = Column(String, unique=True, nullable=False)
    test = Column(String)
    orres = Column(DOUBLE_PRECISION)
    orresu = Column(String)
    co = Column(String)

class OrresuEquation(base):
    __tablename__ = 'orresu_equations'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model = Column(Enum(Models))
    testcd = Column(String, nullable=False, unique=True)
    test = Column(String)
    orresu = Column(String)

# Create tables if they do not yet exist.
base.metadata.create_all(db)


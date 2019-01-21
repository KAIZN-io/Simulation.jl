from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# create an engine to connect to the databse with
db = create_engine('postgresql://postgres@db_postgres/simulation_results')

# create the base for all database classes to inherit from
base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

# create an engine to connect to the databse with
db_engine = create_engine('postgresql://postgres@db_postgres/simulation_results')

# create the base for all database classes to inherit from
base = declarative_base()

# the Session class to derive sessions from
Session = sessionmaker(bind=db_engine)

@contextmanager
def sessionScope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


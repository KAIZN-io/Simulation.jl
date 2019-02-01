from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os


# create the base for all database classes to inherit from
base = declarative_base()

class ThreadScopedSession:
    """
    Class for managing sessions for each process

    The Problem:
    We have the main process running flask. Each simulation is run in an induvidual
    child process which is forked from the main process. When forking a new child
    process for a simultaion, the child process inherits all database connections from
    the main process. But when you try to use these inherited database connections,
    you run into errors as you cannot share connections across processes.

    The Solution:
    For each process - main and child ones - we create a new database engine via
    `create_engine` as the database engine is the one that holds the database
    connections. This way each process has its own engine and thus own connections which
    no othe process will use. And so we don't get into any trouble.

    The How:
    This `ThreadScopedSession` class serves as a singleton wrapper for the
    `_ThreadScopedSession` class, which holds the real functionality. It has a dict
    where the keys are the process ids and as value there is an instances of the
    `_ThreadScopedSession` class. Whenever a new `ThreadScopedSession` shall be created,
    by running `ThreadScopedSession()`, the dict is looked up to check if there already
    exists and instance of `_ThreadScopedSession` for the current process. If there is an
    instance of `_ThreadScopedSession` for the current process, the instance is returned
    and no new instance is created. If no instance exists, a new one is created and added
    to the dict and returned.
    """

    # the dict holding the `_ThreadScopedSession` instances for each process
    threadScopedSessions = {}

    # the wrapped class
    class _ThreadScopedSession:
        """Holds the database engine and session registry for the current process"""

        def __init__(self, pid):
            self.pid = pid
            # create a new database engine that has no inherited connections from the parent process
            self.engine = create_engine('postgresql://postgres@db_postgres/simulation_results')
            # create a session registry to create usable session instances to query the database with
            self.sessionRegistry = scoped_session(sessionmaker(bind=self.engine))

        def __call__(self):
            """
            Returns the scoped session for this thread from the session registry

            This function was designed to model the behaviour of the scoped session of
            SQL Alchemy, where you also can call the sessino registry and retrieve the session.
            """
            return self.sessionRegistry()

        def getEngine(self):
            return self.engine

        def remove(self):
            """Cleans up everything to make sure we don't bloat the memory"""
            self.sessionRegistry.remove()
            del self.sessionRegistry
            del self.engine

    def __new__(cls):
        """
        This function returns the `_ThreadScopedSession` instance for the current process

        This function is executed, then we run `ThreadScopedSession()`. It looks up the
        dict to see if there is already an instance of `_ThreadScopedSession` for this
        process. If there is none, a new one is created, added to the list and returned.
        If there already exists an instance of `_ThreadScopedSession` for the current
        process, the instance is returned.
        """
        # get the current process id
        pid = os.getpid()

        # check if we do not yet have a `_ThreadScopedSession` for the current process
        if pid not in ThreadScopedSession.threadScopedSessions:
            # create the new `_ThreadScopedSession` and add it to the dict
            ThreadScopedSession.threadScopedSessions[pid] = ThreadScopedSession._ThreadScopedSession(pid)

        return ThreadScopedSession.threadScopedSessions[pid]

@contextmanager
def sessionScope():
    """Provide a transactional scope around a series of operations."""
    # get the thread scoped session for the current thread an out of it the session to perform queries with
    session = ThreadScopedSession()()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


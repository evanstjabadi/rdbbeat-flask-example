"""The base management for the database connection"""
import logging
from contextlib import contextmanager
from functools import lru_cache
from typing import Any, Callable, Generator

import sqlalchemy.orm
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://dev:dev@localhost:5432/database"

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def create_engine(database_url: str) -> Engine:
    """
    A database-engine factory.

    Will return an existing engine for a provided URL should one already exist.
    There should not be more than one engine creation per database per instance.
    https://docs.sqlalchemy.org/en/14/core/connections.html#basic-usage
    """
    engine = sqlalchemy.create_engine(database_url)
    logger.debug("created engine for %s", database_url)
    return engine


def create_session_maker(database_url: str) -> sqlalchemy.orm.sessionmaker:
    """A thread-safe session-maker factory."""
    # Set up the session factory to be threadsafe
    Session = sqlalchemy.orm.sessionmaker(
        bind=create_engine(database_url), expire_on_commit=False, autoflush=False
    )

    return Session


def create_session_generator(database_url: str) -> Callable[[], Any]:
    """A session-generator factory."""

    Session = create_session_maker(database_url)

    def session_generator() -> Generator[sqlalchemy.orm.Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = Session()
        try:
            yield session
            session.commit()
        except:  # noqaE722
            session.rollback()
            raise
        finally:
            session.close()

    return session_generator


def create_session_scope(database_url: str) -> Callable:
    """
    A context-managed session-scope factory.
    Will commit on success, rollback on failure, and close on completion.

    Usage:
    ```
    session_scope = create_session_scope(<database_url>)
    with session_scope() as session:
        ...
        session.add(<object>)
    ```
    """
    session_generator = create_session_generator(database_url)
    # This creates a context manager out of the session_generator
    session_scope = contextmanager(session_generator)

    return session_scope


# This is imported by the cli and ad-hoc for debugging purposes
Session = create_session_maker(DATABASE_URL)
# This is used by views to create a scope using FastAPIs dependency injection framework
session_generator = create_session_generator(DATABASE_URL)
# This is used throughout the codebase for write to the database session
session_scope = create_session_scope(DATABASE_URL)

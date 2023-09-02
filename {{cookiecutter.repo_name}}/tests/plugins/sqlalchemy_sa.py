import alembic
import alembic.config
import alembic.command

{%- if cookiecutter.persistence == 'sqlalchemy-postgres' %}
import testing.postgresql
{%- endif %}

import pytest
from {{cookiecutter.repo_name}} import models
from {{cookiecutter.repo_name}}.models.meta import Base
import transaction


{%- if cookiecutter.persistence == 'sqlalchemy-postgres' %}

def handler(postgresql):
    pass


@pytest.fixture(scope="session")
def postgresql():
    return testing.postgresql.PostgresqlFactory(
        cache_initialized_db=True, on_initialized=handler
    )


@pytest.fixture(scope="session")
def dbengine(app_settings, postgresql):
    postgresql = postgresql()
    app_settings["sqlalchemy.url"] = postgresql.url()
    engine = models.get_engine(app_settings)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    postgresql.stop()

{%- else %}

@pytest.fixture(scope='session')
def dbengine(app_settings, ini_file):
    engine = models.get_engine(app_settings)

    alembic_cfg = alembic.config.Config(ini_file)
    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)

{%- endif %}


@pytest.fixture
def tm():
    tm = transaction.TransactionManager(explicit=True)
    tm.begin()
    tm.doom()

    yield tm

    tm.abort()


@pytest.fixture
def dbsession(app, tm):
    session_factory = app.registry['dbsession_factory']
    return models.get_tm_session(session_factory, tm)



import os
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig
import pytest
import webtest

from {{ cookiecutter.repo_name }} import main
from {{ cookiecutter.repo_name }} import models
from {{ cookiecutter.repo_name }}.models.meta import Base


pytest_plugins = [
    {%- if cookiecutter.rpc == 'grpc' %}
    "tests.plugins.grpc",
    {%- endif %}
    {%- if cookiecutter.orchestrator == 'conductor' %}
    "tests.plugins.conductor",
    {%- endif %}
    {%- if cookiecutter.tasks == 'celery' %}
    "tests.plugins.celery",
    {%- endif %}
    {%- if cookiecutter.authentication == 'jwt' %}
    "tests.plugins.jwt",
    {%- endif %}
    "tests.plugins.sa",
]


def pytest_addoption(parser):
    parser.addoption('--ini', action='store', metavar='INI_FILE')


@pytest.fixture(scope='session')
def ini_file(request):
    # potentially grab this path from a pytest option
    return os.path.abspath(request.config.option.ini or 'testing.ini')


@pytest.fixture(scope='session')
def app_settings(ini_file):
    return get_appsettings(ini_file)



@pytest.fixture(scope='module')
{%- if cookiecutter.authentication == 'jwt' %}
def app(mock_public_jwks, app_settings, dbengine):
{%- else %}
def app(app_settings, dbengine):
{%- endif %}
    return main({}, dbengine=dbengine, **app_settings)


@pytest.fixture
def testapp(app, tm, dbsession):
    # override request.dbsession and request.tm with our own
    # externally-controlled values that are shared across requests but aborted
    # at the end
    testapp = webtest.TestApp(app, extra_environ={
        'HTTP_HOST': 'example.com',
        'tm.active': True,
        'tm.manager': tm,
        'app.dbsession': dbsession,
    })

    return testapp

@pytest.fixture
def app_request(app, tm, dbsession):
    """
    A real request.

    This request is almost identical to a real request but it has some
    drawbacks in tests as it's harder to mock data and is heavier.

    """
    with prepare(registry=app.registry) as env:
        request = env['request']
        request.host = 'example.com'

        # without this, request.dbsession will be joined to the same transaction
        # manager but it will be using a different sqlalchemy.orm.Session using
        # a separate database transaction
        request.dbsession = dbsession
        request.tm = tm

        yield request

@pytest.fixture
def dummy_request(tm, dbsession):
    """
    A lightweight dummy request.

    This request is ultra-lightweight and should be used only when the request
    itself is not a large focus in the call-stack.  It is much easier to mock
    and control side-effects using this object, however:

    - It does not have request extensions applied.
    - Threadlocals are not properly pushed.

    """
    request = DummyRequest()
    request.host = 'example.com'
    request.dbsession = dbsession
    request.tm = tm

    return request

@pytest.fixture
def dummy_config(dummy_request):
    """
    A dummy :class:`pyramid.config.Configurator` object.  This allows for
    mock configuration, including configuration for ``dummy_request``, as well
    as pushing the appropriate threadlocals.

    """
    with testConfig(request=dummy_request) as config:
        yield config


{%- if cookiecutter.rpc == 'grpc' %}


@pytest.fixture
def auth_grpc_metada(auth_token):
    def inner(scope: list = None, headers: dict = None):
        headers = headers or {}
        scope = {"scope": scope or []}
        metadata = {"authorization": auth_token(scope)}

        metadata.update(headers)

        return metadata

    return inner


@pytest.fixture
def grpc_testapp(
    app,
    pyramid_grpc_server,
    pyramid_grpc_channel,
    transaction_interseptor_extra_environ_mock,
    tm,
    dbsession,
    test_app_factory,
):
    # override request.dbsession and request.tm with our own
    # externally-controlled values that are shared across requests but aborted
    # at the end

    extra_environ = {
        "http_host": "example.com",
        "tm.active": "True",
        "tm.manager": tm,
        "app.dbsession": dbsession,
    }

    testapp = test_app_factory(
        app,
        server=pyramid_grpc_server,
        channel=pyramid_grpc_channel,
    )

    transaction_interseptor_extra_environ_mock(extra_environ)

    return testapp

{%- endif %}
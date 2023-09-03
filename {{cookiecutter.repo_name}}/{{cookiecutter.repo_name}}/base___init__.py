from pyramid.config import Configurator
from pyramid_auto_env import autoenv_settings

{%- if cookiecutter.persistence == 'zodb' %}
from pyramid_zodbconn import get_connection

from .models import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())
{%- endif %}


@autoenv_settings(prefix="{{cookiecutter.repo_name | upper}}")
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_{{ cookiecutter.template_language }}')
    {%- if cookiecutter.persistence == 'zodb' %}
        config.include('pyramid_tm')
        config.include('pyramid_retry')
        config.include('pyramid_zodbconn')
    {%- endif %}
    {%- if cookiecutter.rest == 'cornice' %}
        config.include('cornice')
    {%- endif %}
    {%- if cookiecutter.persistence.startswith('sqlalchemy') %}
        config.include('.models')
    {%- endif %}
    {%- if cookiecutter.persistence == 'zodb' %}
        config.set_root_factory(root_factory)
    {%- endif %}
    {%- if cookiecutter.authentication == 'jwt' %}
        config.include('.a10n')
    {%- endif %}
    {%- if cookiecutter.tasks == 'celery' %}
        config.include('pyramid_celery')
        config.include('.tasks')
    {%- endif %}
    {%- if cookiecutter.services == 'pyramid-services' %}
        config.include('pyramid_services')
        config.include('.services')
    {%- endif %}
        config.include('.routes')
    {%- if cookiecutter.rpc == 'grpc' %}
        config.include('.grpcs')
    {%- endif %}
        config.scan(ignore='.scripts')

    return config.make_wsgi_app()

{%- if cookiecutter.orchestrator  == 'conductor' %}
from celery.signals import import_modules


@import_modules.connect
def fix_params(*args, **kwargs):
    app = kwargs['sender']
    app.conf.conductor_server_api_url = app.conf['PYRAMID_REGISTRY'].settings['conductor_server_api_url']
{%- endif %}

def includeme(config):
    pass

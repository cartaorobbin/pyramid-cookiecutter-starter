def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    {%- if cookiecutter.backend != 'zodb' %}
    config.add_route('home', '/')
    {%- endif %}
    {%- if cookiecutter.rest_framework == 'cornice' %}
    config.include(".views.api", route_prefix="/api")
    {%- endif %}
    

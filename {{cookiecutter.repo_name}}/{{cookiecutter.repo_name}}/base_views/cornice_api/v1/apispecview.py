{%- if cookiecutter.rest == 'cornice' %}
from pycornmarsh import get_spec


def api_spec(request):
    ret = get_spec(
        request=request,
        title="{{cookiecutter.repo_name}} Service",
        version="1.0.0",
        description="""
        Generates a apispec to api v2 containing endpoints, schemas and can you test the requests
        """,
        {%- if cookiecutter.authentication == 'jwt' %}
        security_scheme={
            "BearerAuth": {
                "type": "http",
                "in": "header",
                "name": "Authorization",
                "scheme": "bearer",
            }
        },
        {%- endif %}
    )

    new_paths = {}

    for key in ret["paths"].keys():
        new_paths[key[1:]] = ret["paths"][key]

    ret["paths"] = new_paths
    return ret
{%- endif %}

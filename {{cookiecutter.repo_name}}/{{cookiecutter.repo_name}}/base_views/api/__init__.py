def includeme(config):
    config.include("pycornmarsh")

    config.include(".v1", route_prefix="/v1")
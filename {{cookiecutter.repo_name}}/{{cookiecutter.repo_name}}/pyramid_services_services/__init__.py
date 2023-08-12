
from {{cookiecutter.repo_name}}.services.greet_service import IGreetService, greet_service_factory


def includeme(config):
    config.register_service_factory(greet_service_factory, IGreetService)
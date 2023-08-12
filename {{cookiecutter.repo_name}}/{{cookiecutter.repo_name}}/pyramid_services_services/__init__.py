
from {{cookiecutter.repo_name}}.services.my_service import IMyService, my_service_factory


def includeme(config):
    config.register_service_factory(my_service_factory, IMyService)
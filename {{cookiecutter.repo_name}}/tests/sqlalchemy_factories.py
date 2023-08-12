import factory
from pytest_factoryboy import register

from {{cookiecutter.repo_name}}.models.mymodel import MyModel


@register
class MyModelFactory(factory.Factory):
    class Meta:
        model = MyModel

    name = "Charles Dickens"
    value = 3
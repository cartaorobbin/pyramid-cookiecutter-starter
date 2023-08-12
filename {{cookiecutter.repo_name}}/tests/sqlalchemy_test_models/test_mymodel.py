
from {{cookiecutter.repo_name}}.models.mymodel import MyModel
from tests.factories import MyModelFactory


def test_my_model(dbsession):
    my_model = MyModel(name="My Name")
    dbsession.add(my_model)
    dbsession.flush()

    assert dbsession.query(MyModel).filter(MyModel.name == "My Name").one()

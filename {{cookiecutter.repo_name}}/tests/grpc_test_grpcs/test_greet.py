import pytest

from {{cookiecutter.repo_name}}.grpcs.greet.v1 import greet_pb2_grpc, greet_pb2

def test_greet(grpc_testapp):
    """
    Just a simple grpc request
    """

    request = greet_pb2.HelloRequest(name="teste")
    resp = grpc_testapp(
        greet_pb2_grpc.GreeterStub,
        "SayHello",
        request
    )
    assert resp.message == "Hello teste"



{%- if cookiecutter.authentication != 'none' %}

def test_secure_greet_with_authorization_token(grpc_testapp, auth_grpc_metada):
    """
    Test grpc request without authorization headers
    """

    request = greet_pb2.HelloRequest(name="teste")

    resp = grpc_testapp(
        greet_pb2_grpc.GreeterStub,
        "SayHelloSecure",
        request,
        metadata=auth_grpc_metada(scope=["{{cookiecutter.repo_name}}::greet::all"])
    )
    assert resp.message == "Hello teste"


def test_secure_greet_without_authorization_token(grpc_testapp):
    """
    Test grpc request without authorization headers
    """

    request = greet_pb2.HelloRequest(name="teste")
    with pytest.raises(Exception) as exp:
        resp = grpc_testapp(
            greet_pb2_grpc.GreeterStub,
            "SayHelloSecure",
            request
        )

    assert exp.value.details() == "Permission Denied"


{%- endif %}
import pytest

from {{cookiecutter.repo_name}}.grpcs.greet.v1 import greet_pb2_grpc, greet_pb2

def test_greet(
    grpc_testapp
):

    request = greet_pb2.HelloRequest(name="teste")
    resp = grpc_testapp(
        greet_pb2_grpc.GreeterStub,
        "SayHello",
        request
    )
    assert resp.message == "Hello teste"

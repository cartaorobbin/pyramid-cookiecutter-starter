
from {{cookiecutter.repo_name}}.grpcs.greet.v1 import greet_pb2_grpc, greet_pb2
from pyramid_grpc.decorators import config_grpc_service, config_grpc_call
from pyramid.authorization import Allow
import logging

logger = logging.getLogger(__name__)


class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    
    def SayHello(self, request, context):
        return greet_pb2.HelloReply(message=f"Hello {request.name}")


@config_grpc_service
def configure(server):
    greet_pb2_grpc.add_GreeterServicer_to_server(
        GreeterServicer(), server
    )

from {{cookiecutter.repo_name}}.grpcs.healthz.v1 import healthz_pb2, healthz_pb2_grpc
from pyramid_grpc.decorators import config_grpc_service


class HealthzServiceServicer(healthz_pb2_grpc.HealthzServiceServicer):
    # Do not exposed thru grpc

    def Healthz(self, request, context):
        return healthz_pb2.Empty()


@config_grpc_service
def configure(server):
    healthz_pb2_grpc.add_HealthzServiceServicer_to_server(
        HealthzServiceServicer(), server
    )
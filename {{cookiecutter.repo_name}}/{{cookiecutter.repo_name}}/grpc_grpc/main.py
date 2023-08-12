
from {{cookiecutter.repo_name}}.grpc.interseptors import TransactionInterseptor
from .decorators import get_services



def build_interceptors(pyramid_app):
    return [TransactionInterseptor(pyramid_app)]


def configure_server(pyramid_app, grpc_server):
    for func in get_services():
        func(grpc_server, pyramid_app)


def serve(pyramid_app, grpc_server):
    
    configure_server(pyramid_app, grpc_server)

    grpc_server.add_insecure_port("[::]:50051")

    grpc_server.start()
    grpc_server.wait_for_termination()



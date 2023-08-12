from concurrent import futures
from dataclasses import dataclass
import re
from typing import Any, Callable

from zope.sqlalchemy import register

from person.grpc.interseptors import TransactionInterseptor
from .decorators import get_services



# def configure(server):
#     companies_pb2_grpc.add_CompaniesServicer_to_server(CompaniesServicer(), server)
#     companies_pb2_grpc.add_RelationshipsServicer_to_server(
#         RelationshipServicer(), server
#     )
#     persons_pb2_grpc.add_PersonsServicer_to_server(PersonsServicer(), server)

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


# if __name__ == "__main__":

#     serve(config=config)

from typing import Any, Callable
from grpc import ServicerContext, HandlerCallDetails
import transaction
from pyramid.scripting import prepare
from grpc_interceptor import ServerInterceptor



class TransactionInterseptor(ServerInterceptor):
    def __init__(self, pyramid_app, extra_environ=None):
        self.pyramid_app = pyramid_app
        self.session = pyramid_app.registry["dbsession_factory"]()
        self.extra_environ = extra_environ or {}

    def intercept(
            self,
            method: Callable,
            request: Any,
            context: ServicerContext,
            method_name: str,
    ) -> Any:

        pyramid_request = prepare(registry=self.pyramid_app.registry)['request']
        pyramid_request.environ.update(self.extra_environ)
        pyramid_request.tm.begin()
        context.pyramid_request = pyramid_request
        try:
            response = method(request, context)
            pyramid_request.tm.commit()
        except Exception as e:
            pyramid_request.tm.abort()
            raise e
        return response
from zope.interface import Interface


def greet_service_factory(context, request):
    return GreetService()


class IGreetService(Interface):
    def all():
        pass


class GreetService:

    def greet(self):
        return "Hi there!"
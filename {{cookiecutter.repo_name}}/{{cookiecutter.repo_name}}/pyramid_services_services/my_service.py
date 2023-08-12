
def optin_factory(context, request):
    return MyService()


class IOptinService(Interface):
    def all():
        pass


class MyService:

    def all(self):
        return [1, 2, 3]
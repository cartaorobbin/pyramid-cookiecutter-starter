from pyramid.authorization import ACLHelper, Everyone, Authenticated
from dataclasses import dataclass

from {{cookiecutter.repo_name}}.a10n.helper import JWtAuthenticationHelper


@dataclass
class Identity:
    sub: str
    source: str
    scope: list
    iat: int
    exp: int
    iss: str


class SecurityPolicy:
    def __init__(self, settings, helper):
        self.helper = helper

    def identity(self, request):
        """Return app-specific user object."""
        if self.helper.get_claims(request):
            return Identity(**self.helper.get_claims(request))

    def authenticated_userid(self, request):
        """Return user id."""
        identity = self.identity(request=request)
        if identity is not None:
            return identity.sub

    def permits(self, request, context, permission):
        principals = [Everyone]
        identity = self.identity(request=request)
        if identity is not None:
            principals.append(Authenticated)
            principals.append("user:" + identity.sub)
            principals.append("source:" + identity.source)
            for scope in identity.scope:
                principals.append(scope)
        return ACLHelper().permits(context, principals, permission)

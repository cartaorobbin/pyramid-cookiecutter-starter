from pyramid_jwt import JWTAuthenticationPolicy

from {{cookiecutter.repo_name}}.a10n import jwks


class JWtAuthenticationHelper:
    def __init__(self, public_key, private_key=None):
        self.jwt = JWTAuthenticationPolicy(
            private_key=private_key,
            public_key=public_key,
            auth_type="Bearer",
            default_claims=["scope", "sub", "uid", "source"],
            algorithm="RS256",
        )

    def get_claims(self, request):
        return self.jwt.get_claims(request)

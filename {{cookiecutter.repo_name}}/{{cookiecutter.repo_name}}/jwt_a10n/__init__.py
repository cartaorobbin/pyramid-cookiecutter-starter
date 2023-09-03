from {{cookiecutter.repo_name}}.a10n.helper import JWtAuthenticationHelper
from {{cookiecutter.repo_name}}.a10n.police import SecurityPolicy
from {{cookiecutter.repo_name}}.a10n.jwks import get_public_pen


def includeme(config):
    config.include("pyramid_jwt")

    private_key = (config.registry.settings["jwt.private_key"],)
    public_key = get_public_pen(config.registry.settings["jwks.url"])
    helper = JWtAuthenticationHelper(public_key=public_key, private_key=private_key)

    config.set_security_policy(SecurityPolicy(config.registry.settings, helper=helper))

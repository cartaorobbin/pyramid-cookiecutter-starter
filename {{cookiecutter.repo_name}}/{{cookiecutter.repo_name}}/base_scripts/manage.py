from dataclasses import dataclass
from gc import callbacks
import requests
import click
from pyramid.paster import bootstrap, setup_logging

import logging
logger = logging.getLogger(__name__)

@dataclass
class Context:
    pyramid_app: object
    pyramid_request: object


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--url", default="http://localhost:6543/health", help="Number of greetings."
)
def health(url):
    click.echo(f"checking {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    click.echo(f"health check passed - {response.status_code}")




@cli.group(name="pyramid-app")
@click.argument('ini_location')
@click.pass_context
def pyramid_app(ctx, ini_location):
    """Simple program that greets NAME for a total of COUNT times."""

    logger.info('Starting server')
    env = bootstrap(ini_location)

    registry = env['registry']
    app = env['app']
    root = env['root']
    request = env['request']
    closer = env['closer']

    {%- if cookiecutter.backend == 'sqlalchemy' %}
    request.tm.begin()

    ctx.obj = Context(pyramid_app=app,pyramid_request=request)
    @ctx.call_on_close
    def commit():
        request.tm.commit()
    {%- endif %}


if __name__ == "__main__":
    cli()

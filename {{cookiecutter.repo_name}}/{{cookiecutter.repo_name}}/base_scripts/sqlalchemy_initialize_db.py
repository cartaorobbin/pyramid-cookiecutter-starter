import argparse
import sys
import alembic

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError
import alembic.config
import alembic.command
from ..models.meta import Base

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    pass


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            Base.metadata.create_all(bind=dbsession.get_bind())
            alembic_cfg = alembic.config.Config(args.config_uri)
            alembic.command.stamp(alembic_cfg, "head")
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')

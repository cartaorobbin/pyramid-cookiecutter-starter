import os
import pytest
import sys
import subprocess
import textwrap

from tests.expected_files import base_files, sqlalchemy_files, zodb_files, pyramid_services_files
from tests.utils import build_files_list, WIN, WORKING


@pytest.mark.parametrize('docs', ["none", "sphinx"])
@pytest.mark.parametrize('tasks', ["none", "celery"])
@pytest.mark.parametrize('pyramid_services', ["none", "pyramid-services"])
@pytest.mark.parametrize('rpc', ["none", "grpc"])
@pytest.mark.parametrize('authentication', ["none", "jwt"])
@pytest.mark.parametrize('schemas', ["none", "marshmallow"])
@pytest.mark.parametrize('rest_framework', ["none", "cornice"])
@pytest.mark.parametrize('backend', ["none", "sqlalchemy", "zodb"])
@pytest.mark.parametrize('template', ['jinja2', 'mako', 'chameleon'])
def test_base(cookies, venv, capfd, template, backend, rest_framework, schemas, pyramid_services, authentication, rpc, tasks, docs):

    if backend != 'sqlalchemy':
        return
    
    if rest_framework != 'cornice':
        return

    if schemas != 'marshmallow':
        return

    if pyramid_services != 'pyramid-services':
        return

    if authentication != 'jwt':
        return

    if rpc != 'grpc':
        return

    if tasks != 'celery':
        return

    if docs != 'sphinx':
        return

    result = cookies.bake(extra_context={
        'project_name': 'Test Project',
        'template_language': template,
        'backend': backend,
        'rest_framework': rest_framework,
        'schemas': schemas,
        'pyramid_services': pyramid_services,
        'authentication': authentication,
        'rpc': rpc,
        'tasks': tasks,
        'docs': docs,
        'repo_name': 'myapp',
    })

    assert result.exit_code == 0

    out, err = capfd.readouterr()

    if WIN:
        assert 'Scripts\\pserve' in out
        for idx, base_file in enumerate(base_files):
            base_files[idx] = base_file.replace('/', '\\')
        base_files.sort()

    else:
        assert 'bin/pserve' in out

    cwd = str(result.project_path)

    # this is a hook for executing scaffold tests against a specific
    # version of pyramid (or a local checkout on disk)
    if 'OVERRIDE_PYRAMID' in os.environ:  # pragma: no cover
        venv.install(os.environ['OVERRIDE_PYRAMID'], editable=True)

    # venv.install(cwd, editable=True, upgrade=True)
    subprocess.call([venv.bin + '/pip', 'install', 'poetry'], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'config', 'virtualenvs.create', 'false', '--local'], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'install'], cwd=cwd)
    subprocess.check_call([venv.bin + '/poetry', 'run', 'pytest'], cwd=cwd)
    subprocess.check_call([venv.bin + '/poetry', 'run', 'proutes', 'development.ini'], cwd=cwd)


def test_it_invalid_module_name(cookies, venv, capfd):
    result = cookies.bake(extra_context={
        'repo_name': '0invalid',
    })
    assert result.exit_code == -1

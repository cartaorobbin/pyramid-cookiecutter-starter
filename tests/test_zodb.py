import pytest
import os
import subprocess
import textwrap

from tests.expected_files import zodb_files
from tests.utils import build_files_list, WIN, WORKING


@pytest.mark.parametrize('template', ['jinja2', 'mako', 'chameleon'])
def test_zodb(cookies, venv, capfd, template):
    result = cookies.bake(extra_context={
        'project_name': 'Test Project',
        'template_language': template,
        'backend': 'zodb',
        'repo_name': 'myapp',
    })

    assert result.exit_code == 0

    out, err = capfd.readouterr()

    if WIN:
        assert 'Scripts\\pserve' in out
        for idx, zodb_file in enumerate(zodb_files):
            zodb_files[idx] = zodb_file.replace('/', '\\')
        zodb_files.sort()
    else:
        assert 'bin/pserve' in out

    # Get the file list generated by cookiecutter. Differs based on backend.
    files = build_files_list(str(result.project_path))
    files.sort()

    # Rename files based on template being used
    if template == 'chameleon':
        template = 'pt'

    for idx, zodb_file in enumerate(zodb_files):
        if 'templates' in zodb_file:
            zodb_files[idx] = zodb_files[idx].split('.')[0] + '.' + template

    assert zodb_files == files

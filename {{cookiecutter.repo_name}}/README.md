{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

Getting Started
---------------

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.md file.

```bash
    cd {{ cookiecutter.repo_name }}
```

- If you are using Visual Studio Code just reopen the window

Otherwise

- Create a Python virtual environment, if not already created.

```bash
    python3 -m venv env
```

- Upgrade packaging tools, if necessary.

```bash
    env/bin/pip install --upgrade pip setuptools
    env/bin/pip install --upgrade poetry
```

- Install the project in editable mode with its testing requirements.

```bash
    env/bin/poetry install
    env/bin/poetry shell
```

{% if cookiecutter.backend == 'sqlalchemy' -%}
- Initialize and upgrade the database using Alembic.

    - Generate your first revision.
```bash
        alembic -c development.ini revision --autogenerate -m "init"
```
    - Upgrade to that revision.
```bash
        alembic -c development.ini upgrade head
```

- Load default data into the database using a script.
```bash
    initialize_{{ cookiecutter.repo_name }}_db development.ini
```
{% endif -%}
- Run your project's tests.
```bash
   pytest
```
- Run your project.

```bash
   pserve development.ini
```

- Access project the shell.

```bash
   pshell development.ini
```

{% if cookiecutter.rpc == 'grpc' -%}

- Run your grpc server.

```bash
   grpc-server development.ini
```
{% endif -%}
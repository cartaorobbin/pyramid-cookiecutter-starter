.PHONY: clean-pyc fmt clear-poetry-cache docker-build docker-run

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


clear-poetry-cache:
	poetry cache clear --all .

fmt:
	poetry run black -l 129 -v {{cookiecutter.repo_name}}
	poetry run black -l 129 -v tests

docker-build:
	docker build -t {{cookiecutter.repo_name}}:latest .

docker-run:
	docker run -it --rm {{cookiecutter.repo_name}}:latest


{%- if cookiecutter.rpc == 'grpc' %}
protos:
	python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/{{cookiecutter.repo_name}}/grpcs/healthz/v1/healthz.proto
	python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/{{cookiecutter.repo_name}}/grpcs/greet/v1/greet.proto
{%- endif %}

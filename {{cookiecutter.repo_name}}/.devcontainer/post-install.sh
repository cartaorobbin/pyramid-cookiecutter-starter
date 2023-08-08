#!/bin/bash

poetry config virtualenvs.in-project true
poetry install

source .venv/bin/activate
PATH=$PATH:.venv/bin

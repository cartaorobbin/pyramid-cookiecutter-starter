#!/bin/bash

poetry config virtualenvs.create true
poetry install

poetry shell

ssh-keygen -R 20.201.28.151
#!/bin/bash

if [ -f devcontainer.env ]; then
  export $(echo $(cat devcontainer.env | sed 's/#.*//g'| xargs) | envsubst)
fi


poetry config virtualenvs.create true
poetry install
poetry shell

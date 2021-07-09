#!/usr/bin/env bash

deployment_venv="python3-deploy-$(date +%s)"
python3 -m venv ./$deployment_venv
source ./$deployment_venv/bin/activate
if [ -f ./requirements.txt ]; then
    pip3 install -r requirements.txt
fi
python ./$1
deactivate
rm -rf ./$deployment_venv && rm -rf __pycache__
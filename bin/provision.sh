#!/bin/bash

cd ../provisioning && python3 -m venv venv && source ./venv/bin/activate && pip install -r requirements.txt
cdk synth
cdk bootstrap -y
cdk deploy

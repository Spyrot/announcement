#!/bin/bash

cd .. && pip install -r ./app/requirements.txt --target ./package
cd ./package && zip -r ../provisioning/lambda.zip .
cd ../app/ && zip -r ../provisioning/lambda.zip .

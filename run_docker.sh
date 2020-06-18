#!/bin/bash

chown

docker build -t figgy-python:demo .

# The ~/.aws/ directory is mounted into the container to give the container access to IAM credentials
# figgy/ is mounted into the container so the container can write the updated figgy.json file to our config/ dir.

docker run -e LOCAL_RUN=true -p 5000:5000 \
    -v ~/.aws/:/root/.aws/ \
    -v $(PWD)/figgy/:/app/figgy/ \
    figgy-python:demo
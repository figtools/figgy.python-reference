#!/bin/bash

echo "Installing pip depdendencies."
pip3 install -r src/requirements.txt >> /dev/null

echo "Setting LOCAL_RUN=true - this makes sure we generate the figgy.json file"
export LOCAL_RUN=true

echo "Running app."
python3 src/app.py
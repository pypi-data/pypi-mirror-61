#!/bin/sh
# create a virtualenv, active it, and install pip-tools
python3.6 -m venv $1
source ./$1/bin/activate
pip install pip-tools==3.1.0

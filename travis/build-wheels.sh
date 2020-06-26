#!/bin/bash
set -e -u -x

pip install -r /io/dev-requirements.txt
pip wheel /io/ --no-deps 
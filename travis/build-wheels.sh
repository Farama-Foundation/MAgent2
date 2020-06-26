#!/bin/bash
set -e -u -x

for PYBIN in /opt/python/*/bin; do
    if [[ ( "$PYBIN" != *"27"* ) && ( "$PYBIN" != *"35"* ) ]]; then
        "${PYBIN}/pip" install -r /io/requirements.txt
        "${PYBIN}/pip" wheel /io/ --no-deps -w wheelhouse/
    fi
done
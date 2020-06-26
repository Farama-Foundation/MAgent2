#!/bin/bash
set -e -u -x

wget https://cmake.org/files/v3.12/cmake-3.12.3.tar.gz
tar zxvf cmake-3.*
cd cmake-3.*
./bootstrap --prefix=/usr/local
make -j$(nproc)
make install
cd ..

for PYBIN in /opt/python/*/bin; do
    if [[ ( "$PYBIN" != *"27"* ) && ( "$PYBIN" != *"35"* ) ]]; then
        "${PYBIN}/pip" install -r /io/requirements.txt
        "${PYBIN}/pip" wheel /io/ --no-deps -w wheelhouse/
    fi
done
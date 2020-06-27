#!/bin/bash
set -e -u -x

yum install -y wget

wget https://github.com/Kitware/CMake/releases/download/v3.15.2/cmake-3.15.2.tar.gz > /dev/null
tar -zxvf cmake-3.15.2.tar.gz > /dev/null
cd cmake-3.15.2
./bootstrap > /dev/null
make -j$(nproc)
make install
cd ..

for PYBIN in /opt/python/*/bin; do
    if [[ ( "$PYBIN" == *"36"* ) || ( "$PYBIN" != *"37"* ) || ( "$PYBIN" != *"38"* ) ]]; then
        "${PYBIN}/pip" install -r /io/requirements.txt
        "${PYBIN}/pip" wheel /io/ --no-deps -w wheelhouse/
    fi
done
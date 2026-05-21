set shell := ["bash", "-cu"]

venv := ".venv"
python := venv + "/bin/python"

default:
    @just --list

docs-install:
    python3 -m venv {{venv}}
    {{python}} -m pip install --upgrade pip
    {{python}} -m pip install cmake
    {{python}} -m pip install .
    {{python}} -m pip install -r docs/requirements.txt

docs-serve: docs-install
    {{python}} docs/scripts/gen_mds.py
    {{venv}}/bin/sphinx-autobuild docs docs/_build/html --open-browser

docs-build: docs-install
    {{python}} docs/scripts/gen_mds.py
    {{venv}}/bin/sphinx-build -b html docs docs/_build/html

docs-clean:
    rm -rf docs/_build

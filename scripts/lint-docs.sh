#!/bin/sh
set -e

folders="docs"

set -x

# check the docs with doc8
python3 -m doc8 $folders --quiet

# check package build for README.rst
rm -rf dist
python3 setup.py --quiet sdist
python3 -m twine check dist/*

#!/bin/sh
set -e

folders="codingame tests examples docs setup.py"

set -x

# put every import on one line for autoflake remove unused imports
python3 -m isort $folders --force-single-line-imports
# remove unused imports and variables
python3 -m autoflake $folders --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py
# resort imports
python3 -m isort $folders

# format code
python3 -m black $folders --line-length 80

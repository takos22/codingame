#!/bin/sh
set -e

folders="codingame tests examples docs setup.py"

set -x

# put every import on one line for autoflake remove unused imports
isort $folders --force-single-line-imports
# remove unused imports and variables
autoflake $folders --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py
# resort imports
isort $folders

# format code
black $folders --line-length 80

#!/bin/sh
set -e

folders="codingame tests examples"

set -x

# put every import on one line for autoflake remove unused imports
isort $folders --force-single-line-imports
# remove unused imports and variables
autoflake $folders --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py

# format code
black $folders --line-length 80

# resort imports
isort $folders

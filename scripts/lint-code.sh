#!/bin/sh
set -e

folders="codingame tests examples docs setup.py"

set -x

# stop the build if there are Python syntax errors or undefined names
python3 -m flake8 $folders --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
python3 -m flake8 $folders --count --exit-zero --statistics

# check formatting with black
python3 -m black $folders --check --line-length 80

# check import ordering with isort
python3 -m isort $folders --check-only

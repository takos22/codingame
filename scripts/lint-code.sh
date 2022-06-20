#!/bin/sh
set -e

folders="codingame tests examples docs setup.py"

set -x

# stop the build if there are Python syntax errors or undefined names
flake8 $folders --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
flake8 $folders --count --exit-zero --statistics

# check formatting with black
black $folders --check --line-length 80

# check import ordering with isort
isort $folders --check-only

#!/bin/sh
set -e
set -x

python3 -m pytest --only-mocked --overwrite-environ
python3 -m pytest --no-mocking --cov-append

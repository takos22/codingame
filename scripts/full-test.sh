#!/bin/sh
set -e
set -x

pytest --only-mocked --overwrite-environ
pytest --no-mocking --cov-append

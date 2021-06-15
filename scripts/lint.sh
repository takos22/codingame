#!/bin/sh
set -e

# lint code
./scripts/lint-code.sh

# lint docs and README
./scripts/lint-docs.sh

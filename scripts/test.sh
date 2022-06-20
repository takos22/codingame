#!/bin/sh
set -e

lint=true
full=false

# no linitng if -n or --no-lint flag
for arg in "$@"
do
    if [ "$arg" == "-n" ] || [ "$arg" == "--no-lint" ]; then
        lint=false
    fi
    if [ "$arg" == "-f" ] || [ "$arg" == "--full" ]; then
        full=true
    fi
done

if [ "$lint" = true ]; then
    # lint
    ./scripts/lint.sh
fi


if [ "$full" = true ]; then
    # lint
    ./scripts/full-test.sh
else
    set -x
    pytest
fi

#!/bin/bash
set -evu

python setup.py sdist
for sdist in $TRAVIS_BUILD_DIR/dist/*.tar.gz
    do curl -F package=@"$sdist" https://${FURY_PUSH}@push.fury.io/cqcl/
done
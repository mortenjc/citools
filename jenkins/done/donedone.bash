#!/bin/bash

SCRIPTS="done_merged.bash done_builds.bash done_run.bash done_tests.bash done_coverage.bash done_doxygen.bash"

function errexit()
{
    echo "Error: $1 failed"
    exit 1
}

cd testproject
make clean

for script in $SCRIPTS
do
    echo Running script $script
    ../jenkins/done/$script || errexit $done
done

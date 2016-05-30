#!/bin/bash

BANNER=banner

type banner >/dev/null || BANNER=echo

function errexit()
{
   echo "Error: "$1
   $BANNER FAIL 
   exit 1
}


MINCOV=73.0

#
#
$BANNER Build cov 

make clean
make COVERAGE=y test || errexit "test build failed"

#
#
$BANNER Run tests

make testrun || errexit "some tests failed"

#
#
make coverage |tee build/coverage.log || errexit "coverage extraction failed"

#
#

COV=$(cat build/coverage.log | grep "lines..." | awk '{print $2}' | tail -n 1 | sed -e 's/%//g')

cat build/coverage.log | grep "lines..." | awk '{print $2}' | tail -n 1 | sed -e 's/%//g' || errexit "no coverage data"

#
#
if [ "$(echo $COV '>' $MINCOV | bc -l)" -eq 0 ];then
   errexit "Minimum coverage of $MINCOV % not met (got $COV %)"
fi

$BANNER DONE

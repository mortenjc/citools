#!/bin/bash

BANNER=banner

type banner >/dev/null || BANNER=echo

function errexit()
{
   echo "Error: "$1
   $BANNER FAIL 
   exit 1
}

#
#
#
$BANNER Build all

make V=y all || errexit "failed to build project"

#
#
#
$BANNER Build test

make clean

make COVERAGE=y test || errexit "failed to build tests"

$BANNER DONE

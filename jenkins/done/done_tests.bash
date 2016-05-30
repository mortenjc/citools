#!/bin/bash

BANNER=banner

type banner >/dev/null || BANNER=echo

function errexit()
{
   echo "Error: "$1
   $BANNER FAIL 
   exit 1
}

$BANNER Run tests

make testrun || errexit "some tests failed"


$BANNER DONE

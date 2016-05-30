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
$BANNER Run prog 

make clean

make V=y run || errexit "failed to run application"

$BANNER DONE

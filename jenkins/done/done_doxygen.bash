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
$BANNER Doxygen 

cd $WORKSPACE
doxygen doxygen/config.dox testproject || errexit "doxygen failed"

#
#
test -s doxygenerrors.log && errexit "doxygen errors were generated"


$BANNER DONE

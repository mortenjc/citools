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

pushd $WORKSPACE/citest
doxygen ../doxygen/config.dox . || errexit "doxygen failed"

#
#
test -s doxygenerrors.log && errexit "doxygen errors were generated"

popd
$BANNER DONE

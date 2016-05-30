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

git fetch

git checkout mjcdev || errexit "cant change to devmjc branch"

git diff master > mydiff

test -s mydiff && errexit "branch mjcdev not merged with master"


$BANNER DONE

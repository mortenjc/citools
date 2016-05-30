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

$BANNER Fetch
git fetch

git status
git branch -a

$BANNER Chkout
git checkout mjcdev || errexit "cant change to devmjc branch"


$BANNER Compare 
git diff master > mydiff

test -s mydiff && errexit "branch mjcdev not merged with master"

$BANNER DONE

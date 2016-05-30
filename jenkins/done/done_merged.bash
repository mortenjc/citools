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
git merge master | grep "Already up-to-date" || errexit "branch is not merged from master"

$BANNER DONE

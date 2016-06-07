#!/bin/bash


function argcheck()
{
   if [[ $1 == "" ]]; then
      echo "Missing argument"
      exit
   fi
}

function helptext()
{
   echo "s3 commands"
   echo "  s3dir    bucket  	list entries in bucket"
   echo "  s3list		lists the users buckets"
   echo "  s3create bucket      creates a new bucket" 
   echo "  s3delete bucket      deletes bucket with content"
   echo 
   echo "ec2 commands"

}

function s3commands()
{
case $awscmd in

"s3list")
  aws s3api list-buckets
  ;;

"s3dir")
  argcheck $arg
  aws s3 ls s3://$arg
  ;;

"s3create")
  argcheck $arg
  aws s3api create-bucket --acl private --bucket $arg
  ;;

"s3delete")
  argcheck $arg
  aws s3 rm s3://$arg --recursive
  aws s3api delete-bucket --bucket $arg
  ;;

*)
   helptext
   exit 
   ;;
esac
exit 
}


#run-instances --image-id "ami-d0f89fb9" --key-name mjctestkeypair --instance-type t1.micro --security-groups quicklaunch-1 
#aws ec2 describe-instances


awscmd=$1
arg=$2

[[ $awscmd =~ s3.*  ]] && s3commands  
[[ $awscmd =~ ec2.* ]] && ec3commands

helptext

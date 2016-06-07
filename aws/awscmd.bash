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
   echo "  s3dir    bucket      list entries in a bucket"
   echo "  s3list               lists the user\'s buckets"
   echo "  s3create bucket      creates a new bucket" 
   echo "  s3delete bucket      deletes bucket with content"
   echo 
   echo "ec2 commands"
   echo "  ec2list              list available instances"
   echo "  ec2run keys          run a t2.micro instance with specified keys"
   echo "  ec2stop instance     stop a running instance"
   echo "  ec2delete instance   delete a stopped instance"

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


function ec2commands()
{
case $awscmd in

"ec2list")
  aws ec2 describe-instances
  ;;

"ec2run")
  argcheck $arg
  aws ec2 run-instances --image-id ami-f5f41398 --count 1 --key-name $arg  --instance-type t2.micro --subnet-id subnet-7889a045
  ;;

"ec2stop")
  argcheck $arg
  aws ec2 stop-instances --instance-ids $arg
  ;;

"ec2delete")
  argcheck $arg
  aws ec2 terminate-instances --instance-ids $arg
  ;;

esac
exit
}


#
# Script starts here
#

awscmd=$1
arg=$2
arg2=$3

[[ $awscmd =~ s3.*  ]] && s3commands  
[[ $awscmd =~ ec2.* ]] && ec2commands

helptext

# Amazon Web Services CLI Python scripts
These files implements some of the commands for the Amazon Web Services API.

So far only a subset of EC2 and S3 commands have been implemented. The AWS API
is implemented in the class awscommands (awscommands.py). To demonstrate the
usage you can use the example shells ec2_shell.py and s3_shell.py.

## Basic EC2 functionality
This includes creating and deleting key_pairs, listing all available
ec2 instances, describing a specific instance id, running, stopping and
terminating instances. List create and delete security groups.

## Basic S3 functionality
Show, create, delete buckets. Copy files to buckets. Delete files in buckets

## Running

    > ./awscommands.py
    > ./ec2_shell.py
    > ./s3_shell.py

## Configuration
Some default parameters can be supplied using a config file (.awscfg) which
should be edited and copied to your home directory.

#!/usr/bin/python

import cmd, sys, os


def adds3(text):
   if not text.startswith("s3://"):
      return "s3://" + text 
   else:
      return text

def call(cmd):
   output = os.popen(cmd).read()
   print output


class AWShell(cmd.Cmd):

   intro = "AWS Shell"
   prompt = '(awshell) '
   file = None

   subnet="subnet-7889a045"
   ami="ami-f5f41398"

#
#  S3 Commands
#
   def do_s3_list(self, line):
      'List all buckets'
      call("aws s3api list-buckets")

   def do_s3_create(self, line):
      'Create an S3 bucket by name'
      bucket = line.split()[0]
      call("aws s3api create-bucket --acl private --bucket %s" % (bucket))

   def do_s3_delete(self, line):
      'Delete an S3 bucket by name'
      bucket = line.split()[0]
      call("aws s3api delete-bucket --bucket %s" % (bucket))

   def do_s3_ls(self, line):
      'List contents of bucket'
      bucket = adds3(line.split()[0])
      call("aws s3 ls %s" % (bucket))

   def do_s3_rm(self, line):
      'Remove file from bucket'
      file = adds3(line.split()[0])
      call("aws s3 rm %s" % (file))

   def do_s3_cp(self, line):
      'Copy file from bucket'
      src = line.split()[0]
      dst = line.split()[1]
      call("aws s3 cp %s %s" % (src, dst))


#
# EC2 Commands
#

   def do_ec2_list(self, line):
      'List all AWS instances'
      call("aws ec2 describe-instances")

   def do_ec2_run(self, line):
      'Run instance - specify keys'
      keys = line.split()[0]
      call("aws ec2 run-instances --image-id %s --count 1 --key-name %s  --instance-type t2.micro --subnet-id %s" % (ami, keys, subnet))

   def do_ec2_stop(self, line):
      'Stop a running instance by instance_id'
      instanceid = line.split()[0]
      call("aws ec2 stop-instances --instance-ids %s" % (instanceid))

   def do_ec2_delete(self, line):
      'Terminate instance by id'
      instanceid = line.split()[0]
      call("aws ec2 terminate-instances --instance-ids %s" % (instanceid))

#
# CMD behavior customization
#
   def do_shell(self, line):
      'Run a shell command'
      output = os.popen(line).read()
      print output

   def do_EOF(self, line):
      return True

   def emptyline(self):
      print self.prompt

   def do_quit(self, arg):
      'Quit the shell'
      sys.exit(0)

if __name__ == '__main__':
   AWShell().cmdloop()

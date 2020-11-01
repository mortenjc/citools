#!/usr/local/bin/python3

import cmd, sys, os
from awscommands import awscommands

class AWShell(cmd.Cmd):
   intro = "AWS Shell"
   prompt = '(s3) '
   aws = awscommands()

   def __init__(self):
      cmd.Cmd.__init__(self)

#
#  S3 Commands
#
   def do_list(self, unused):
      'List all buckets'
      self.aws.bucket_list()

   def do_create(self, name):
      'Create an S3 bucket by name'
      self.aws.bucket_create(name)

   def do_delete(self, name):
      'Delete an S3 bucket by name'
      self.aws.bucket_delete(name)

   def do_ls(self, name):
      'List contents of bucket'
      self.aws.bucket_ls(name)

   def do_rm(self, file):
      'Remove file from bucket'
      self.aws.bucket_rm(file)

   def do_cp(self, line):
      'Copy file from bucket'
      self.aws.bucket_cp(line)


#
# CMD behavior customization
#
   def do_EOF(self, line):
      return True

   def emptyline(self):
      print(self.prompt)

   def do_quit(self, arg):
      'Quit the shell'
      sys.exit(0)

if __name__ == '__main__':
   AWShell().cmdloop()

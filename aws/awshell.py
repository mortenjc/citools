#!/usr/bin/python

import cmd, sys, subprocess

class AWShell(cmd.Cmd):
   intro = "AWS Shell"
   prompt = '(awshell) '
   file = None

   def do_s3list(self, arg):
      'List all buckets'
      subprocess.call(["aws", "s3api",  "list-buckets"])

   def do_s3create(self, arg):
      'Create an S3 bucket by name'
      subprocess.call(["aws", "s3api", "create-bucket", "--acl",  "private", "--bucket", arg])

   def do_s3delete(self, arg):
      'Delete an S3 bucket by name'
      subprocess.call(["aws", "s3api", "delete-bucket", "--bucket", arg])

   def do_quit(self, arg):
      'Quit the shell'
      sys.exit(0)

if __name__ == '__main__':
   AWShell().cmdloop()

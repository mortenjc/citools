#!/usr/bin/python

import cmd, sys, subprocess

class AWShell(cmd.Cmd):
   intro = "AWS Shell"
   prompt = '(awshell) '
   file = None

   def do_s3list(self, arg):
      'List all buckets'
      subprocess.call(["aws", "s3api",  "list-buckets"])

   def do_quit(self, arg):
      sys.exit(0)

if __name__ == '__main__':
   AWShell().cmdloop()

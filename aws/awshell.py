#!/usr/bin/python

import cmd, sys

class AWShell(cmd.Cmd):
   intro = "AWS Shell"
   prompt = '(awshell) '
   file = None

   def do_s3list(self, arg):
      'List all buckets'
      print("Call s3list")

if __name__ == '__main__':
   AWShell().cmdloop()

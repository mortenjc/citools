#!/usr/bin/python

import cmd, sys, os


def adds3(text):
   if not text.startswith("s3://"):
      return "s3://" + text 
   else:
      return text


class AWShell(cmd.Cmd):

   intro = "AWS Shell"
   prompt = '(awshell) '
   file = None

#
#
#
   def do_s3list(self, line):
      'List all buckets'
      self.call("aws s3api list-buckets")

   def do_s3create(self, line):
      'Create an S3 bucket by name'
      bucket = line.split()[0]
      self.call("aws s3api create-bucket --acl private --bucket %s" % (bucket))

   def do_s3delete(self, line):
      'Delete an S3 bucket by name'
      bucket = line.split()[0]
      self.call("aws s3api delete-bucket --bucket %s" % (bucket))

   def do_s3ls(self, line):
      'List contents of bucket'
      bucket = adds3(line.split()[0])
      self.call("aws s3 ls %s" % (bucket))

   def do_s3rm(self, line):
      'Remove file from bucket'
      file = adds3(line.split()[0])
      self.call("aws s3 rm %s" % (file))

   def do_s3cp(self, line):
      'Copy file from bucket'
      src = line.split()[0]
      dst = line.split()[1]
      self.call("aws s3 cp %s %s" % (src, dst))


#
#
#
      
   def call(self, cmd):
      'Calls a (aws) command, print output'
      output = os.popen(cmd).read()
      print output

   def do_shell(self, line):
      'Run a shell command'
      output = os.popen(line).read()
      print output

   def do_quit(self, arg):
      'Quit the shell'
      sys.exit(0)

if __name__ == '__main__':
   AWShell().cmdloop()

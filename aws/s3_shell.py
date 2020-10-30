#!/usr/local/bin/python3

import cmd, sys, os


def adds3(text):
   if not text.startswith("s3://"):
      return "s3://" + text
   else:
      return text

def call(cmd):
   output = os.popen(cmd).read()
   print(output)


class AWShell(cmd.Cmd):
   intro = "AWS Shell"
   prompt = '(s3) '

   def __init__(self):
      cmd.Cmd.__init__(self)

#
#  S3 Commands
#
   def do_list(self, line):
      'List all buckets'
      call("aws s3api list-buckets")

   def do_create(self, line):
      'Create an S3 bucket by name'
      bucket = line.split()[0]
      call("aws s3api create-bucket --acl private --bucket %s" % (bucket))

   def do_delete(self, line):
      'Delete an S3 bucket by name'
      bucket = line.split()[0]
      call("aws s3api delete-bucket --bucket %s" % (bucket))

   def do_ls(self, line):
      'List contents of bucket'
      bucket = adds3(line.split()[0])
      call("aws s3 ls %s" % (bucket))

   def do_rm(self, line):
      'Remove file from bucket'
      file = adds3(line.split()[0])
      call("aws s3 rm %s" % (file))

   def do_cp(self, line):
      'Copy file from bucket'
      src = line.split()[0]
      dst = line.split()[1]
      call("aws s3 cp %s %s" % (src, dst))


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

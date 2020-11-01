#!/usr/local/bin/python3

import cmd, os, configparser
from awscommands import awscommands

class AWSShell(cmd.Cmd):
    intro = "AWS EC2 Shell"
    prompt = '(ec2) '
    aws = awscommands()

    def __init__(self):
        cmd.Cmd.__init__(self)

#
# CMD behavior customization
#
    def do_EOF(self, unused):
        print()
        return True

#
#
#
    def do_get_cost(self, unused):
        'return the cost for a period (WIP)'
        command = "aws ce get-cost-and-usage --time-period=Start='2020-10-01',End='2020-10-31' --metrics=AmortizedCost"
        res = self.aws.aws_cmd(command)
        print(res)



    def emptyline(self):
        print(self.prompt)

if __name__ == '__main__':
   #AWSShell().do_inst_type_desc("t1.micro")
   AWSShell().cmdloop()

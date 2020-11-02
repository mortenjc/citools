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
# Security group
#

    def do_sg_list(self, unused):
        'list all security groups'
        self.aws.security_group_list()

    def do_sg_create(self, groupname):
        'create a security group'
        self.aws.security_group_create(groupname)

    def do_sg_delete(self, groupname):
        'delete a security group'
        self.aws.security_group_delete(groupname)

    # def do_show_four_core_instances(self, unused):
    #     'query instances with 4 cores - to be parametrised'
    #     mycmd = "aws ec2 describe-instance-types --output json --query 'InstanceTypes[?VCpuInfo.DefaultCores==`4`].{Instance:InstanceType,Threads:VCpuInfo.DefaultVCpus}'"
    #     output = os.popen(mycmd).read()
    #     print(output)

    def do_show_available_instance_types(self, unused):
        'list all available ec2 instance types'
        self.aws.show_available_instance_types()

    def do_describe_instance_type(self, type):
        'describe an instance type'
        self.aws.describe_instance_type(type)

#
# Key pairs
#
    def do_key_pair_list(self, unused):
        'describe (list) all key pairs'
        self.aws.keypair_describe()

    def do_key_pair_create(self, newkp):
        'create a key pair'
        self.aws.keypair_create(newkp)

    def do_key_pair_delete(self, kp):
        'delete a key pair'
        self.aws.keypair_delete(kp)

#
# Show, start, stop and delete instances
#
    def do_show_our_instances(self, unused):
        'list all ec2 our instances'
        self.aws.show_our_instances()

    def do_run_instance(self, type):
        'run an instance of image: ami-0dba2cb6798deb6d8'
        self.aws.run_instance(type)

    def do_stop_instance(self, instid):
        'stop an instance'
        self.aws.stop_instance(instid)

    def do_terminate_instance(self, instid):
        'terminate an instance'
        self.aws.terminate_instance(instid)

    def do_terminate_all(self, unused):
        'terminate all instances'
        self.aws.terminate_all()

    def do_subnet_show(self, unused):
        'show available subnets'
        self.aws.subnet_show()

#
# Images
#
    def do_show_our_images(self, unused):
        'list images I own'
        self.aws.images_show_our()

    def do_image_create(self, line):
        'create image from instanceid and (optional) name'
        self.aws.image_create(line)

#
# Other commands
#
    def do_whoami(self, unused):
        'show account and user information'
        self.aws.whoami()

    def do_ssh(self, ipaddr):
        'show ssh command to use for login'
        dir = os.path.join(self.aws.cfg.options['key_dir'], self.aws.cfg.options['key_pair'])
        print("ssh -i {}.pem ubuntu@{}"\
           .format(dir, ipaddr))


    def emptyline(self):
        print(self.prompt)

if __name__ == '__main__':
   #AWSShell().do_inst_type_desc("t1.micro")
   AWSShell().cmdloop()

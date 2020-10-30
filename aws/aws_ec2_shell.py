#!/usr/local/bin/python3

import cmd, os, sys, json
import subprocess as sp

class AWSShell(cmd.Cmd):
    intro = "AWS  Shell"
    prompt = '(awsshell) '

    def __init__(self):
        cmd.Cmd.__init__(self)

#
# Helper functions
#
    def print_subnet(self, js):
        for i in range(len(js['Subnets'])):
            id = js['Subnets'][i]['SubnetId']
            ip = js['Subnets'][i]['CidrBlock']
            print("{0:20} {1:20}".format(id, ip))

    def print_instance_type(self, js):
        type = js['InstanceTypes'][0]['InstanceType']
        threads = js['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
        memsize = js['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
        nwperf = js['InstanceTypes'][0]['NetworkInfo']['NetworkPerformance']
        print("Type: {}".format(type))
        print("Cpuinfo: {}".format(threads))
        print("Memory: {} MB".format(memsize))
        print("Network performance: {}".format(nwperf))

    def print_instances(self, instances):
        js = json.loads(instances)


    # do the aws command and return valid json or empty string
    def aws_cmd(self, command):
        #print(command)
        popenarg = command.split()
        #print(popenarg)
        p = sp.Popen(popenarg, stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = p.communicate()
        #print("out: {}".format(out))
        #print("err: {}".format(err))
        if len(err) > 0:
            print('aws command failed: {}'.format(popenarg[2]))
            return ''
        if len(out) > 0:
            return json.loads(out)
        return ''

#
# CMD behavior customization
#
    def do_EOF(self, unused):
        print()
        return True


    def do_sg_list(self, unused):
        'list all security groups'
        fmt="{0:25} {1:20} {2:60}"
        res = self.aws_cmd("aws ec2 describe-security-groups")
        if (res != ''):
            print(fmt.format('GroupId', 'GroupName', 'Description'))
            for i in range(len(res['SecurityGroups'])):
                id = res['SecurityGroups'][i]['GroupId']
                name = res['SecurityGroups'][i]['GroupName']
                desc = res['SecurityGroups'][i]['Description']
                print(fmt.format(id, name, desc))


    def do_sg_create(self, groupname):
        'create a security group'
        parms = "--description 'testgroup_created_by_ecdc_script' --group-name " + groupname
        command = "aws ec2 create-security-group " + parms
        js = self.aws_cmd(command)
        if (js != ''):
            group = js['GroupId']
            print("new group id: {}".format(group))


    def do_sg_delete(self, groupname):
        'delete a security group'
        command = "aws ec2 delete-security-group --group-name " + groupname
        res = self.aws_cmd(command)


    # def do_show_four_core_instances(self, unused):
    #     'query instances with 4 cores - to be parametrised'
    #     mycmd = "aws ec2 describe-instance-types --output json --query 'InstanceTypes[?VCpuInfo.DefaultCores==`4`].{Instance:InstanceType,Threads:VCpuInfo.DefaultVCpus}'"
    #     output = os.popen(mycmd).read()
    #     print(output)


    def do_show_available_instance_types(self, unused):
        'list all available ec2 instance types'
        query = "--query \'InstanceTypes[*].{Instance:InstanceType,Cores:VCpuInfo.DefaultCores,Threads:VCpuInfo.DefaultVCpus}\'"
        mycmd = "aws ec2 describe-instance-types --output json " + query
        # doesn't work with aws_cmd()
        js = json.loads(os.popen(mycmd).read())
        for entry in js:
            if entry['Cores'] == None:
                entry['Cores'] = '-'
            print("{0:20} {1:3} {2:3}".format(entry['Instance'], entry['Cores'], entry['Threads']))


    def do_describe_instance_type(self, type):
        'describe an instance type'
        mycmd = "aws ec2 describe-instance-types --output json --instance-types=" + type
        res = self.aws_cmd(mycmd)
        self.print_instance_type(res)


#
# Show, start, stop and delete instances
#
    def do_show_our_instances(self, unused):
        'list all ec2 our instances'
        fmt = "{0:20} {1:16} {2:16} {3:15} {4:25} {5:30} {6:15}"
        query="--query \'Reservations[*].Instances[*].{" + \
          "Id:InstanceId,Ip:PublicIpAddress,Key:KeyName,Type:InstanceType," + \
          "Image:ImageId,Time:LaunchTime,State:State.Name}\'"
        mycmd = "aws ec2 describe-instances --output json " + query
        # For some reason doesn't work wirh aws_cmd()
        js = json.loads(os.popen(mycmd).read())
        print(fmt.format("Instance Id", "Ip Address", "Key", "Instance Type", "Image Id", "Launch time", "State"))
        for entries in js:
            for e in entries:
                if (e['Key'] is None):
                    e['Key'] = 'None'
                if (e['Ip'] is None):
                    e['Ip'] = 'None'
                print(fmt.format(e['Id'], e['Ip'], e['Key'], e['Type'], e['Image'], e['Time'], e['State']))


    def do_run_instance(self, type):
        'run an instance of image: ami-0dba2cb6798deb6d8'
        if type=='':
            type = 't1.micro'
        command = "aws ec2 run-instances --key-name=kp_mjc_work --image-id=ami-0dba2cb6798deb6d8 --instance-type=" + type
        js = self.aws_cmd(command)



    def do_stop_instance(self, instid):
        'stop an instance'
        command = "aws ec2 stop-instances --instance-id=" + instid
        js = self.aws_cmd(command)
        pst = js['StoppingInstances'][0]['PreviousState']['Name']
        nst = js['StoppingInstances'][0]['CurrentState']['Name']
        print("{}: state: {} -> {}".format(instid, pst, nst))


    def do_terminate_instance(self, instid):
        'terminate an instance'
        command = "aws ec2 terminate-instances --instance-id=" + instid
        js = self.aws_cmd(command)
        if (js != ''):
            pst = js['TerminatingInstances'][0]['PreviousState']['Name']
            nst = js['TerminatingInstances'][0]['CurrentState']['Name']
            print("{}: state: {} -> {}".format(instid, pst, nst))


    def do_terminate_all(self, unused):
        query = "\'Reservations[*].Instances[*].{Id:InstanceId}\'"
        command = "aws ec2 describe-instances --output json --query " + query
        js = self.aws_cmd(command)
        for entries in js:
            for entry in entries:
                self.do_terminate_instance(entry['Id'])


    def do_subnet_show(self, unused):
        'show available subnets'
        res = self.aws_cmd('aws ec2 describe-subnets')
        self.print_subnet(res)


    # def do_ssh(self, line):
    #     'launch terminal and ssh into instance'
    #     return


    def emptyline(self):
        print(self.prompt)

if __name__ == '__main__':
   #AWSShell().do_inst_type_desc("t1.micro")
   AWSShell().cmdloop()

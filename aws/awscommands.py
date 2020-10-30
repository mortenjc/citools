#!/usr/local/bin/python3

import json, os
import subprocess as sp

class awscommands():

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
# Command implementations
#

# Security group commands
    def security_group_list(self):
        fmt="{0:25} {1:20} {2:60}"
        res = self.aws_cmd("aws ec2 describe-security-groups")
        if (res != ''):
            print(fmt.format('GroupId', 'GroupName', 'Description'))
            for i in range(len(res['SecurityGroups'])):
                id = res['SecurityGroups'][i]['GroupId']
                name = res['SecurityGroups'][i]['GroupName']
                desc = res['SecurityGroups'][i]['Description']
                print(fmt.format(id, name, desc))


    def security_group_create(self, groupname):
        parms = "--description 'testgroup_created_by_ecdc_script' --group-name " + groupname
        command = "aws ec2 create-security-group " + parms
        js = self.aws_cmd(command)
        if (js != ''):
            group = js['GroupId']
            print("new group id: {}".format(group))


    def security_group_delete(self, groupname):
        command = "aws ec2 delete-security-group --group-name " + groupname
        res = self.aws_cmd(command)


# Instance commands
    def show_available_instance_types(self):
        query = "--query \'InstanceTypes[*].{Instance:InstanceType,Cores:VCpuInfo.DefaultCores,Threads:VCpuInfo.DefaultVCpus}\'"
        mycmd = "aws ec2 describe-instance-types --output json " + query
        # doesn't work with aws_cmd()
        js = json.loads(os.popen(mycmd).read())
        for entry in js:
            if entry['Cores'] == None:
                entry['Cores'] = '-'
            print("{0:20} {1:3} {2:3}".format(entry['Instance'], entry['Cores'], entry['Threads']))


    def describe_instance_type(self, type):
        mycmd = "aws ec2 describe-instance-types --output json --instance-types=" + type
        res = self.aws_cmd(mycmd)
        self.print_instance_type(res)


    def show_our_instances(self):
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


    def run_instance(self, type):
        if type=='':
            type = 't1.micro'
        command = "aws ec2 run-instances --key-name=kp_mjc_work --image-id=ami-0dba2cb6798deb6d8 --instance-type=" + type
        js = self.aws_cmd(command)


    def stop_instance(self, instid):
        command = "aws ec2 stop-instances --instance-id=" + instid
        js = self.aws_cmd(command)
        pst = js['StoppingInstances'][0]['PreviousState']['Name']
        nst = js['StoppingInstances'][0]['CurrentState']['Name']
        print("{}: state: {} -> {}".format(instid, pst, nst))


    def terminate_instance(self, instid):
        command = "aws ec2 terminate-instances --instance-id=" + instid
        js = self.aws_cmd(command)
        if (js != ''):
            pst = js['TerminatingInstances'][0]['PreviousState']['Name']
            nst = js['TerminatingInstances'][0]['CurrentState']['Name']
            print("{}: state: {} -> {}".format(instid, pst, nst))


    def terminate_all(self):
        query = "\'Reservations[*].Instances[*].{Id:InstanceId}\'"
        command = "aws ec2 describe-instances --output json --query " + query
        # grr should work with aws_cmd
        js = json.loads(os.popen(command).read())
        for entries in js:
            for entry in entries:
                print(entry)
                self.terminate_instance(entry['Id'])


    def subnet_show(self):
        res = self.aws_cmd('aws ec2 describe-subnets')
        self.print_subnet(res)


if __name__ == '__main__':
    awscommands().show_our_instances()
    awscommands().security_group_list()
    awscommands().subnet_show()
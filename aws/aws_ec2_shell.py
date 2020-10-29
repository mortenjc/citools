#!/usr/local/bin/python3

import cmd, os, json

class AWSShell(cmd.Cmd):
    intro = "AWS  Shell"
    prompt = '(awsshell) '

    def __init__(self):
        cmd.Cmd.__init__(self)

#
# Helper functions
#
    def print_subnet(self, res):
        js = json.loads(res)
        for i in range(len(js['Subnets'])):
            id = js['Subnets'][i]['SubnetId']
            ip = js['Subnets'][i]['CidrBlock']
            print("{0:20} {1:20}".format(id, ip))

    def print_instance_type(self, insttype):
        js = json.loads(insttype)
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

#
# CMD behavior customization
#
    def do_EOF(self, line):
        print()
        return True


    def do_sg_list(self, line):
        'list all security groups'
        output = os.popen("aws ec2 describe-security-groups").read()
        print(output)


    def do_sg_create(self, line):
        'create a security group'
        parms = "--description 'security group created by awsshell' --group-name "
        command = "aws ec2 create-security-group "
        output = os.popen(command + parms + line).read()
        print(output)


    def do_sg_delete(self, line):
        'delete a security group'
        parms = "--group-name "
        command = "aws ec2 delete-security-group "
        output = os.popen(command + parms + line).read()
        print(output)


    def do_show_four_core_instances(self, line):
        'query instances with 4 cores - to be parametrised'
        mycmd = "aws ec2 describe-instance-types --output json --query 'InstanceTypes[?VCpuInfo.DefaultCores==`4`].{Instance:InstanceType,Threads:VCpuInfo.DefaultVCpus}'"
        output = os.popen(mycmd).read()
        print(output)


    def do_show_available_instance_types(self, line):
        'list all available ec2 instance types'
        mycmd = "aws ec2 describe-instance-types --output json --query 'InstanceTypes[*].{Instance:InstanceType,Cores:VCpuInfo.DefaultCores,Threads:VCpuInfo.DefaultVCpus}'"
        js = json.loads(os.popen(mycmd).read())
        for entry in js:
            print("{}, {}, {}".format(entry['Instance'], entry['Cores'], entry['Threads']))


    def do_describe_instance_type(self, line):
        'describe an instance type'
        mycmd = "aws ec2 describe-instance-types --output json --instance-types "
        output = os.popen(mycmd + line).read()
        #print(output)
        self.print_instance_type(output)


#
# Show, start, stop and delete instances
#
    def do_show_our_instances(self, line):
        'list all ec2 our instances'
        query="\'Reservations[*].Instances[*].{Id:InstanceId,Ip:PublicIpAddress,Key:KeyName,Type:InstanceType,Image:ImageId,Time:LaunchTime,State:State.Name}\'"
        mycmd = "aws ec2 describe-instances --output json --query " + query
        js = json.loads(os.popen(mycmd).read())
        fmt = "{0:20} {1:16} {2:16} {3:15} {4:25} {5:30} {6:15}"
        print(fmt.format("Instance Id", "Ip Address", "Key", "Instance Type", "Image Id", "Launch time", "State"))
        for entries in js:
            for entry in entries:
                if (entry['Key'] is None):
                    entry['Key'] = 'None'
                print(fmt.format(entry['Id'], entry['Ip'], entry['Key'], entry['Type'], entry['Image'], entry['Time'], entry['State']))


    def do_run_instance(self, line):
        'run an instance of image: ami-0dba2cb6798deb6d8'
        if line=='':
            line = 't1.micro'
        mycmd = "aws ec2 run-instances --key-name=kp_mjc_work --image-id=ami-0dba2cb6798deb6d8 --instance-type="
        js = json.loads(os.popen(mycmd + line).read())
        instid = js['Instances'][0]['InstanceId']
        print("new instance id: {}".format(instid))


    def do_stop_instance(self, line):
        'stop an instance'
        mycmd = "aws ec2 stop-instances --instance-id="
        js = json.loads(os.popen(mycmd + line).read())
        pst = js['StoppingInstances'][0]['PreviousState']['Name']
        nst = js['StoppingInstances'][0]['CurrentState']['Name']
        print("{}: state: {} -> {}".format(line, pst, nst))


    def do_terminate_instance(self, line):
        'terminate an instance'
        mycmd = "aws ec2 terminate-instances --instance-id="
        js = json.loads(os.popen(mycmd + line).read())
        pst = js['TerminatingInstances'][0]['PreviousState']['Name']
        nst = js['TerminatingInstances'][0]['CurrentState']['Name']
        print("{}: state: {} -> {}".format(line, pst, nst))


    def do_terminate_all(self, line):
        mycmd = "aws ec2 describe-instances --output json --query 'Reservations[*].Instances[*].{Id:InstanceId,Type:InstanceType,Image:ImageId,Time:LaunchTime,State:State.Name}'"
        js = json.loads(os.popen(mycmd).read())
        for entries in js:
            for entry in entries:
                self.do_terminate_instance(entry['Id'])


    def do_subnet_show(self, line):
        'show available subnets'
        mycmd = 'aws ec2 describe-subnets'
        res = os.popen(mycmd).read()
        self.print_subnet(res)


    def do_ssh(self, line):
        'launch terminal and ssh into instance'
        return


    def emptyline(self):
        print(self.prompt)

if __name__ == '__main__':
   #AWSShell().do_inst_type_desc("t1.micro")
   AWSShell().cmdloop()

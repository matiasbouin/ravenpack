# Pseudo-Code for AWS CDK in Python to create a NAT instance with Auto Scaling

from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2

# 1. Create a VPC with Public and Private subnets in 2 AZs
vpc = ec2.Vpc(self, "NATVpc",
              max_azs=2,
              nat_gateways=0, # We are building our own
              subnet_configuration=[...])

# 2. Create a Launch Template for the NAT instance
launch_template = ec2.LaunchTemplate(self, "NATLaunchTemplate",
    instance_type=ec2.InstanceType("t3.micro"),
    machine_image=ec2.MachineImage.latest_amazon_linux(),
    user_data=ec2.UserData.custom("#!/bin/bash\n/sbin/sysctl -w net.ipv4.ip_forward=1\n/sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n"),
    security_group=nat_security_group
)

# 3. Create an Auto Scaling Group
asg = autoscaling.AutoScalingGroup(self, "NATAutoScalingGroup",
    vpc=vpc,
    launch_template=launch_template,
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
    min_capacity=1,
    max_capacity=4,
    desired_capacity=2, # One per AZ
    health_check=autoscaling.HealthCheck.ec2()
)
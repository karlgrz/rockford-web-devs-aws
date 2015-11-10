#!/usr/bin/python

import boto.ec2.autoscale
import argparse
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup

def main():
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument('-c','--capacity', help='Capacity to increase autoscaling group to', required=False)
	parser.add_argument('-a','--action', help='create or capacity', required=True)
	args = vars(parser.parse_args())

	if args['action'] == 'create':
	    create()
	elif args['action'] == 'capacity':
		change_capacity(args['capacity'])

def change_capacity(capacity):
	conn = boto.ec2.autoscale.connect_to_region('us-east-1')

	groups = conn.get_all_groups()

	my_group = [group for group in groups if group.name == 'karlgrz-karlgrzcluster01-autoscaling-group'][0]

	conn.set_desired_capacity(my_group.name, capacity)

def create():
	conn = boto.ec2.autoscale.connect_to_region('us-east-1')

	groups = conn.get_all_groups()

	my_group = [group for group in groups if group.name == 'karlgrz-karlgrzcluster01-autoscaling-group']

	print 'creating launch configuration and autoscaling group'
	lc = LaunchConfiguration(name='karlgrz-karlgrzcluster01-launch-configuration',
						 image_id='ami-d50d74bf',
                         key_name='karlgrz-karlgrzcluster01',
                         instance_profile_name='karlgrz-services',
                         instance_type='t1.micro',
                         block_device_mappings=['/dev/sda1'],
                         user_data='#!/bin/bash\ndocker run --name json-service -p 8888:8888 karlgrz/karlgrz-dummy-json-service',
                         security_groups=['karlgrzcluster01-us-east-1b-host01','karlgrzcluster01-us-east-1d-host01','karlgrzcluster01','karlgrz'])
	conn.create_launch_configuration(lc)

	ag = AutoScalingGroup(group_name='karlgrz-karlgrzcluster01-autoscaling-group', load_balancers=['karlgrz-karlgrzcluster01'],
                          availability_zones=['us-east-1b', 'us-east-1d'],
                          vpc_zone_identifier=['subnet-320e3419','subnet-9fd7dcc6'],
                          launch_config=lc, min_size=0, max_size=5,
                          health_check_type='ELB',
                          health_check_period=300,
                          connection=conn)
	conn.create_auto_scaling_group(ag)

if __name__ == '__main__':
	main()
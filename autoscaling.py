#!/usr/bin/python

import boto.ec2.autoscale
import sys

def main(argv):
	desired_capacity = argv[1]
	print 'desired_capacity = {}'.format(desired_capacity)

	ec2 = boto.ec2.autoscale.connect_to_region('us-east-1')

	groups = ec2.get_all_groups()

	my_group = [group for group in groups if group.name == 'karlgrz-karlgrzcluster01-autoscaling-group'][0]
	ec2.set_desired_capacity(my_group.name, desired_capacity)
	print my_group
	print my_group.name

if __name__ == '__main__':
	main(sys.argv)
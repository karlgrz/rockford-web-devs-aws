#!/usr/bin/python

import boto

ec2 = boto.connect_ec2()

instances = ec2.get_all_instances()

print 'instances:{}'.format(instances)
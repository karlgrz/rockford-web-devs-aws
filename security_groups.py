#!/usr/bin/python

import boto

desired_groups = set([
	'karlgrzcluster01-us-east-1b-host01',
	'karlgrzcluster01-us-east-1d-host01',
	'karlgrzcluster01',
	'karlgrz'
])

ec2 = boto.connect_ec2()

existing_groups = [group.name for group in ec2.get_all_security_groups()]
print 'groups before:{}'.format(existing_groups)

missing_groups = [x for x in desired_groups if x not in existing_groups ]
for group in missing_groups:
	sg = ec2.create_security_group(group, group)
	if group == 'karlgrz':
		sg.authorize('tcp', 22, 22, '0.0.0.0/0')
		sg.authorize('tcp', 80, 80, '0.0.0.0/0')
		sg.authorize('tcp', 8888, 8888, '0.0.0.0/0')

groups = ec2.get_all_security_groups()
print 'groups after:{}'.format(groups)
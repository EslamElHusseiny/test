#!/usr/bin/env python

import boto, boto.cloudformation, yaml, os 

def get_cfn_conn(region):
	try : 
		cfn_conn = boto.cloudformation.connect_to_region(region_name=region)
	except boto.exception.NoAuthHandlerFound as e:
		print e
	return cfn_conn

def get_template_body(template):
	with open(template, "r") as stack_file:
	    template_body = stack_file.read()
	    return template_body


def parse_answers(answers_file):
	ret={}
	with open(answers_file, "r") as answers: 
	    yans = yaml.load(answers)
	    ret['stack_name'] = yans.keys()[0] 
	    ret['template'] = yans[ret['stack_name']]['template']
	    ret['aws_region'] = yans[ret['stack_name']]['region']
	    ret['parameters'] = list(yans[ret['stack_name']]['parameters'].viewitems())
	    return ret


if __name__ == '__main__':
	answers = parse_answers('answers.yml')
	cfn_conn = get_cfn_conn(answers['aws_region'])
	cfn_conn.create_stack(stack_name=answers['stack_name'], template_body=get_template_body(answers['template']), parameters=answers['parameters'])

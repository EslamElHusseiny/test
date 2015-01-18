#!/usr/bin/env python

import boto, boto.cloudformation, yaml, time

def get_cfn_conn(region):
	try : 
		cfn_conn = boto.cloudformation.connect_to_region(region_name=region)
	except boto.exception.NoAuthHandlerFound as e:
		print e
	return cfn_conn

def get_template_body(template):
	try:
		with open(template, "r") as stack_file:
			template_body = stack_file.read()
			return template_body
	except Exception, e:
		print str(e)
		exit(1)

def parse_answers(answers_file):
	ret={}
	try :
		with open(answers_file, "r") as answers:
			yans = yaml.load(answers)	
			ret['stack_name'] = yans.keys()[0] 
			ret['template'] = yans[ret['stack_name']]['template']
			ret['aws_region'] = yans[ret['stack_name']]['region']
			ret['parameters'] = list(yans[ret['stack_name']]['parameters'].viewitems())
			return ret		
	except Exception as e : 
		print str(e)
		exit(1)

def get_stack_outputs(cfn_conn, stack_name):
	stack = cfn_conn.describe_stacks(stack_name)[0]
	for outputs in stack.outputs:
		print('%s ==> %s   /*%s*/' %(outputs.key, outputs.value, outputs.description))

def log_stack_events(cfn_conn, stack_name):
	create_complete = 'StackEvent AWS::CloudFormation::Stack '+stack_name+' CREATE_COMPLETE'
	rollback_complete = 'StackEvent AWS::CloudFormation::Stack '+stack_name+' ROLLBACK_COMPLETE'
	event = str(cfn_conn.describe_stack_events(stack_name)[0])
	while event != create_complete and event != rollback_complete: 
		if str(cfn_conn.describe_stack_events(stack_name)[0]) != event:
			event = str(cfn_conn.describe_stack_events(stack_name)[0])
			print event
		else:
			time.sleep(2) #TODO: needs refactoring see => https://forums.aws.amazon.com/thread.jspa?messageID=366822

if __name__ == '__main__':
	answers = parse_answers('answers.yml')
	cfn_conn = get_cfn_conn(answers['aws_region'])
	try:
		cfn_conn.create_stack(stack_name=answers['stack_name'], template_body=get_template_body(answers['template']), parameters=answers['parameters'])
	except Exception, e:
		print str(e)
		exit(1)
	log_stack_events(cfn_conn, answers['stack_name'])
	get_stack_outputs(cfn_conn, answers['stack_name'])
	





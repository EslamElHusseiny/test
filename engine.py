#!/usr/bin/env python

import boto, boto.cloudformation, yaml, time, logging, sys, prettytable

def get_cfn_conn(region):
	logger = create_stdout_logger()
	try : 
		cfn_conn = boto.cloudformation.connect_to_region(region_name=region)
	except boto.exception.NoAuthHandlerFound as e:
		print e
	if type(cfn_conn) != boto.cloudformation.connection.CloudFormationConnection :
		logger.info("Seems like \""+region+"\" isn't a valid aws region")
		logger.info("kindly check http://docs.aws.amazon.com/general/latest/gr/rande.html")
		exit(1)
	return cfn_conn

def get_template_body(template):
	try:
		with open(template, "r") as stack_file:
			template_body = stack_file.read()
			return template_body
	except Exception, e:
		print str(e)
		exit(1)

def validate_template(cfn_conn, template_body):
	logger = create_stdout_logger()
	try:
		cfn_conn.validate_template(template_body=template_body)
	except boto.exception.BotoServerError, e:
		logger.info(e)

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
	table = prettytable.PrettyTable(['key','value','description'])
	for output in stack.outputs:
		table.add_row([output.key, output.value, output.description])
	print table

def create_stdout_logger():
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	stdout = logging.StreamHandler(sys.stdout)
	stdout.setLevel(logging.INFO)
	logger.addHandler(stdout)
	return logger


def log_stack_events(cfn_conn, stack_name):
	create_complete = 'StackEvent AWS::CloudFormation::Stack '+stack_name+' CREATE_COMPLETE'
	rollback_complete = 'StackEvent AWS::CloudFormation::Stack '+stack_name+' ROLLBACK_COMPLETE'
	events = ['']
	logger = create_stdout_logger()
	while str(events[0]) != create_complete and str(events[0]) != rollback_complete: 
		new_events = cfn_conn.describe_stack_events(stack_name)
		if len(new_events) > len(events):
			for i in range(len(new_events)-len(events),0,-1):
				logger.info(new_events[i])
			events = new_events
		else:
			time.sleep(2) #TODO: needs refactoring see => https://forums.aws.amazon.com/thread.jspa?messageID=366822
	logger.info(events[0])

if __name__ == '__main__':
	answers = parse_answers('answers.yml')
	cfn_conn = get_cfn_conn(answers['aws_region'])
	validate_template(cfn_conn,get_template_body(answers['template']))
	try:
		cfn_conn.create_stack(stack_name=answers['stack_name'], template_body=get_template_body(answers['template']), parameters=answers['parameters'])
	except Exception, e:
		print str(e)
		exit(1)
	log_stack_events(cfn_conn, answers['stack_name'])
	get_stack_outputs(cfn_conn, answers['stack_name'])

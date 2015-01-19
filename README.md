# Test
Just another test Repository!

This repo includes :
* Dockerfile 
* CloudFormation template 
* Yaml file includes values of parameters of CloudFormation template
* Python script : parses Yaml file and launch AWS stack descriped in CloudFormation template

## How to start 
### Build docker image 
```
sudo docker build -t myimage:latest .
```

### Run docker container
```
sudo docker run --rm -e "AWS-ACCESS-KEY-ID=<Your aws access key>"  -e "AWS-SECRET-ACCESS-KEY=<Your aws secret key>" myimage
```
Happy path output should be as following : 
```
StackEvent AWS::CloudFormation::Stack <stack_name> CREATE_IN_PROGRESS
StackEvent AWS::EC2::SecurityGroup InstanceSecurityGroup CREATE_IN_PROGRESS
StackEvent AWS::EC2::EIP IPAddress CREATE_IN_PROGRESS
StackEvent AWS::EC2::EIP IPAddress CREATE_IN_PROGRESS
StackEvent AWS::EC2::SecurityGroup InstanceSecurityGroup CREATE_IN_PROGRESS
StackEvent AWS::EC2::EIP IPAddress CREATE_COMPLETE
StackEvent AWS::EC2::SecurityGroup InstanceSecurityGroup CREATE_COMPLETE
StackEvent AWS::EC2::Instance EC2Instance CREATE_IN_PROGRESS
StackEvent AWS::EC2::Instance EC2Instance CREATE_IN_PROGRESS
StackEvent AWS::EC2::Instance EC2Instance CREATE_COMPLETE
StackEvent AWS::EC2::EIPAssociation IPAssoc CREATE_IN_PROGRESS
StackEvent AWS::EC2::EIPAssociation IPAssoc CREATE_IN_PROGRESS
StackEvent AWS::EC2::EIPAssociation IPAssoc CREATE_COMPLETE
StackEvent AWS::CloudFormation::Stack <stack_name> CREATE_COMPLETE
+-------------------+--------------+----------------------------------------------+
|        key        |    value     |                 description                  |
+-------------------+--------------+----------------------------------------------+
|     InstanceId    |  i-xxxxxxxx  | InstanceId of the newly created EC2 instance |
| InstanceIPAddress | xx.xx.xx.xxx | IP address of the newly created EC2 instance |
+-------------------+--------------+----------------------------------------------+
```
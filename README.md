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


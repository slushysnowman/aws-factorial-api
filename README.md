# aws-factorial-api

## Introduction
This project deploys a very (very) simple API to Fargate, presented via an Application Load Balancer.

When a number parameter is passed to the address via a GET, the factorial of the number is returned.

## Choices/Context

Rough sketch of architecture can be seen below

![architecture](architecture/images/aws-factorial-api.drawio.png)

### Infrastructure-as-code - Python CDK
* Python CDK was chosen to be used to provision AWS infrastructure
* For this scenario I chose to go the really easy route and use an ECS pattern as it provided everything needed for this use case.
* I've also chosen to allow the CDK to take care of the build process for the docker image

Now I have to say, in a 'production' scenario I probably wouldn't allow CDK to handle the docker build - I would separate the build of the container from the deployment. This allows the container to be tested before deployment. Normally for the container I would do something like:
* Lint Dockerfile
* Build image with a `:dev` tag or `:{git-commit-id}-rc`
* Scan image using a tool like Trivy
* 'Promote' image by retagging to `:latest` and `:{git-commit-id}`
* Push image to registry
* Use image in run, promoting across different environments

In a normal scenario I probably also wouldn't use an ecs_pattern as I prefer finer control over all the infrastructure, and I've had problems with them in the past. The main reason I actually ended up using it was because I hadn't used the ecs_patterns in a long while and wanted to see if they had improved (they have). So thanks for giving me an opportunity to refresh my knowledge :D.

### Application Load Balancer
* Load balancer was a requirement for this assignment.
* Normally for this use case I would have used an API gateway as it ends up cheaper since this is a no/low volume application, but that wasn't specified
* Using a load balancer per service is normally super inefficient - If I was setting up multiple applications making use of load balancers I'd probably setup a central one and use that for them all
* Load balancer is configured with 2 listeners
* * HTTP - redirects to HTTPS
* * HTTPS - forwards traffic to the API container

### ECS Fargate
* Fargate was chosen as it is a very simple setup, with no complexity to maintain - perfect for this simple application
* If I'd had free rein to choose the compute for this assignment, I probably would have used Lambda instead, in combination with API gateway, to remove the container layer from the stack - I'm not against containers, but something this simple could easily be a Lambda
* Desired count for the service is set to 2 - this has primarily been done to demonstate that I know how to do this. I deliberately haven't chose to go too far into scaling as it seems like overkill in this case

### DNS entry in Route53
* Consistent endpoint rather than using the loadbalancer address
* Ability to use an ACM certificate for TLS termination on the load balancer

### ACM certificate for HTTPS listener
* Obvious choice for certificate. Traffic after the loadbalancer, to the container is unencrypted. This is deemed acceptable given the nature of this API, and the fac that that traffic is inside the VPC account already.

### Dockerfile (./container/Dockerfile)
* (Google distroless image)[https://github.com/GoogleContainerTools/distroless] is used as a base for the API container as these images are very secure and lightweight - these are very minimal images
* Multi-stage build is used to reduce eventual image size

### Factorial API (./container/app/app.py)
* Written in Python leveraging Flask
* * Honestly - first time using Flask as generally for APIs I use Lambda - so my usage isn't very advanced, but it was nice to have an excuse to experiment with Flask
* The internals of how this works are very simple. Now, there are many routes I could have gone down to return the factorial of the integer provided - recursion/iteration etc. But honestly, it makes no sense to do this when there is a default library available which does exactly that. So in the end I opted to use `math.factorial` to determine the factorial.

Basic unit tests are in place to test the functionality.

### CI/CD & pre-commit hooks
CI/CD has not been setup due to lack of time.

However, pre-commit hooks do some basic checks on all commits. Documentation for this can be found here: https://pre-commit.com/
Pre-commit configuration can be found in `.pre-commit-config.yaml` - here you can see which pre-commit hooks are enabled

### Alerts
Not defined due to

## Prerequisites
### Setting up AWS account
* Create user with sufficient privileges for deployment
* CDK bootstrap `cdk bootstrap`

## Local development
### Prerequisites
* AWS CDK installed
* Python 3.6+ installed
* Python venv installed
* Docker installed (we're using a construct for Lambda which requires this locally)
* AWS credentials configured

### Python venv setup
* Be in root folder of this repo
* `python3 -m venv .venv`
* `source .venv/bin/activate`
* `pip3 install -r requirements.txt`
* You're now running in your local dev environment

### Pre-commit hooks
Pre-commmit hooks are used to ensure quality of committed code. Documentation for this can be found here: https://pre-commit.com/
Pre-commit configuration can be found in `.pre-commit-config.yaml` - here you can see which pre-commit hooks are enabled

This can also be run manually to check all files from within the venv: `pre-commit run --all-files`

### Run unit tests
```
./run-unit-tests.sh
```

### Deploying from local
* NOTE - `cdk bootstrap` needs to have been run first for this to work
* Run `cdk synth` to check that cdk setup is valid
* Run `cdk deploy` to deploy using the AWS credentials you have configured.
** If using a profile then do `cdk deploy --profile {profile_name}`

### Building docker image locally
```
cd container
docker build -t factorial-api:dev
```

### Running docker image locally
```
docker run factorial-api:dev
```
You can then head to http://172.17.0.2:5000/api/v1/factorial?number=2

## API in AWS
Available at https://factorial.to-assignment.net/api/v1/factorial?number=50

Can be tested for various numbers by changing the number parameter

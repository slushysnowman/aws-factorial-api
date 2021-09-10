#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from aws_factorial_api.aws_factorial_api_stack import AwsFactorialApiStack


app = cdk.App()
AwsFactorialApiStack(app, "AwsFactorialApiStack")

app.synth()

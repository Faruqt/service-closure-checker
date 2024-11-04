#!/usr/bin/env python3

"""
app.py: This file contains the code to define the CDK app.
"""
# library imports
import os
import aws_cdk as cdk

# local imports
from infrastructure.infrastructure_stack import InfrastructureStack

app = cdk.App()
InfrastructureStack(
    app,
    "InfrastructureStack",
    # Specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()

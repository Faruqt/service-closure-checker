"""
lambda_stack.py : This file contains the code to create a Lambda function using the AWS CDK.
"""

# library imports
import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct

# get the current directory
CURRENT_DIR = os.path.dirname(__file__)


class LambdaStack(Stack):
    """
    LambdaStack: This class creates a Lambda function using the AWS CDK.

    Args:
        Stack (aws_cdk.core.Stack): The base class for Stack
        Construct (aws_cdk.core.Construct): The base class for Construct

    Returns:
        None
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function_name = os.getenv("SERVICE_STATUS_LAMBDA_FUNCTION_NAME")

        # Define environment variables for the Lambda function
        environment_variables = {
            "SERVICES_TABLE_NAME": os.getenv("SERVICES_TABLE_NAME"),
        }

        # create a Lambda function
        self.lambda_function = _lambda.Function(
            self,
            "ServicesStatusLambdaFunction",
            function_name=lambda_function_name,
            runtime=_lambda.Runtime.PYTHON_3_9,  # Runtime environment for the Lambda function
            handler="lambda_function.lambda_handler",  # Entry point for the Lambda function
            code=_lambda.Code.from_asset(
                os.path.join(CURRENT_DIR, "handler")
            ),  # Directory containing the Lambda function code
            environment=environment_variables,  # Environment variables for the Lambda function
        )

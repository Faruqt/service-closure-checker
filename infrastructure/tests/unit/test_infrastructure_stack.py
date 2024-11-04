"""
test_infrastructure_stack.py: This module contains the unit tests for the infrastructure stack.
"""

# library imports
import os
import unittest
from unittest.mock import patch
import aws_cdk as core
import aws_cdk.assertions as assertions

# Import the stacks to be tested
from infrastructure.dynamo_db.services_table import ServicesTableStack
from infrastructure.lambdas.lambda_stack import LambdaStack


class TestInfrastructureStack(unittest.TestCase):
    """
    TestInfrastructureStack: This class contains the unit tests for the infrastructure stack.
    """

    def setUp(self):
        self.app = core.App()

    def test_dynamodb_table_synthesizes_properly(self):
        """
        Test that the DynamoDB table synthesizes properly.
        """
        # Create the stack for your DynamoDB table
        services_table_stack = ServicesTableStack(self.app, "SomeTableStack")

        # Check that the stack is defined
        assert services_table_stack, "The stack should be defined"
        assert isinstance(services_table_stack.table, core.aws_dynamodb.Table)

        template = assertions.Template.from_stack(services_table_stack)

        # Check that the stack creates a DynamoDB table
        template.has_resource_properties(
            "AWS::DynamoDB::Table",
            {
                "TableName": "TestTable",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
                "KeySchema": [
                    {"AttributeName": "service_name", "KeyType": "HASH"},
                ],
                "AttributeDefinitions": [
                    {"AttributeName": "service_name", "AttributeType": "S"},
                ],
            },
        )

    def test_dynamodb_table_has_correct_deletion_policy_in_production_environment(self):
        """
        Test if the DynamoDB table is created with the expected deletion policy.
        """
        # Set the environment to production
        with patch.dict("os.environ", {"ENVIRONMENT": "production"}):
            # Create the stack for your DynamoDB table
            services_table_stack = ServicesTableStack(self.app, "AnotherTestTableStack")

            # Prepare the stack for assertions.
            template = assertions.Template.from_stack(services_table_stack)

            # Check if the DynamoDB table has the expected DeletionPolicy
            template.has_resource("AWS::DynamoDB::Table", {"DeletionPolicy": "Retain"})

    def test_dynamodb_table_has_correct_deletion_policy_in_test_environment(self):
        """
        Test if the DynamoDB table is created with the expected deletion policy.
        """

        # create the stack for your DynamoDB table
        services_table_stack = ServicesTableStack(self.app, "AnotherTestTableStack")

        # Prepare the stack for assertions.
        template = assertions.Template.from_stack(services_table_stack)

        # Check if the DynamoDB table has the expected DeletionPolicy
        template.has_resource("AWS::DynamoDB::Table", {"DeletionPolicy": "Delete"})

    def test_lambda_function_synthesizes_properly(self):
        """
        Test that the Lambda function synthesizes properly.
        """
        # create the stack for your DynamoDB table
        lambda_stack = LambdaStack(self.app, "SomeLambdaStack")

        # Check that the stack is defined
        assert lambda_stack, "The stack should be defined"

        template = assertions.Template.from_stack(lambda_stack)

        # Check that the stack creates a Lambda function
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {
                "Handler": "lambda_function.lambda_handler",
                "Runtime": "python3.9",
                "FunctionName": "TestFunction",
            },
        )

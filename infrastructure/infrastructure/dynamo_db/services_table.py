"""
services_table.py: This file contains the code to create a DynamoDB table to store the services data.
"""

# library imports
import os
from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)
from constructs import Construct


class ServicesTableStack(Stack):
    """
    ServicesTableStack: This class creates a DynamoDB table to store the services data.

    Args:
        Stack (aws_cdk.core.Stack): The base class for Stack
        Construct (aws_cdk.core.Construct): The base class for Construct

    Returns:
        None
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Determine the environment
        environment = os.getenv("ENVIRONMENT", "development")

        # retrieve the table name from the environment variables
        table_name = os.getenv("SERVICES_TABLE_NAME")

        # set the removal policy based on the environment
        removal_policy = (
            RemovalPolicy.DESTROY
            if environment in ["development", "test"]
            else RemovalPolicy.RETAIN
        )

        self.table = dynamodb.Table(
            self,
            "ServicesTable",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="service_name", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,  # Use provisioned billing mode
            read_capacity=5,  # Specify read capacity units
            write_capacity=5,  # Specify write capacity units
            removal_policy=removal_policy,
        )

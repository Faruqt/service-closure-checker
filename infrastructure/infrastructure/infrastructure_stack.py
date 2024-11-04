"""
infrastructure_stack.py: This file contains the code to create the infrastructure stack.
"""

# library imports
from aws_cdk import (
    Stack,
)
from constructs import Construct

# local imports
from infrastructure.dynamo_db.services_table import ServicesTableStack


class InfrastructureStack(Stack):
    """
    InfrastructureStack: This class creates the infrastructure stack.

    Args:
        Stack (aws_cdk.core.Stack): The base class for Stack
        Construct (aws_cdk.core.Construct): The base class for Construct

    Returns:
        None
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instantiate the ServicesTableStack
        services_table_stack = ServicesTableStack(self, "ServicesTableStack")

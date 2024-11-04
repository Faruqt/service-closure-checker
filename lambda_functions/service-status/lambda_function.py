"""
handler.py : This file contains a simple Lambda function that interacts with a DynamoDB table.
"""

# library imports
import os
import logging
import boto3

# local imports
from service_checker import service_checker

dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("SERVICES_TABLE_NAME")
table = dynamodb.Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    lambda_handler: This function interacts with a DynamoDB table.

    Args:
        event (dict): The event data passed to the Lambda function
        context (object): The runtime information of the Lambda function

    Returns:
        dict: The response from the Lambda function
    """

    try:
        # Get the service name from the event data
        service_name = event.get("Details", {}).get("Parameters", {}).get("ServiceName")

        if not service_name:
            logger.warning("Service name is required but not provided")
            return {
                "statusCode": 400,
                "body": {
                    "message": "Service name is required",
                },
            }

        logger.info(f"Checking status for service: {service_name}")
        result_map = service_checker(service_name, table, logger)
        return result_map

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": {
                "message": "Sorry we could not process your request, please try again later",
            },
        }

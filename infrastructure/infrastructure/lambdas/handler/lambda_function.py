"""
lambda_function.py : This file contains a simple Lambda function that returns a response. 
This file will be used to create Lambda functions using the AWS CDK.
"""


def lambda_handler(event, context):
    """
    lambda_handler: This function returns a response when invoked.

    Args:
        event (dict): The event data passed to the Lambda function
        context (object): The runtime information of the Lambda function

    Returns:
        dict: The response from the Lambda function
    """

    return {"statusCode": 200, "body": "Hello from Lambda!"}

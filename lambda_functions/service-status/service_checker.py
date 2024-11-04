from datetime import datetime
from botocore.exceptions import ClientError


def service_checker(service_name, table, logger=None):
    """
    service_checker: This function checks the status of a service.

    Args:
        service_name (str): The name of the service to check
        table (object): The DynamoDB table object
        logger (object): The logger object (optional)

    Returns:
        dict: The response containing the status of the service
    """

    try:
        # Get today's date in the format YYYY-MM-DD
        today = datetime.today().strftime("%Y-%m-%d")

        # Retrieve service information from DynamoDB
        response = table.get_item(Key={"service_name": service_name})

        if "Item" not in response:
            if logger:
                logger.info(f"Service {service_name} not found")
            return {
                "statusCode": 404,
                "Attributes": {
                    "service_name": service_name,
                    "status": "Service not found",
                    "message": f"Service {service_name} not found",
                },
            }

        # Check if today is in the closed dates
        closed_dates = response["Item"].get("closed_dates", [])
        for item in closed_dates:
            if today == item["date"]:
                if logger:
                    logger.info(
                        f"The service {service_name} is closed today for {item['reason']}"
                    )
                return {
                    "statusCode": 200,
                    "Attributes": {
                        "service_name": service_name,
                        "status": "Closed",
                        "message": f"The service {service_name} is closed today for {item['reason']}",
                    },
                }

        # If no closed date matches, the service is open today
        if logger:
            logger.info(f"The service {service_name} is open today")
        return {
            "statusCode": 200,
            "Attributes": {
                "service_name": service_name,
                "status": "Open",
                "message": "The service is open today",
            },
        }

    except ClientError as e:
        # Capture detailed error message for AWS-related issues
        error_message = e.response["Error"].get("Message", str(e))
        if logger:
            logger.error(f"ClientError occurred: {error_message}")
        return {
            "statusCode": 500,
            "Attributes": {
                "service_name": service_name,
                "status": "Error",
                "message": "Sorry, we could not process your request. Please try again later.",
            },
        }

    except Exception as e:
        # Generic error handler
        if logger:
            logger.error(f"An error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "Attributes": {
                "service_name": service_name,
                "status": "Error",
                "message": "Sorry, we could not process your request. Please try again later.",
            },
        }

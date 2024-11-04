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
                "body": {"message": f"Service {service_name} not found"},
            }

        # Check if today is in the closed dates
        closed_dates = response["Item"].get("ClosedDates", [])
        for item in closed_dates:
            if today == item["date"]:
                if logger:
                    logger.info(
                        f"The service {service_name} is closed today for {item['reason']}"
                    )
                return {
                    "statusCode": 200,
                    "body": {
                        "service_name": service_name,
                        "status": f"The service {service_name} is closed today for {item['reason']}",
                    },
                }

        # If no closed date matches, the service is open today
        if logger:
            logger.info(f"The service {service_name} is open today")
        return {
            "statusCode": 200,
            "body": {
                "service_name": service_name,
                "status": "The service is open today",
            },
        }

    except (ClientError, Exception) as e:
        if logger:
            logger.error(f"An error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": {"message": f"An error occurred: {str(e)}"},
        }

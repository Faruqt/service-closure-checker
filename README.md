# SERVICE CLOSURE CHECKER

This project provides a solution for checking the operational status of services, considering specific closed dates (like holidays). It integrates an AWS Lambda function with a DynamoDB table to store and retrieve service status information. The solution is designed to be consumed by Amazon Connect contact flows.

## Project Structure

- **infrastructure**: Contains AWS Cloud Development Kit (CDK) definitions for deploying the Lambda function and the DynamoDB table.
- **lambda_functions**: Contains the Lambda Function for checking the service status
  - **handler.py**: The entry point for the Lambda function that interacts with the DynamoDB table.
  - **service_checker.py**: Contains the logic for checking the service status against closed dates.

## Design Overview

### Storage Definitions

#### DynamoDB Table: `Services`

The DynamoDB table `Services` is used to store information about various services, including their operational status and any specific closed dates. The table structure is as follows:

- **Primary Key**:

  - `service_name` (String): The unique identifier for each service.

- **Attributes**:
  - `closed_dates` (List of Maps): A list containing objects that specify the dates when the service is closed. Each object has the following structure:
    - `date` (String): The date when the service is closed (format: YYYY-MM-DD).
    - `reason` (String): A description of the reason for closure (e.g., "Christmas", "New Year").

#### Example Item in DynamoDB Table

```json
{
  "service_name": "Customer Support",
  "closed_dates": [
    { "date": "2024-12-25", "reason": "Christmas" },
    { "date": "2025-01-01", "reason": "New Year" }
  ]
}
```

## Lambda function

The Lambda function service_checker retrieves the service information from the DynamoDB table and checks if the service is closed on the current date. It returns a response in the following format:

```json
{
  "statusCode": 200,
  "Attributes": {
    "service_name": "Customer Support",
    "status": "The service is open today"
  }
}
```

In the case of a closed date, the response will indicate the reason for closure:

```json
{
  "statusCode": 200,
  "Attributes": {
    "service_name": "Customer Support",
    "status": "The service is closed today for Christmas"
  }
}
```

### Error Handling

The Lambda function includes error handling to manage cases where:

- The service name is not provided.
- The service is not found in the DynamoDB table.
- An error occurs during the interaction with DynamoDB.

In these cases, appropriate error messages are returned to ensure a smooth user experience.

### Integration with Amazon Connect

The Lambda function is designed to be integrated into Amazon Connect contact flows, enabling the automated checking of service availability based on customer inquiries. The responses can be utilized within the contact flow to guide customer interactions.

## Deployment

To deploy the project, use the AWS Cloud Development Kit (CDK). Ensure that your AWS credentials are configured properly.

## Conclusion

This project provides a robust solution for managing service availability, leveraging AWS Lambda and DynamoDB to create a seamless experience for users interacting through Amazon Connect.

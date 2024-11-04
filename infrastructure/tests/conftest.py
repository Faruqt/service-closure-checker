"""
conftest.py: This module is used to define fixtures that can be used in multiple test modules.
"""

# library imports
import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """
    Set environment variables for the test session.

    This fixture sets the environment variables required for the application
    to run in a testing environment. It ensures that all tests run with the correct
    configuration settings.

    Note: This fixture is automatically applied to all tests due to autouse=True.
    """
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SERVICES_TABLE_NAME"] = "TestTable"
    os.environ["SERVICE_STATUS_LAMBDA_FUNCTION_NAME"] = "TestFunction"

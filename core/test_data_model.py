from typing import Optional
from pydantic import BaseModel


class APIData(BaseModel):
    """
    A Pydantic model representing the structure of an individual API test case.

    This model is used to validate and store the data for each API test,
    including test identifiers, request details, expected responses, and status.

    Attributes:
        TestId (str): A unique identifier for the test case.
        TestCase (str): The name or description of the test case.
        Run (str): A flag indicating whether the test should be run ('Y' or 'N').
        Method (str): The HTTP method to be used in the request (e.g., GET, POST).
        URL (str): The base URL for the API request.
        Endpoint (str): The specific API endpoint to call (relative to the base URL).
        Authorization (Optional[str]): The authorization token or type, if applicable.
        User (Optional[str]): The username for basic authentication (if required).
        Password (Optional[str]): The password for basic authentication (if required).
        Headers (Optional[dict]): Additional headers for the request, if any.
        Body (Optional[dict]): The body of the request, if applicable.
        ExpectedStatusCode (int): The expected HTTP status code in the response.
        ExpectedResponse (Optional[dict]): The expected response body, if applicable.
        Status (Optional[str]): The status of the test case after execution (PASSED, FAILED, SKIPPED).
        Error (Optional[str]): An error message in case the test case fails.
    """

    TestId: str  # Unique identifier for the test case
    TestCase: str  # Name or description of the test case
    Run: str  # Flag to indicate if the test should run ('Y' or 'N')
    Method: str  # HTTP method (e.g., GET, POST)
    URL: str  # Base URL for the API request
    Endpoint: str  # API endpoint (relative to the base URL)

    # Optional fields for authentication and request details
    Authorization: Optional[str] = None  # Authorization token (if applicable)
    User: Optional[str] = None  # Username for basic auth (if applicable)
    Password: Optional[str] = None  # Password for basic auth (if applicable)

    # Optional fields for headers and request body
    Headers: Optional[dict] = None  # Additional headers for the request
    Body: Optional[dict] = None  # The body of the API request

    ExpectedStatusCode: int  # Expected HTTP status code from the response
    ExpectedResponse: Optional[dict] = None  # Expected response body (optional)

    # Fields to store the result of the test case after execution
    Status: Optional[str] = None  # Status of the test case ('PASSED', 'FAILED', 'SKIPPED')
    Error: Optional[str] = None  # Error message if the test fails

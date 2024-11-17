import pytest
import time
from core.api_client import APIClient
from core.db_manager import DBManager
from core.excel_reader import ExcelReader
from core.excel_writer import ExcelWriter

# Fixture to load test data from an Excel file for the entire test module
@pytest.fixture(scope="module")
def test_data():
    """
    Loads test data from an Excel file (data/test_data.xlsx) to be used across test cases.

    Returns:
        list: A list of test cases, each containing the data needed for API requests.

    Raises:
        pytest.fail: If no data is found in the Excel file.
    """
    reader = ExcelReader('data/test_data.xlsx')
    data = reader.load_data()
    if not data:
        pytest.fail("No se encontraron datos en el archivo Excel.")  # No data found in Excel
    return data

# Helper function to prepare headers and authorization based on the test case
def prepare_headers_and_auth(test_case):
    """
    Prepares the request headers and authorization method for an API call based on the test case data.

    Args:
        test_case (TestCase): A single test case object containing necessary details for the request.

    Returns:
        tuple: A tuple containing headers dictionary and authorization credentials (tuple).
               If no authentication is needed, the auth will be None.
    """
    if test_case.Authorization:
        headers = test_case.Headers if test_case.Headers else {}
        headers['Authorization'] = test_case.Authorization
        auth = None
    elif test_case.User and test_case.Password:
        headers = test_case.Headers if test_case.Headers else {}
        auth = (test_case.User, test_case.Password)
    else:
        headers = test_case.Headers if test_case.Headers else {}
        auth = None

    return headers, auth

# Helper function to send API request and measure the time taken for the request
def send_request_and_measure_time(client, test_case, headers, auth):
    """
    Sends an API request using the provided client and test case, and measures the time taken for the request.

    Args:
        client (APIClient): The client used to send the request.
        test_case (TestCase): A test case containing request details (method, URL, body, etc.).
        headers (dict): Headers to be included in the request.
        auth (tuple or None): Authentication credentials, or None if no authentication is required.

    Returns:
        tuple: A tuple containing the response object, the duration of the request in seconds,
               and the size of the response in bytes.
    """
    start_time = time.time()  # Start timing the request
    try:
        response = client.send_request(
            test_case.Method,
            test_case.URL,
            test_case.Endpoint,
            headers=headers,
            body=test_case.Body,
            auth=auth
        )
    except Exception as e:
        pytest.fail(f"API request failed: {e}")  # Fail the test if the request fails

    end_time = time.time()  # End timing the request
    duration = end_time - start_time  # Calculate the time taken
    response_size = len(response.text)  # Get the size of the response in bytes

    return response, duration, response_size

# Helper function to check if the response matches the expected result
def check_response(response, test_case):
    """
    Compares the response from the API with the expected result as defined in the test case.

    Args:
        response (Response): The response object returned from the API call.
        test_case (TestCase): The test case containing expected status code and response.

    Returns:
        tuple: A tuple containing the test result status ('PASSED' or 'FAILED')
               and an error message (or None if no error).
    """
    if response.status_code == test_case.ExpectedStatusCode:
        status = "PASSED"
        error = None
    else:
        status = "FAILED"
        error = f"Expected status code: {test_case.ExpectedStatusCode}, Got: {response.status_code}"

    try:
        response_body = response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text
        if response_body != test_case.ExpectedResponse:
            status = "FAILED"
            error = f"Expected response: {test_case.ExpectedResponse}, Got: {response_body}"
    except ValueError as e:
        status = "FAILED"
        error = f"Failed to parse response: {str(e)}"

    return status, error

# Main test function that runs all the test cases and logs the results
def test_api(test_data):
    """
    Executes API tests based on the provided test data and logs results to a database and an Excel file.

    Args:
        test_data (list): A list of test cases to be executed.

    Logs:
        - Results to the database.
        - A summary of the execution to the console.
        - Updates the results in the Excel file.
    """
    client = APIClient()  # Initialize the API client
    db_manager = DBManager('reports/results.db')  # Initialize database manager for results
    db_manager.create_tables()  # Create necessary tables in the database
    execution_name = f"TestExecution_{time.strftime('%Y%m%d_%H%M%S')}"  # Unique execution name based on current time
    execution_id = db_manager.insert_test_execution(execution_name)  # Insert the test execution record
    if not execution_id:
        pytest.fail("No se pudo crear la ejecución en la base de datos.")  # Fail the test if execution could not be logged

    # Lists to hold durations, response sizes, and individual test results
    durations = []
    response_sizes = []
    results = []

    # Loop through all test cases and execute them
    for test_case in test_data:
        if test_case.Run == "N":  # If 'Run' is "N", the test case is skipped
            status = "SKIPPED"
            error = "Test skipped (Run = N)"
        else:
            headers, auth = prepare_headers_and_auth(test_case)  # Prepare headers and auth for the request
            response, duration, response_size = send_request_and_measure_time(client, test_case, headers, auth)  # Send the request
            status, error = check_response(response, test_case)  # Check the response against the expected values

        # Prepare the result dictionary
        result = {
            "TestId": test_case.TestId,
            "TestCase": test_case.TestCase,
            "Status": status,
            "Error": error,
            "Method": test_case.Method,
            "URL": test_case.URL,
            "Endpoint": test_case.Endpoint,
            "ExpectedStatusCode": test_case.ExpectedStatusCode,
            "ActualStatusCode": response.status_code if status != "SKIPPED" else None,
            "Duration": duration if status != "SKIPPED" else None,
            "ResponseSize": response_size if status != "SKIPPED" else None
        }

        # Insert the test result into the database
        db_manager.insert_test_result(execution_id, result)

        # Append the result data for summary reporting
        durations.append(duration)
        response_sizes.append(response_size)
        results.append(result)

    # Prepare a summary of the test execution
    summary = {
        "TotalTests": len(test_data),
        "PassedTests": sum(1 for r in results if r['Status'] == "PASSED"),
        "FailedTests": sum(1 for r in results if r['Status'] == "FAILED"),
        "SkippedTests": sum(1 for r in results if r['Status'] == "SKIPPED"),
        "AvgDuration": sum(durations) / len(durations) if durations else 0,
        "TotalResponseSize": sum(response_sizes),
    }

    # Insert the summary into the database
    db_manager.insert_test_summary(execution_id, summary)

    # Print the execution summary to the console
    print("\n--- Resumen de la Ejecución de Pruebas ---")
    print(f"Total de pruebas: {summary['TotalTests']}")
    print(f"Pruebas pasadas: {summary['PassedTests']}")
    print(f"Pruebas falladas: {summary['FailedTests']}")
    print(f"Pruebas saltadas: {summary['SkippedTests']}")
    print(f"Duración promedio: {summary['AvgDuration']:.2f} segundos")
    print(f"Tamaño total de respuestas: {summary['TotalResponseSize']} bytes")

    # Update the Excel file with the test results
    ExcelWriter('data/test_data.xlsx').update_results(results)

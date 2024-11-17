import requests
from requests.exceptions import RequestException

class APIClient:
    """
    A simple API client that provides a method to send HTTP requests using the `requests` library.

    This class is used to interact with APIs, allowing the sending of requests using different HTTP methods
    (GET, POST, PUT, DELETE, etc.), with support for headers, request bodies, and basic authentication.

    Methods:
        send_request(method, url, endpoint, headers=None, body=None, auth=None):
            Sends an HTTP request and returns the response.
    """

    @staticmethod
    def send_request(method, url, endpoint, headers=None, body=None, auth=None):
        """
        Sends an HTTP request to a specified URL and endpoint.

        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            url (str): The base URL for the API.
            endpoint (str): The API endpoint to append to the base URL.
            headers (dict, optional): Headers to include in the request. Default is None.
            body (dict, optional): The JSON body to send with the request. Default is None.
            auth (tuple, optional): A tuple containing username and password for basic authentication. Default is None.

        Returns:
            response (Response): The response object from the request.
            If the request fails, returns a dictionary containing the error message.
        """
        try:
            # Combine the base URL and endpoint to form the full URL
            full_url = f"{url}{endpoint}"

            # Send the request using the specified method
            response = requests.request(
                method=method,
                url=full_url,
                headers=headers,  # Optional headers
                json=body,  # Convert the body to JSON (if provided)
                auth=auth,  # Optional basic authentication
            )

            return response  # Return the response object

        except RequestException as e:
            # Catch any request exceptions (network issues, invalid responses, etc.)
            return {"error": f"Request failed: {e}"}  # Return an error message if the request fails

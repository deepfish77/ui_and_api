import requests
import pytest

BASE_URL = "https://poetrydb.org/"


def execute_get_call(base_url, endpoint, header=None, params=None):
    """
    Executes a GET request to the specified endpoint with optional headers and parameters.
    """
    if header is None:
        header = {}
    if params is None:
        params = {}

    constructed_url = f"{base_url}{endpoint}"

    try:
        # Send GET request
        api_response = requests.get(constructed_url, headers=header, params=params)
        status_code = api_response.status_code
        print(f"API Response Status Code: {status_code}")

        # Raise exception for HTTP errors
        api_response.raise_for_status()
        return api_response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Exception: {req_err}")

    return None



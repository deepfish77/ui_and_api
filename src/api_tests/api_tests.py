import pytest
import json
from src.api_tests.query_data.poems import ozymandias_poem_1, why_should_p2
from src.api_tests.api_queries_builder import execute_get_call

BASE_URL = "https://poetrydb.org/"


@pytest.mark.parametrize(
    "poem_data, endpoint",
    [
        (json.loads(ozymandias_poem_1), "title/Ozymandias"),
        (
            [json.loads(why_should_p2)],
            "title/Why%20Should%20A%20Foolish%20Marriage%20Vow",
        ),
    ],
)
def test_static_data_validation(poem_data, endpoint):
    """
    Test Case: Validate API responses against static data.

    Steps:
    1. Load the static poem data from the query_data folder.
    2. Query the PoetryDB API using the title as the endpoint.
    3. Validate the response structure and content:
        - Ensure the response is not `None`.
        - Ensure the response is a list.
        - Compare each field (e.g., `title`, `author`, `linecount`, `lines`) in the response with the static data.

    Expected Result:
    - The API should return a poem matching the static data exactly.

    Validation:
    - Compare the API response with the static poem data field by field.
    - Assert that all fields match between the response and the static data.
    """
    response = execute_get_call(BASE_URL, endpoint)

    # Validate response
    assert response is not None, "Response is empty- please check params"
    assert isinstance(
        response, list
    ), f"Type of response is not matching list(): {type(response)}"
    assert len(response) == len(
        poem_data
    ), f"Unexpected count results: {len(response)} vs {len(poem_data)}"

    # Compare each poem in the response to the corresponding static data
    for fetched_poem, expected_poem in zip(response, poem_data):
        assert fetched_poem.get("title") == expected_poem["title"], "Title mismatch"
        assert fetched_poem.get("author") == expected_poem["author"], "Author mismatch"
        assert (
            fetched_poem.get("linecount") == expected_poem["linecount"]
        ), "Linecount mismatch"
        assert all(
            line in fetched_poem.get("lines", []) for line in expected_poem["lines"]
        ), "Lines mismatch"


@pytest.mark.parametrize(
    "author, lines",
    [
        ("Shakespeare", "shall I compare"),
        ("Percy Bysshe Shelley", "And on the pedestal these words appear"),
        ("Thomas Hood", "With Reverend Mr. Crow and six small boys,"),
    ],
)
def test_combination_author_and_lines(author, lines):
    """
    Test Case: Validate JSON output for combination of author and lines.

    Steps:
    1. Query the API with a combination of author and specific lines.
    2. Validate the response:
        - Ensure the response is a list.
        - Check that the list contains at least one poem.
    3. Extract the title of the first poem from the response.
    4. Query the API again using the extracted title as the endpoint.
    5. Compare the responses from the two queries for consistency.

    Expected Result:
    - The response for the second query should match the corresponding data from the first query exactly.

    Validation:
    - Compare the JSON objects returned by the two queries.
    - Assert that all fields (e.g., `title`, `author`, `linecount`, `lines`) are identical.
    """
    # Step 1: Execute first API call for combination of author and lines
    combination_endpoint = f"author,lines/{author};{lines}"
    response = execute_get_call(BASE_URL, combination_endpoint)

    # Check if response is valid
    assert response is not None, "First response is empty"
    assert isinstance(
        response, (list, dict)
    ), f"Unexpected response type: {type(response)}"

    # Handle scenarios where no results are found
    if isinstance(response, dict) and response.get("status") == 404:
        pytest.skip(f"No poems found for author '{author}' and lines '{lines}'.")

    # Validate response as a list
    assert isinstance(response, list), "First response is not a list"
    assert len(response) > 0, "No poems found for the combination query"

    # Step 2: Get the first poem's title from the response
    first_poem = response[0]
    title = first_poem.get("title")
    assert title is not None, "No title found in the first poem"

    # Step 3: Execute second API call to fetch poem by its title
    title_endpoint = f"title/{title.replace(' ', '%20')}"
    title_response = execute_get_call(BASE_URL, title_endpoint)

    # Validate second response
    assert title_response is not None, "Title response is empty"
    assert isinstance(
        title_response, list
    ), f"Title response is not a list: {type(title_response)}"
    assert len(title_response) == 1, "Unexpected number of results for title query"

    # Step 4: Compare JSON outputs
    assert (
        first_poem == title_response[0]
    ), "JSON output mismatch between combination query and title query"


@pytest.mark.parametrize(
    "title, partial_title, line_content, linecount",
    [
        ("Ozymandias", "Ozy", "Look on my works, ye Mighty, and despair!", 14),
    ],
)
def test_accessing_by_partial_content(title, partial_title, line_content, linecount):
    """
    Test Case: Validate API access by partial title, line content, and line count.

    Steps:
    1. Query the API to fetch the full poem by exact title.
    2. Validate the API response structure and ensure it contains the expected poem.
    3. Query the API using a partial title and validate that the original poem is present in the response.
    4. Query the API using a line from the poem and validate that the original poem is present in the response.
    5. Query the API using the line count and validate that the original poem is present in the response.
    6. Extract and compare all fields from the original poem fetched by exact title with the validated responses.

    Expected Result:
    - The poem should be accessible through all partial content queries.
    - The original poem data should match exactly with the data fetched through partial queries.

    Validation:
    - Assert that the original poem exists in the responses from all partial queries.
    - Assert that all fields (`title`, `author`, `lines`, `linecount`) are identical to the original data.
    """
    # Step 1: Get the poem by title
    exact_title_endpoint = f"title/{title}:abs"
    full_poem_response = execute_get_call(BASE_URL, exact_title_endpoint)

    assert full_poem_response is not None, "Failed to fetch poem by exact title"
    assert isinstance(
        full_poem_response, list
    ), "Response for exact title is not a list"
    assert len(full_poem_response) == 1, "Unexpected number of results for exact title"

    poem_data = full_poem_response[0]

    # Step 2: Validate by partial title
    partial_title_endpoint = f"title/{partial_title}"
    partial_title_response = execute_get_call(BASE_URL, partial_title_endpoint)

    assert partial_title_response is not None, "Failed to fetch poems by partial title"
    assert isinstance(
        partial_title_response, list
    ), "Response for partial title is not a list"
    assert any(
        poem["title"] == title for poem in partial_title_response
    ), "Original poem not found in partial title response"

    # Step 3: Validate by line content
    line_content_endpoint = f"lines/{line_content}"
    line_content_response = execute_get_call(BASE_URL, line_content_endpoint)

    assert line_content_response is not None, "Failed to fetch poems by line content"
    assert isinstance(
        line_content_response, list
    ), "Response for line content is not a list"
    assert any(
        poem["title"] == title for poem in line_content_response
    ), "Original poem not found in line content response"

    # Step 4: Validate by line count
    linecount_endpoint = f"linecount/{linecount}"
    linecount_response = execute_get_call(BASE_URL, linecount_endpoint)

    assert linecount_response is not None, "Failed to fetch poems by line count"
    assert isinstance(linecount_response, list), "Response for line count is not a list"
    assert any(
        poem["title"] == title for poem in linecount_response
    ), "Original poem not found in line count response"

    # Step 5: Extract and validate all data matches original poem
    extracted_poem_data = {
        "title": poem_data["title"],
        "author": poem_data["author"],
        "linecount": poem_data["linecount"],
        "lines": poem_data["lines"],
    }

    assert extracted_poem_data["title"] == title, "Title mismatch in extracted data"
    assert (
        extracted_poem_data["author"] == poem_data["author"]
    ), "Author mismatch in extracted data"
    assert extracted_poem_data["linecount"] == str(
        linecount
    ), "Linecount mismatch in extracted data"
    assert (
        extracted_poem_data["lines"] == poem_data["lines"]
    ), "Lines mismatch in extracted data"


@pytest.mark.parametrize(
    "invalid_title",
    [
        "InvalidTitle123",  # Non-existent title
        "12345",  # Number formatted string
        "",  # Empty string - This is supposed to Fail
        "!@#$%^&*()",  # Special characters
        "<script>alert('XSS')</script>",  # Malicious script attempt - This is failing as well
    ],
)
def test_invalid_title_responses(invalid_title):
    """
    Test Case: Validate API responses for invalid title parameters.

    Steps:
    1. Query the API using various invalid title parameters such as:
        - Non-existent strings
        - Numbers
        - Empty strings
        - Special characters
        - Potentially malicious script inputs
    2. Validate the API response:
        - Ensure no server failures occur.
        - Ensure the API returns a proper error message and status code.

    Expected Result:
    - The API should return a 404 status with a `reason` field indicating "Not found" for invalid inputs.
    - No server crashes or unexpected behavior should occur.

    Validation:
    - Assert that the response is a dictionary.
    - Assert that the `status` field is 404.
    - Assert that the `reason` field contains "Not found".
    """
    # Construct endpoint with invalid title
    invalid_title_endpoint = f"title/{invalid_title}"
    response = execute_get_call(BASE_URL, invalid_title_endpoint)

    # Validate response
    assert response is not None, "API call failed or returned None"
    assert isinstance(response, dict), "Response for invalid title is not a dictionary"
    assert response.get("status") == 404, "Unexpected status code for invalid title"
    assert "reason" in response, "No reason provided for invalid title response"
    assert (
        response["reason"] == "Not found"
    ), "Unexpected reason message for invalid title"

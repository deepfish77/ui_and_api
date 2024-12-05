# ui_and_api
UI and API tests implementation
# PoetryDB API Test Suite

This repository contains a test suite for validating the functionality of the PoetryDB API using `pytest`. The tests ensure the correctness of the API responses, handle edge cases, and validate against static data.

---

## Test Cases

The following test cases are implemented:

| Test Case ID | Test Name                         | Description                                                                                                       | Steps                                                                                                           | Expected Result                                                                                                     | Validation                                                                                                           |
|--------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| TC01         | Static Data Validation           | Validates API responses against static data stored locally.                                                       | 1. Fetch data using the API for exact title.<br>2. Compare response with local static data.                     | API response matches the locally stored data exactly.                                                               | Validate `title`, `author`, `linecount`, and `lines` fields match the static data.                                   |
| TC02         | Combination of Author and Lines  | Queries poems by author and a partial line, then validates data by querying the title separately.                 | 1. Fetch data using author and lines.<br>2. Fetch data by title from the first response.<br>3. Compare results. | The poem fetched by author and lines matches the poem fetched by title.                                             | Ensure JSON output is identical for both responses.                                                                 |
| TC03         | Accessing by Partial Content     | Validates access to a poem by partial title, line content, and line count.                                        | 1. Fetch the full poem by exact title.<br>2. Validate partial title.<br>3. Validate line content.<br>4. Validate line count.<br>5. Compare data. | The poem is accessible via partial title, line content, and line count. Data matches across all queries.            | Validate `title`, `author`, `linecount`, and `lines` fields match the full poem data.                                |
| TC04         | Invalid Title Responses          | Validates API behavior for invalid title inputs, including special characters, numbers, and empty strings.        | 1. Query the API using invalid titles.<br>2. Validate response for each input.                                  | API returns a `404 Not Found` status and appropriate error message.                                                 | Ensure response is a dictionary with `status: 404` and `reason: Not found`.                                         |

---

## Usage Instructions

### Prerequisites

1. Python version 3.7 or higher.
2. Install dependencies using `pip`.

### Clone the Repository

```bash
git clone  https://github.com/deepfish77/ui_and_api.git

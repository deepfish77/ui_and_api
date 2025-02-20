from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse


def intercept_requests(url):
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Specify the path to your downloaded ChromeDriver executable
    driver = webdriver.Chrome(
        executable_path="C:\\your_driver\\path\\here\\chromedriver.exe",  # Update this path
        options=chrome_options,
    )

    try:
        driver.get(url)
        time.sleep(10)
        for request in driver.requests:
            print("Request URL:", request.url)
            print("Request Method:", request.method)
            print("Request Headers:", request.headers)

            if request.response:
                print("Response Status Code:", request.response.status_code)
                print("Response Headers:", request.response)
            print("-" * 80)
    finally:
        driver.quit()



def intercept_and_extract_tokens(url):
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the Selenium Wire Chrome driver (update executable_path if necessary)
    driver = webdriver.Chrome(
        executable_path="C:\\your_driver\\path\\here\\chromedriver.exe",  # Update this path
        options=chrome_options,
    )

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait to allow requests to be made (adjust as needed)
        time.sleep(10)

        # Iterate over all intercepted requests
        for request in driver.requests:
            print("======================================")
            print("Request URL:", request.url)
            print("Request Method:", request.method)
            print("Request Headers:", request.headers)

            # Check for an Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header:
                print("Found token in header: ", auth_header)

            # Parse URL query parameters to see if a token is passed there
            parsed_url = urllib.parse.urlparse(request.url)
            qs = urllib.parse.parse_qs(parsed_url.query)
            for key, value in qs.items():
                if "token" in key.lower() or "auth" in key.lower():
                    print(f"Found token in URL parameter: {key} = {value}")

            # Optionally, you could also inspect request.body if needed:
            if request.body:
                print("Request Body:", request.body)

            print("======================================\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_url = "https://example.cne.two.com/"  # Replace with the target URL
    intercept_and_extract_tokens(test_url)

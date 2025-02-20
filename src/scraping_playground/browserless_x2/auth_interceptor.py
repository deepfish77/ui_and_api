import os
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    NetworkInterceptor,
    InterceptedRequest,
)
import asyncio


async def on_request(data: InterceptedRequest, auth_container: dict):
    # Intercept GET requests
    if data.request.method == "GET":
        try:
            # print("Request Headers:", data.request.headers)
            auth_header = data.request.headers.get("Authorization")
            if auth_header:
                auth_container["auth"] = auth_header
                print("Found auth header:", auth_header)
        except KeyError:
            print("No 'Authorization' header found in this request.")


async def main(url):
    # Use a mutable container (dictionary) to store the auth token.
    auth_container = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    # Uncomment and set your proxy if needed:
    # options.single_proxy = os.getenv("mobileproxy")

    async with webdriver.Chrome(options=options) as driver:
        # Pass the auth_container to the on_request callback using a lambda
        async with NetworkInterceptor(
            driver, on_request=lambda data: on_request(data, auth_container)
        ):
            await driver.get(url=url)
            # Wait for a few seconds to allow network requests to be made
            await driver.sleep(3)

    # Return the token from the container (or None if not found)
    return auth_container.get("auth")


def get_token_for_url(url):
    # Replace with your target URL
    auth_token = asyncio.run(main(url))
    print("Returned auth token:", auth_token)
    return auth_token


# get_token_for_url("https://example.cne.bob.ec/dada")

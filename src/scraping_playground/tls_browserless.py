import asyncio
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    NetworkInterceptor,
    InterceptedRequest,
)
import tls_client
from rich import print

# Initialize the TLS client session
session = tls_client.Session(
    client_identifier="chrome_116",
    ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
    h2_settings={
        "HEADER_TABLE_SIZE": 65536,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_HEADER_LIST_SIZE": 262144,
    },
    supported_signature_algorithms=[
        "ECDSAWithP256AndSHA256",
        "PSSWithSHA256",
        "PKCS1WithSHA256",
        "ECDSAWithP384AndSHA384",
        "PSSWithSHA384",
        "PKCS1WithSHA384",
        "PSSWithSHA512",
        "PKCS1WithSHA512",
    ],
    supported_versions=["1.3", "1.2"],
    key_share_curves=["X25519"],
    cert_compression_algo="brotli",
    pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
    connection_flow=15663105,
    header_order=["accept", "user-agent", "accept-encoding", "accept-language"],
)

async def on_request(data: InterceptedRequest, session: tls_client.Session):
    # Intercept API requests and handle them with tls_client
    if "api" in data.request.url:
        print(f"Intercepted request to: {data.request.url}")

        # Prepare headers from the intercepted request
        headers = dict(data.request.headers)

        # Make the request with tls_client instead of the browser
        response = session.get(data.request.url, headers=headers)

        if response.ok:
            print("Response Status:", response.status_code)
            print("Response Data:", response.json())
        else:
            print("Failed to fetch data using tls_client.")

async def main(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    async with webdriver.Chrome(options=options) as driver:
        async with NetworkInterceptor(
            driver, on_request=lambda data: on_request(data, session)
        ):
            await driver.get(url=url)
            await driver.sleep(5)


if __name__ == "__main__":
    asyncio.run(main("https://example.com"))

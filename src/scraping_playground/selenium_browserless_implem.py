import os
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    NetworkInterceptor,
    InterceptedRequest,
)
import asyncio
from rich import print

proxy = os.getenv("mobileproxy")


async def on_request(data: InterceptedRequest):
    if "api" in data.request.url and data.request.method == "GET":
        global auth
        try:
            if data.request.headers["authorization"]:
                auth = data.request.headers
        except KeyError:
            print("No header found")


async def main(url):

    options = webdriver.ChromeOptions()
    # options.single_proxy = proxy

    async with webdriver.Chrome(options=options) as driver:
        async with NetworkInterceptor(driver, on_request=on_request):
            await driver.get(url=url)
            await driver.sleep(6)


asyncio.run(main=main)

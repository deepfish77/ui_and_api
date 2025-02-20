import os
import asyncio
from selenium_driverless.types.by import By
from selenium_driverless import webdriver
from asynciolimiter import Limiter

rate_limiter = Limiter(1 / 3)
proxy = os.getenv("my proxy path")

if proxy is None:
    print("no proxy found")
    quit()


async def get_data_rate_limit(driver, url, by=By.CSS, value="script[type='application/ld+json']"):
    await rate_limiter.wait()
    new_context = await driver.new_context()
    await new_context.get(url)
    schema = await new_context.find_element(by, value)
    # print(await schema.text)
    await new_context.close()


async def main(url="https://your_path.html"):
    options = webdriver.ChromeOptions()
    async with webdriver.Chrome(options=options) as driver:
        await driver.set_single_proxy(proxy)
        await driver.get(
            url,
            wait_load=True,
        )

        products = await driver.find_elements(
            By.CSS, "div.product-grid-product__figure"
        )

        urls = []
        for p in products:
            data = await p.find_element(By.CSS, "a")
            link = await data.get_dom_attribute("href")
            urls.append(link)

        tasks = [get_data_rate_limit(driver, url) for url in urls]
        await asyncio.gather(*tasks)


asyncio.run(main())

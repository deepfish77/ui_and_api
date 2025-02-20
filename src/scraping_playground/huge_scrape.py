import asyncio
import os
from curl_cffi.requests import AsyncSession
import logging
from rich.logging import RichHandler
import time
from pymongo import MongoClient
import csv


PROXY = "stickyproxy"
MONGOCON = "192.168..."
MONGOPORT = 32769
MONGODB = "scrapeditems"
MONGOCOL = "product"

m_client = MongoClient(MONGOCON, MONGOPORT)
db = m_client[MONGODB]
collection = db[MONGOCOL]

start_time = time.time()
logging.basicConfig(
    format="{asctime} - {levelname} = {messsage}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def get_urls_from_file(csv_path=""):
    with open(csv_path, "r") as file:
        reader = csv.reader()
        urls = [url[0] for url in reader]
        return urls


async def execute_scrape_urls():
    async with AsyncSession() as session:
        proxy = os.getenv(PROXY)
        if proxy is not None:
            log.info("Proxy found")
            session.proxies = {"http": proxy, "https": proxy}
        else:
            log.warning("No Matching proxy found, please check proxy configuration")
        tasks = []
        urls = get_urls_from_file()
        for url in urls:
            task = session.get(url)
            tasks.append(task)

        result = await asyncio.gather(*tasks)
    return result


def main():
    data = asyncio.run(execute_scrape_urls())
    failed = []
    results = []

    for response in data:
        if response.status_code != 200:
            log.warning(f"failed on, {response.status_code}")
            failed.append(response.url)
        else:
            results.append({"url": response.url, "date": "", "html": response.text})

    inserted = collection.insert_many(results)
    log.info(inserted)

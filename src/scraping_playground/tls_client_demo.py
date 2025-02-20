import os
import logging
from extruct.jsonld import JsonLdExtractor
from rich.logging import RichHandler
import tls_client
from tls_client.sessions import TLSClientExeption


def setup_logger():
    """
    Sets up and returns a logger using the RichHandler for colored output.
    """
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger("rich")


def create_session():

    session = tls_client.Session(
        client_identifier="chrome_120", random_tls_extension_order=True
    )

    # Update proxies using environment variables
    session.proxies.update(
        {"http": os.getenv("mobileproxyuk"), "https": os.getenv("mobileproxyuk")}
    )

    # Update headers
    session.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Priority": "u=1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        }
    )

    return session


def execute_crawler(url="https://eu.example.com/gb/en/shop/collections?page=1"):

    log = setup_logger()
    jsde = JsonLdExtractor()
    session = create_session()
    response = session.get(url=url)
    data = jsde.extract(response)
    log.info(f"Status code: {data}")

    received_products = []
    for item in data[1]["itemListElement"]:
        received_products.append(item)
        log.info(f"item {item} added successfully")

    for product in received_products:
        try:
            response = session.get(product["url"])
            data = jsde.extract(response.text)
        except Exception as e:
            print("failed to extract with the error", e)

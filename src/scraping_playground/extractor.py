import redis
import logging
import requests
from pymongo import MongoClient
import time

def get_logger():
    # Placeholder function for creating or retrieving a logger
    return logging.getLogger(__name__)

class Extractor:
    def __init__(self):
        self.logger = get_logger()
        self.session = requests.Session()
        self.redis_client = redis.Redis(host="localhost", port=6379)
        self.mongo_client = MongoClient()
        self.db = self.mongo_client["testdb"]
        self.collection = self.db["testcol"]

    def scrape(self):
        while True:
            url = self.redis_client.rpop("url_queue")
            if not url:
                self.logger.info("No URLs, waiting")
                time.sleep(1)
            else:
                try:
                    resp = self.session.get(url)
                    posted_id = self.collection.insert_one(resp.json()).inserted_id
                    self.logger.info(f"Inserted ID {posted_id} for {url}")
                except Exception as e:
                    self.logger.warning(f"Failed to fetch URL {url}: {e}")
                    self.redis_client.rpush("url_queue", url)
                    self.logger.info(f"URL back to queue: {url}")

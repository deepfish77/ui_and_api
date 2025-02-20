import redis
import logging
import requests
from bs4 import BeautifulSoup

class Seeder:
    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis(host="localhost", port=6379)
        self.logger = logging.getLogger()

    def seed(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "xml")
        id = soup.find("id").text
        self.redis.lpush("mylist", id)
        self.logger.info(f"{url} added to queue")

if __name__ == "__main__":
    seeder = Seeder()
    url = "https://www.somethingfromtheweb.com"
    seeder.seed(url)
from .crawler import Crawler
from .shared.selenium import create_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait


class JsCrawler(Crawler):
    def __init__(self):
        self.driver = None
        self.wait = None

    def prepare(self):
        self.driver = create_chrome_driver()
        self.driver.get(self.url())
        self.wait = WebDriverWait(self.driver, 10)

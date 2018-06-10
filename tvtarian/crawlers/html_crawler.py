from .crawler import Crawler
from .shared.beautiful_soup import create_soup


class HtmlCrawler(Crawler):
    def __init__(self):
        self.soup = None

    def prepare(self):
        self.soup = create_soup(self.url())

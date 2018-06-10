import datetime

from .html_crawler import HtmlCrawler
from .shared.const import ANOTHER_SKY_ID


class Anothersky(HtmlCrawler):
    def url(self):
        return 'http://www.ntv.co.jp/anothersky/'

    def id(self):
        return ANOTHER_SKY_ID

    def title(self):
        return self.soup.title.text

    def date(self):
        date_str = self.block().splitlines()[0][5:].split('.')
        return datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    def name(self):
        return self.block().splitlines()[2]

    def description(self):
        return "".join(self.block().splitlines())

    def block(self):
        return self.soup.find(id="nextGuest").p.text

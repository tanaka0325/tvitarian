import datetime
import re

from .html_crawler import HtmlCrawler
from .shared.const import JOHNETSU_ID


class Johnetsu(HtmlCrawler):
    def url(self):
        return 'https://www.mbs.jp/jounetsu/'

    def id(self):
        return JOHNETSU_ID

    def title(self):
        return self.soup.title.text

    def date(self):
        d = self.block().find(id="PeopleDate")
        date_str = d.text.splitlines()[1].strip()
        date_list = re.split('[年月日]', date_str)
        return datetime.date(
            int(date_list[0]), int(date_list[1]), int(date_list[2]))

    def name(self):
        return self.block().find(id="profile").find(class_="name").text

    def description(self):
        return self.block().find(class_="catch").text

    def block(self):
        return self.soup.find(id="MainPeopleBK")
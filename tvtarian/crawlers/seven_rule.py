import datetime

from .shared.beautiful_soup import create_soup
from .shared.const import SEVEN_RULE_ID
from .html_crawler import HtmlCrawler


class SevenRule(HtmlCrawler):
    def prepare(self):
        super().prepare()
        self.next_soup = create_soup(self.url() + self.next_onair_page_url())

    def url(self):
        return 'https://www.ktv.jp/7rules/'

    def id(self):
        return SEVEN_RULE_ID

    def title(self):
        return self.soup.title.text

    def date(self):
        return datetime.date(
            int('20' + self.next_onair_page_url()[8:10]), int(self.next_onair_page_url()[10:12]),
            int(self.next_onair_page_url()[12:14]))

    def name(self):
        job = self.block().find('h3').text
        name = self.block().find('span', class_='name').text
        profile = self.block().find('span', class_='profile').text
        return f"{name}({job}): {profile}"

    def description(self):
        return self.block().find_all('p')[-1].text

    def next_onair_page_url(self):
        return self.soup.find(
            'section', class_='conts-box program').h1.a['href']

    def block(self):
        return self.next_soup.find('div', class_='parsys contents_parsys')

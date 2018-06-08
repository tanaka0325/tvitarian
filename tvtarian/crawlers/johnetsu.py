import datetime
import re
from .shared.beautiful_soup import create_soup
from .shared.const import JOHNETSU_ID


class Johnetsu:
    url = 'https://www.mbs.jp/jounetsu/'

    def crawl(self):
        soup = create_soup(self.url)

        block = soup.find(id="MainPeopleBK")
        d = block.find(id="PeopleDate")
        title = soup.title.text

        date_str = d.text.splitlines()[1].strip()
        date_list = re.split('[年月日]', date_str)
        date = datetime.date(
            int(date_list[0]), int(date_list[1]), int(date_list[2]))

        name = block.find(id="profile").find(class_="name").text
        description = block.find(class_="catch").text

        return (JOHNETSU_ID, title, date, name, description)

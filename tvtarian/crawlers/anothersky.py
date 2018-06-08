import datetime

from .shared.beautiful_soup import create_soup
from .shared.const import ANOTHER_SKY_ID


class Anothersky:
    url = 'http://www.ntv.co.jp/anothersky/'

    def crawl(self):
        soup = create_soup(self.url)

        block = soup.find(id="nextGuest").p.text
        title = soup.title.text

        date_str = block.splitlines()[0][5:].split('.')
        date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))

        name = block.splitlines()[2]
        description = "".join(block.splitlines())

        return (ANOTHER_SKY_ID, title, date, name, description)

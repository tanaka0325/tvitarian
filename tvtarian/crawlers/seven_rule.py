import datetime

from .shared.beautiful_soup import create_soup
from .shared.const import SEVEN_RULE_ID


class SevenRule:
    url = 'https://www.ktv.jp/7rules/'

    def crawl(self):
        index_soup = create_soup(self.url)
        next_onair_page_url = index_soup.find(
            'section', class_='conts-box program').h1.a['href']

        soup = create_soup(self.url + next_onair_page_url)
        block = soup.find('div', class_='parsys contents_parsys')
        title = index_soup.title.text
        date = datetime.date(
            int('20' + next_onair_page_url[8:10]), int(next_onair_page_url[10:12]),
            int(next_onair_page_url[12:14]))
        job = block.find('h3').text
        name = block.find('span', class_='name').text
        profile = block.find('span', class_='profile').text
        description = block.find_all('p')[-1].text

        return (SEVEN_RULE_ID, title, date, f"{name}({job}): {profile}",
                description)

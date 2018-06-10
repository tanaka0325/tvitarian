import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .shared.const import MUSIC_STATION_ID
from .js_crawler import JsCrawler


class MusicStation(JsCrawler):
    def url(self):
        return 'http://www.tv-asahi.co.jp/music'

    def id(self):
        return MUSIC_STATION_ID

    def title(self):
        return self.driver.title

    def date(self):
        date_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body//*[@id='title_date_lineup']")))
        l = date_element.text.split(".FRI")[0].split('.')
        return datetime.date(int(l[0]), int(l[1]), int(l[2]))

    def name(self):
        name_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@id='artists_info_lineup']")))
        elements = name_element.find_elements_by_xpath(".//li")
        artists_and_songs = list(map(lambda e: e.text.replace("\n", "(") + ")", elements))
        return ", ".join(artists_and_songs)

    def description(self):
        return 'なし'


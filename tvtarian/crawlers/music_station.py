import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .shared.const import MUSIC_STATION_ID
from .shared.selenium import create_chrome_driver


class MusicStation:
    url = 'http://www.tv-asahi.co.jp/music'

    def crawl(self):
        driver = create_chrome_driver()
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)

        title = driver.title

        date_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body//*[@id='title_date_lineup']")))
        l = date_element.text.split(".FRI")[0].split('.')
        date = datetime.date(int(l[0]), int(l[1]), int(l[2]))

        name_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@id='artists_info_lineup']")))
        elements = name_element.find_elements_by_xpath(".//li")
        artists_and_songs = list(map(lambda e: e.text.replace("\n", "(") + ")", elements))
        name = ", ".join(artists_and_songs)

        return (MUSIC_STATION_ID, title, date, name, "なし")

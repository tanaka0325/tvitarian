import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .shared.const import PROFESSIONAL_ID
from .shared.selenium import create_chrome_driver


class Professional:
    url = 'http://www4.nhk.or.jp/professional/'

    def crawl(self):
        driver = create_chrome_driver()
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)

        title = driver.title

        date_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body//*[@id='ProgramContents']//time")))
        l = date_element.get_attribute('datetime').split('-')
        date = datetime.date(int(l[0]), int(l[1]), int(l[2]))

        name_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@id='ProgramContents']//p[@class='appear']")))
        name = re.search("】(.+),【", name_element.text).group(1)

        desc_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@class='program-description col-4']/p[1]")))
        description = desc_element.text

        return (PROFESSIONAL_ID, title, date, name, description)

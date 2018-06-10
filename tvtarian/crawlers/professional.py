import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .js_crawler import JsCrawler
from .shared.const import PROFESSIONAL_ID


class Professional(JsCrawler):
    def url(self):
        return 'http://www4.nhk.or.jp/professional/'

    def id(self):
        return PROFESSIONAL_ID

    def title(self):
        return self.driver.title

    def date(self):
        date_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body//*[@id='ProgramContents']//time")))
        l = date_element.get_attribute('datetime').split('-')
        return datetime.date(int(l[0]), int(l[1]), int(l[2]))

    def name(self):
        name_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@id='ProgramContents']//p[@class='appear']")))
        return re.search("】(.+),【", name_element.text).group(1)

    def description(self):
        desc_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body//*[@class='program-description col-4']/p[1]")))
        return desc_element.text

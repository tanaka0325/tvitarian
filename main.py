import datetime
import os
import re
import textwrap
import time
from collections import namedtuple
import redis
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# constants
ANOTHER_SKY_ID = 1
JOHNETSU_ID = 2
PROFESSIONAL_ID = 3
SEVEN_RULE_ID = 4

# namedtuples
Program = namedtuple('Program', 'id title date name description')


def main():
    programs = Program._make(get_anothersky()), Program._make(
        get_johnetsu()), Program._make(get_professional()), Program._make(
            get_seven_rule())

    conn = connect_redis()
    for program in programs:
        notify(program, conn)


def get_anothersky():
    url = 'http://www.ntv.co.jp/anothersky/'
    soup = create_soup(url)

    block = soup.find(id="nextGuest").p.text
    title = soup.title.text

    date_str = block.splitlines()[0][5:].split('.')
    date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    name = block.splitlines()[2]
    description = "".join(block.splitlines())

    return (ANOTHER_SKY_ID, title, date, name, description)


def get_johnetsu():
    url = 'https://www.mbs.jp/jounetsu/'
    soup = create_soup(url)

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


def get_professional():
    url = 'http://www4.nhk.or.jp/professional/'
    driver = create_chrome_driver()
    driver.get(url)
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


def get_seven_rule():
    index_url = 'https://www.ktv.jp/7rules/'
    index_soup = create_soup(index_url)
    next_onair_page_url = index_soup.find(
        'section', class_='conts-box program').h1.a['href']

    soup = create_soup(index_url + next_onair_page_url)
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


def create_chrome_driver():
    options = ChromeOptions()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return Chrome(options=options)


def create_soup(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    return BeautifulSoup(r.text, "html.parser")


def connect_redis():
    return redis.from_url(os.environ.get("REDIS_URL"))


def isUpdated(program, conn):
    notified_date_bytes = conn.get(program.id)
    if notified_date_bytes is None:
        return True

    l = notified_date_bytes.decode('utf-8').split('-')
    notified_date = datetime.date(int(l[0]), int(l[1]), int(l[2]))

    if notified_date < program.date:
        return True
    else:
        return False


def update_notify_date(program, conn):
    conn.set(program.id, program.date)


def notify(program, conn):
    if isUpdated(program, conn):
        print(program)
        notify_to_line(program)
        update_notify_date(program, conn)
    else:
        print('no update')


def format_message(title, date, name, description):
    template = textwrap.dedent("""番組名: {title}
        次回放送: {date}
        ゲスト: {name}
        番組説明: {description}
    """)
    return template.format(
        title=title, date=date, name=name, description=description)


def notify_to_line(program):
    token = os.environ.get('LINE_TOKEN')
    if token is None:
        print('no token')
        return

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer {}".format(token)}
    message = format_message(program.title, program.date, program.name,
                             program.description)
    payload = {"message": message}

    r = requests.post(url, headers=headers, data=payload)


if __name__ == '__main__':
    main()

import datetime
import os
import re
import textwrap
from collections import namedtuple
import redis
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

# constants
ANOTHER_SKY_ID = 1
JOHNETSU_ID = 2
PROFESSIONAL_ID = 3

# namedtuples
Program = namedtuple('Program', 'id title date name description')


def main():
    programs = Program._make(get_anothersky()), Program._make(
        get_johnetsu()), Program._make(get_professional())

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
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    block = soup.find(id="ProgramContents")
    title = soup.title.text

    date_str = block.find("time")['datetime']
    date_list = date_str.split('-')
    date = datetime.date(
        int(date_list[0]), int(date_list[1]), int(date_list[2]))

    description_block = block.find(class_="program-description")
    description = description_block.p.get_text()

    name_str = description_block.find(class_="appear").get_text()
    name = re.search("】(.+),【", name_str).group(1)

    return (PROFESSIONAL_ID, title, date, name, description)


def create_chrome_driver():
    options = ChromeOptions()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
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
        notify_to_line(program)
        print(program)
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

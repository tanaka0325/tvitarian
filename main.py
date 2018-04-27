import os
import textwrap
from collections import namedtuple
import requests
from bs4 import BeautifulSoup


def main():
    Program = namedtuple('Program', 'title datetime name description')

    anothersky = Program._make(get_anothersky())
    johnetsu = Program._make(get_johnetsu())
    professional = Program._make(get_professional())

    notify_to_line(anothersky)


def get_anothersky():
    url = 'http://www.ntv.co.jp/anothersky/'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    block = soup.find(id="nextGuest").p.text
    title = soup.title.text
    datetime = block.splitlines()[0] + ' ' + block.splitlines()[1]
    name = block.splitlines()[2]
    description = "".join(block.splitlines())

    return (title, datetime[5:-5], name, description)


def get_johnetsu():
    url = 'https://www.mbs.jp/jounetsu/'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    block = soup.find(id="MainPeopleBK")
    d = block.find(id="PeopleDate")
    title = soup.title.text
    date = d.text.splitlines()[1].strip()
    time = d.script.text.splitlines()[2].strip()[-5:-1]
    name = block.find(id="profile").find(class_="name").text
    description = block.find(class_="catch").text

    return (title, date + time, name, description)


def get_professional():
    url = 'http://www4.nhk.or.jp/professional/'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    block = soup.find(id="free1")
    title = block.find(class_="title").text
    date = block.find(class_="date").text[:-2]
    time = soup.find(class_="header-schedule").text.strip()[8:16]
    name = title  # TODO
    description = block.p.text

    return (title, date + time, name, description)


def notify_to_line(program):
    token = os.environ.get('LINE_TOKEN')
    if token is None:
        print('no token')
        return

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer {}".format(token)}
    message = textwrap.dedent("""
        番組名: {title}
        次回放送: {datetime}
        ゲスト: {name}
        番組説明: {description}
    """)
    payload = {
        "message":
        message.format(
            title=program.title,
            datetime=program.datetime,
            name=program.name,
            description=program.description)
    }

    r = requests.post(url, headers=headers, data=payload)


if __name__ == '__main__':
    main()

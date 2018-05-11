import os
import textwrap
from collections import namedtuple
import requests
from bs4 import BeautifulSoup


def main():
    Program = namedtuple('Program', 'title date name description')

    anothersky = Program._make(get_anothersky())
    johnetsu = Program._make(get_johnetsu())
    professional = Program._make(get_professional())

    notify_to_line(anothersky)


def get_anothersky():
    url = 'http://www.ntv.co.jp/anothersky/'
    soup = create_soup(url)

    block = soup.find(id="nextGuest").p.text
    title = soup.title.text
    date = block.splitlines()[0]
    name = block.splitlines()[2]
    description = "".join(block.splitlines())

    return (title, date[5:], name, description)


def get_johnetsu():
    url = 'https://www.mbs.jp/jounetsu/'
    soup = create_soup(url)

    block = soup.find(id="MainPeopleBK")
    d = block.find(id="PeopleDate")
    title = soup.title.text
    date = d.text.splitlines()[1].strip()
    name = block.find(id="profile").find(class_="name").text
    description = block.find(class_="catch").text

    return (title, date, name, description)


def get_professional():
    url = 'http://www4.nhk.or.jp/professional/'
    soup = create_soup(url)

    block = soup.find(id="free1")
    title = soup.title.text
    date = block.find(class_="date").text[:-2]
    name = block.find(class_="title").text  # TODO
    description = block.p.text

    return (title, date, name, description)


def create_soup(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    return BeautifulSoup(r.text, "html.parser")


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

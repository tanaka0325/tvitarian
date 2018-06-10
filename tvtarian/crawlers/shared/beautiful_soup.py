import requests
from bs4 import BeautifulSoup


def create_soup(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    return BeautifulSoup(r.text, "html.parser")

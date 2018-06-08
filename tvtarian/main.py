from collections import namedtuple

from crawlers.anothersky import Anothersky
from crawlers.johnetsu import Johnetsu
from crawlers.music_station import MusicStation
from crawlers.professional import Professional
from crawlers.seven_rule import SevenRule
from datastore.redis import Redis as Datastore
from notifier.line import Line as Notifier


# namedtuples
Program = namedtuple('Program', 'id title date name description')

crawlers = [
    Anothersky(),
    Johnetsu(),
    MusicStation(),
    Professional(),
    SevenRule()
]


def main():
    for crawler in crawlers:
        program = Program._make(crawler.crawl())
        notifier = Notifier(Datastore())
        notifier.notify(program)


if __name__ == '__main__':
    main()

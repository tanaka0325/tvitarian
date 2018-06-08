from .shared.beautiful_soup import create_soup

class Crawler:
    def crawl(self):
        page = self.prepare()
        return self.id(), self.title(page), self.date(page), self.name(page), self.description(page)

    def prepare(self):
        return create_soup(self.url)

    def url(self):
        pass
    
    def id(self):
        pass

    def title(self, page):
        pass

    def date(self, page):
        pass

    def name(self, page):
        pass

    def description(self, page):
        pass
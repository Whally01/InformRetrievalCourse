import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.items import BookItem, BooksItemLoader
import pymorphy2
import os.path


class BooksSpider(CrawlSpider):
    name = "books_spider"
    allowed_domains = ['briefly.ru']
    start_urls = ['https://briefly.ru/new', 'https://briefly.ru/nonfiction']
    globvar = 1
    save_path = '/home/dr/PycharmProjects/inform_retrive/scraper/files/'
    morph = pymorphy2.MorphAnalyzer()

    # custom_settings = {
    #     'DEPTH_LIMIT': 1
    # }

    rules = (
        Rule(LinkExtractor(allow=(r'https://briefly.ru/\w+/\w+'),
                           restrict_xpaths=('//div[@class="grid"]',)),
             callback="parse_item",
             # follow=True
             ),
    )

    def parse_item(self, response):
        print('Processing..' + response.url)
        selector = Selector(response)
        loader = BooksItemLoader(BookItem(), selector)
        loader.add_value('url', response.url)
        self.globvar = self.globvar + 1

        if selector.xpath('//h1[@id="title"]') is not None:
            f = selector.xpath('//h1[@id="title"]/text()').extract_first()
            filename = os.path.join(self.save_path, f)
            print(filename)

        elif selector.xpath('//h1[@id="title"]/span'):
            f = selector.xpath('//h1[@id="title"]/span/text()').extract_all()
            filename = os.path.join(self.save_path, f)
            print(filename)
        else:
            filename = 'file %d' % self.globvar
            filename = os.path.join(self.save_path, filename)

        # loader.add_xpath('text', '//div[@id="text"]/p')

        with open(filename + ".txt", 'w') as f:
            for item in selector.xpath('//div[@id="text"]/p/text()').extract():
                f.write("%s\n" % item)

        with open("index.txt", 'a') as f:
            f.write("%s) %s : %s \n" % (self.globvar, filename, response.url))

        self.log('Saved file:  %s' % filename.upper())
        self.log('Count: %d' % self.globvar)

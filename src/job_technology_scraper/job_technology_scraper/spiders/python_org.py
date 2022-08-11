import scrapy


class PythonOrgSpider(scrapy.Spider):
    name = 'python_org'
    allowed_domains = ['python.org']
    start_urls = ['https://python.org/']

    def parse(self, response):
        pass

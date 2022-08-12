import scrapy
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup as BS


class PythonOrgSpider(scrapy.Spider):
    name = 'python_org'
    allowed_domains = ['python.org']
    start_urls = ['https://python.org/jobs']
    job_page_urls: list[str] = []


    def extract_job_data(self, response: HtmlResponse):
        '''
        Feature extraction method for the individual job pages.'''

        # TODO: Add job page scraping with quick cleaning.


    def parse(self, response: HtmlResponse):
        # Extracting and returning all job links. 
        job_list = response.css('ol').get()
        job_soup = BS(job_list, 'html.parser')
        job_cells = job_soup.find_all('li')
        job_urls = [job.find('a')['href'] for job in job_cells]
        self.job_page_urls.extend(job_urls)

        # Going to the next page and repeating the process.
        next_page: str|None = response.css('section ul li.next a')[0].attrib['href']
        if next_page is not None or next_page != '':
            next_page_url = self.start_urls[0] + next_page
            yield response.follow(next_page_url, callback=self.parse)
        else:
            # Requesting each individual job page when no are more job list pages.
            for url in self.job_page_urls:
                yield scrapy.Request(url, callback=self.extract_job_data)

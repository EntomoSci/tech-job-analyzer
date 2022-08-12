import scrapy
from scrapy.http import HtmlResponse
from job_technology_scraper.items import PythonJobItem
from bs4 import BeautifulSoup as BS


class PythonOrgSpider(scrapy.Spider):
    name = 'python_org'
    allowed_domains = ['python.org']
    start_urls = ['https://python.org/jobs']
    job_page_urls: list[str] = []


    def _get_title_and_content(self, section: str) -> tuple[str,str]:
        '''
        Return raw title and content separately from section.'''

        title, content = section.split('</h2>')
        data = title.strip(), content.strip()

        return data


    def extract_job_data(self, response: HtmlResponse):
        '''
        Job feature extraction method for the individual job pages.'''

        # Extracting parent section containing all features.
        job_page = response.css('section').get()
        page_soup = BS(job_page, 'html.parser')
        sections: list[str] = str(page_soup.find('article')\
                                           .find('div'))\
                                           .split('<h2>')[1:]

        # Extracting separate data for all sections.
        data: list[tuple[str,str]] = [self._get_title_and_content(section) for section in sections]
        
        # Filling each feature variable to its correponding content by checking their title.
        job_item_dict = {}
        for sample in data:
            sample: tuple[str,str]
            match sample[0].lower():
                case 'job title':
                   job_item_dict['job_title'] = sample[1]
                case 'job description':
                   job_item_dict['job_description'] = sample[1]
                case 'restrictions':
                   job_item_dict['job_restrictions'] = sample[1]
                case 'requirements':
                   job_item_dict['job_requirements'] = sample[1]
                case 'about the company':
                   job_item_dict['company_about'] = sample[1]
                case 'contact info':
                   job_item_dict['contact_info'] = sample[1]

        return PythonJobItem(job_item_dict)


    def parse(self, response: HtmlResponse):
        # Extracting and returning all job links. 
        job_list = response.css('ol').get()
        job_soup = BS(job_list, 'html.parser')
        job_cells = job_soup.find_all('li')
        job_urls = [job.find('a')['href'] for job in job_cells]
        self.job_page_urls.extend(job_urls)

        # Going to the next page and repeating the process.
        next_page: str|None = response.css('section ul li.next a')[0].attrib['href']
        if next_page != '':  # CONDITIONAL DISABLED: "next_page is not"
            next_page_url = self.start_urls[0] + next_page
            yield response.follow(next_page_url, callback=self.parse)
        else:  # Requesting each individual job page when are no more job list pages.
            for url in self.job_page_urls:
                yield scrapy.Request(self.start_urls[0] + url.removeprefix('/jobs'), callback=self.extract_job_data)

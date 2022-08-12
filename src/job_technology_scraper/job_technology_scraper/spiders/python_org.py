import scrapy
from scrapy.http import HtmlResponse
from job_technology_scraper.items import PythonJob
from bs4 import BeautifulSoup as BS


class PythonOrgSpider(scrapy.Spider):
    name = 'python_org'
    allowed_domains = ['python.org']
    start_urls = ['https://python.org/jobs']
    job_page_urls: list[str] = []


    def _get_title_and_content(section: str) -> tuple[str,str]:
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
        _, job_title = data[0]
        _, job_description = data[1]
        _, job_restrictions = data[2]
        _, job_requirements = data[3]
        _, company_about = data[4]
        _, contact_info = data[5]

        # Yielding the raw data for each job feature.
        yield PythonJob(
            job_title=job_title,
            job_description=job_description,
            job_restrictions=job_restrictions,
            job_requirements=job_requirements,
            company_about=company_about,
            contact_info=contact_info
            )


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

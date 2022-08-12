# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from bs4 import BeautifulSoup as BS
from itemadapter import ItemAdapter
from job_technology_scraper.items import PythonJobItem


class PythonJobPipeline:
    '''
    Class to do data preparation on PythonJob objects.'''

    def process_item(self, item: PythonJobItem, spider):
        # NOTE: job_title is comes already cleaned.
        # Processing job_description.
        clean_description: str = BS(item['job_description'], 'html.parser').text.replace('\n', ' ').strip()
        # Processing job_restrictions:
        clean_restrictions: str = BS(item['job_restrictions', 'html.parser']).text.replace('\n', ' ').strip()
        # Processing job_requirements:
        reqs_soup = BS(item['job_requirements'], 'html.parser')
        reqs_lists = reqs_soup.find_all('ul')
        reqs1 = [req.text for req in reqs_soup.find_all('p')]
        reqs2 = [req.text for req in reqs_lists[0] + reqs_lists[1]]
        clean_requirements: list[str] = reqs1 + reqs2
        # TODO: Processing company_about:
        # TODO: Processing contact_info:


class JobTechnologyScraperPipeline:
    def process_item(self, item, spider):
        return item

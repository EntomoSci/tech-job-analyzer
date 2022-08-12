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


    def _extract_paragraphs_and_list_items(self, section: str) -> list[str]:
        '''
        Return a list with the content of all paragraph and list item tags in section.'''

        soup = BS(section, 'html.parser')

        # Extracting and concatenating all lists into a single one.
        lists = soup.find_all('ul')
        lists_joined = []
        for i in range(len(lists)):
            lists_joined.extend(lists[i])

        paragraph_content = [p.text for p in lists.find_all('p')]
        lists_content = [li.text for li in lists_joined]
        full_data: list[str] = paragraph_content + lists_content

        return full_data


    def process_item(self, item: PythonJobItem, spider):
        # NOTE: job_title is comes already cleaned.

        # Processing job_description.
        clean_description: str = BS(item['job_description'], 'html.parser').text.replace('\n', ' ').strip()

        # Processing job_restrictions:
        clean_restrictions: str = BS(item['job_restrictions', 'html.parser']).text.replace('\n', ' ').strip()

        # Processing job_requirements:
        clean_requirements: list[str] = self._extract_paragraphs_and_list_items(item['job_requirements'])
        # TODO: Processing company_about:
        # TODO: Processing contact_info:


class JobTechnologyScraperPipeline:
    def process_item(self, item, spider):
        return item

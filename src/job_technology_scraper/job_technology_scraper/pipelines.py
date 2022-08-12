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

        # Extracting and concatenating all lists into a single one.
        soup = BS(section, 'html.parser')
        lists = soup.find_all('ul')
        lists_joined = []
        for i in range(len(lists)):
            lists_joined.extend(lists[i])

        # Extracting and joining all text content of <p> and <li> tags.
        paragraph_content = [p.text for p in soup.find_all('p')]
        lists_content = [li.text for li in lists_joined]
        full_data: list[str] = paragraph_content + lists_content

        return full_data


    def process_item(self, item: PythonJobItem, spider):
        adapter = ItemAdapter(item)

        # Processing all item's features.
        # NOTE: job_title comes already cleaned.
        clean_description: str = BS(item['job_description'], 'html.parser').text.replace('\n', ' ').strip()
        clean_restrictions: str = BS(item['job_restrictions'], 'html.parser').text.replace('\n', ' ').strip()
        clean_requirements: list[str] = [x for x in self._extract_paragraphs_and_list_items(item['job_requirements']) if not x.isspace()]
        clean_company_about: list[str] = [x for x in self._extract_paragraphs_and_list_items(item['company_about']) if not x.isspace()]
        clean_contact_info: list[str] = [x.text for x in BS(item['contact_info'], 'html.parser').find_all('li') if not x.text.isspace()]

        # Settings the new cleaned features back to the item.
        adapter['job_description'] = clean_description
        adapter['job_restrictions'] = clean_restrictions
        adapter['job_requirements'] = clean_requirements
        adapter['company_about'] = clean_company_about
        adapter['contact_info'] = clean_contact_info

        return item

    
class JobTechnologyScraperPipeline:
    def process_item(self, item, spider):
        return item

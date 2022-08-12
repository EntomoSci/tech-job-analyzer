# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class PythonJob(Item):
    '''
    Class that represent a Python job from python.org.'''

    job_title = Field()
    job_description = Field()
    job_restrictions = Field()
    job_requirements = Field()
    company_about = Field()
    contact_info = Field()


class JobTechnologyScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

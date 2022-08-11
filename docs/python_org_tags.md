# Python.org tags

By: smv7\
Creation: 2022/11/8 3:12\
Last update: 2022/11/8 3:12

## Abstract
In this document I show you how to locate the HTML tags of the website https://www.python.org/jobs/ that contains the data of Python jobs, used by `src.job_technology_scraper.job_technology_scraper.spiders.python_org.py` spider to retrieve that data back to us.

## Features

The features scraped from the site are listed below, with some additional notes associated to some of them:
1. `job_title`
2. `post_date`
3. `tags`: Used to enhance definition of learning goals.
4. `is_remote`
5. `country`
6. `description`: Will be summarized with *wordclouds*.
7. `requirements`: **Learning goals** (technologies we need to know to apply).

**NOTE**: Before diving into the examples, they assume the following facts:
1. A `response` variable containing a *scrapy response* retrieved from https://www.python.org/jobs/ is available.
2. `bs4.BeautifulSoup` is imported as `BS`.
```py
# Extracting job_title:
job_list = response.css('ol')
job_soup = BS(job_list.get(), 'html.parser')
titles_list = job_soup.find_all('li')
job_titles: list[str] = [titles_list[i].find('a').text for i in range(len(titles_list))]
```

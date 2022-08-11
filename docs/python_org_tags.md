# Python.org tags

By: smv7\
Creation: 2022/11/8 3:12\
Last update: 2022/11/8 3:12

## Abstract
In this document I show you how to locate the HTML tags of the website https://www.python.org/jobs/ that contains the data of Python jobs, used by `src.job_technology_scraper.job_technology_scraper.spiders.python_org.py` spider to retrieve the data of each individual job back to us.

## Approach
1. Get links of each individual job page from https://www.python.org/jobs/.
2. Get all variables listed below for each job from its individual pages.

Before diving into the examples, they assume the following facts:
1. A `response` variable containing a *scrapy response* retrieved from a request send to the corresponding website (relative to the section where is written) is available.
2. `bs4.BeautifulSoup` is imported as `BS`.

## Extracting jobs page links
```py
job_list = response.css('ol').get()
job_soup = BS(job_list, 'html.parser')
job_cells = job_soup.find_all('li')
job_urls = [job.find('a')['href'] for job in job_cells]
```

## Extracting job features from each job page

The features scraped from the site are listed below, with some additional notes associated to some of them:
1. `job_title`
2. `location`
3. `post_date`
3. `tags`: Used to enhance definition of learning goals.
4. `is_remote`
5. `country`
6. `description`: Will be summarized with *wordclouds*.
7. `requirements`: **Learning goals** (technologies we need to know to apply).

```py
# Extracting job_title:

# Extracting location:

# Extracting post_date:

# Extracting tags:

# Extracting is_remote:

# Extracting country:

# Extracting description:

# Extracting requirements:

```

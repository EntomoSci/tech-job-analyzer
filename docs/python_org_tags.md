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

The features scraped from the site are listed below, with the first 6 in the same order that appear in the its job page (some additional notes associated to some of them are written):
1. `job_title`
2. `description`: Will be summarized with *wordclouds*.
3. `restrictions`
4. `requirements`: **Learning goals** (technologies we need to know to apply).
5. `company_about`
6. `contact_info`

These features will be added after:

7. `post_date`
8. `location`
9. `tags`: Used to enhance definition of learning goals.
10. `is_remote`
11. `country`

```py
# Extracting parent section containing all features.
# NOTE: The 0 index element is a useless remaning piece of
# HTML that is inevitably collected with the approach used,
# thats why is excluded. The preserved items contains the
# HTML of each section listed above in the same order, so
# first item at index 0 contains the data of 'job_title', 
# at index 1 of 'description' and so on.
sections: list[str] = str(page_soup.find('article')\
                      .find('div'))\
                      .split('<h2>')[1:]
```

## Data preparations for all raw HTML sections
The *hacky* method to cut the HTML and get each feature section separately by spliting the code in `<h2>`, returns each section with a `</h2>` that can be used to separate the title of the section from its content. So we've convenient to write a function to do that for all sections.

**Note**: The dummy variables `_` receive the titles of the sections that can be used to ensure that the data goes to the correct variables. If the structure of job page varies from job to job, you must consider using these variables.
```py
# Function to separate each section title from its content.
def get_title_and_content(section: str) -> tuple[str,str]:
    '''
    Return raw title and content separately from section.'''

    title, content = section.split('</h2>')
    data = title.strip(), content.strip()

    return data

# Extracting separate data for all sections.
data: list[tuple[str,str]] = [get_title_and_content(section) for section in sections]

# Extracting job_title:
_, job_title = data[0]

# Extracting job_description:
_, job_description = data[1]

# Extracting job_restrictions:
_, job_restrictions = data[2]

# Extracting job_requirements:
_, job_requirements = data[3]

# Extracting company_about:
_, company_about = data[4]

# Extracting contact_info:
_, contact_info = data[5]

# These features will be defined later.
# Extracting location:
# Extracting post_date:
# Extracting tags:
# Extracting is_remote:
# Extracting country:
# Extracting description:
```

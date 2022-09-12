#!/usr/bin/env python
# coding: utf-8


# In[1]:

import pymongo
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Import Dependencies
import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# In[4]:


# Visit Nasa News url  using splinter module
Nasa_url = 'https://mars.nasa.gov/news/'
browser.visit(Nasa_url)

time.sleep(1)

# create HTMl Object
html = browser.html

# parse HTML with beautiful soup
Nasa_soup = bs(html, 'html.parser')

# Extract title text
nasa_news_title = Nasa_soup.find('div', class_='list_text').find('a').text
print(nasa_news_title)

# Extract Paragraph text
nasa_news_paragraph = Nasa_soup.find('div', class_='article_teaser_body').text
print(nasa_news_paragraph)


# In[5]:


news_title = "NASA's Perseverance Makes New Discoveries in Mars' Jezero Crater"
news_p = "The rover found that Jezero Crater’s floor is made up of volcanic rocks that have interacted with water"


# ### JPL Mars Space Images—Featured Image

# In[6]:


# Visit Nasa's JPL Mars Space url  using splinter module
jplNasa_url = 'https://spaceimages-mars.com'
browser.visit(jplNasa_url)

time.sleep(1)

# get base Nasa link
main_url = 'https://spaceimages-mars.com'

# get to image
image_url = browser.find_by_tag('button')[1]

image_url.click()


# In[7]:


html = browser.html
soup = bs(html, 'html.parser')

space_url = soup.find('img', class_='fancybox-image').get('src')
print(space_url)


# In[8]:


featured_image_url = jplNasa_url+'/'+space_url
featured_image_url


# In[9]:


featured_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'


# ### Mars Facts

# In[10]:


# mars facts Url link
mars_url = 'https://galaxyfacts-mars.com'

# find the table of mars facts
table = pd.read_html(mars_url)
table


# In[11]:


# get the fist table
facts_table = table[0]

# set table header and index
facts_table.columns = facts_table.iloc[0]
facts_table = facts_table.iloc[1:, :]
facts_table.set_index('Mars - Earth Comparison', inplace=True)
facts_table


# In[12]:


facts_table_html = facts_table.to_html()


# ### Mars Hemispheres

# In[13]:


# Visit the USGS Astrogeology site
USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
short_url = "https://astrogeology.usgs.gov"


# In[14]:


browser.visit(USGS_url)

time.sleep(1)

html = browser.html
soup = bs(html, 'html.parser')
main_url = soup.find_all('div', class_='item')
titles = []
hemisphere_img_urls = []

for x in main_url:

    title = x.find('h3').text
    url = x.find('a')['href']
    hem_img_url = short_url+url

    # print(hem_img_url)
    browser.visit(hem_img_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_img_original = soup.find('div', class_='downloads')
    hemisphere_img_url = hemisphere_img_original.find('a')['href']

    print(hemisphere_img_url)
    img_data = dict({'title': title, 'img_url': hemisphere_img_url})
    hemisphere_img_urls.append(img_data)

browser.quit()

# In[15]:


def scrape_info():
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'facts_table': facts_table_html,
        'hemisphere_image_urls': hemisphere_img_urls
    }
    return mars_data


client = pymongo.MongoClient("mongodb://localhost:27017")

db = client.mars_db
collection = db.mars_data
collection.delete_many({})

collection.insert_many(
    [
        {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'facts_table': facts_table_html,
            'hemisphere_image_urls': hemisphere_img_urls
        }
    ]
)

import pandas as pd
import numpy as np
import requests
from requests import get
import re
from bs4 import BeautifulSoup



def get_codeup_articles(blog):
    '''
    This function takes in a Codeup blog url and returns a dictionary of its title 
    and contents.
    '''
    response = requests.get(blog, headers={'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    title = soup.select('title')[0].text
    content = ' '.join([soup('p')[i].text for i in range(0, len(soup('p')))])
    return {
        'title': title,
        'content': content
    }

def get_blog_articles():
    '''
    This function returns a dataframe of the titles and contents of all blog posts
    linked on Codeup's blog page.
    '''
    soup = BeautifulSoup(requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'}).text)
    blog_urls = [soup.select('.more-link')[i]['href'] for i in range(0,len(soup.select('.more-link')))]
    return pd.DataFrame([get_codeup_articles(blog) for blog in blog_urls])

def get_news_card(card):
    '''
    This function returns a dictionary of relevant information from a news card
    found at inshorts.com.
    '''
    card_title = card.select_one('.news-card-title')
    title = card.find('span', itemprop = 'headline').text
    author = card.find('span', class_ = 'author').text
    content = card.find('div', itemprop = 'articleBody').text
    date = card.find('span', clas ='date').text
    return {
        'title': title,
        'date': date,
        'content': content,
        'author': author
    }

def get_inshorts_page(url):
    '''
    This function returns a dataframe where each row is a news article from 
    a page on inshorts.com.
    '''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    articles = pd.DataFrame([get_news_card(card) for card in cards])
    articles['category'] = category
    return articles

def get_inshorts_articles():
    '''
    This function returns a dataframe of news articles from the business, sports, 
    technology, and entertainment sections of inshorts.com.
    '''
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(get_inshorts_page(url + cat))])
    df = df.reset_index(drop=True)
    return df
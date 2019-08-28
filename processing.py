# AUR NEWS TICKER - Ben Laufer, 10 Jul 2017
# RSS Feed Filter

import feedparser
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import webbrowser
import string
import time
import uuid
from project_util import translate_html


headers = {'User-Agent': 'Chrome/41.0.2228.0 Safari/537.3'}

def process(url, searchword):
    """
    converts url to text and checks for matches with word. returns count of matches
    """

    req_url = url
    print(url)
    word = searchword
    req = Request(url=req_url, headers=headers)
    soup = BeautifulSoup(urlopen(req).read(), 'html.parser')
    for a in soup.findAll('a'):
        del a['href']
    text = soup.get_text()

    text = text.lower()
    word = word.lower()

    i = text.count(word)

    return i

def readUrlConfig(url):
    """
    scans basurl for links, adds valid links to list
    """
    baseurl = url
    req = Request(url=baseurl, headers=headers)
    soup = BeautifulSoup(urlopen(req).read(), 'html.parser')
    urllist = soup.find_all('a')
    urls = []
    for u in urllist:
        try:
            link = u.get('href')
            if "http" in link or "tel:" in link:
                return_url = link
            else:
                return_url = baseurl + link
            urls.append(return_url)
        except:
            continue
    urls = list(set(urls))
    print(urls)
    print(len(urls))
    return urls

#!/usr/bin/python2.7

import scrapy
from ..models import *
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime

"""py -2 -m pwiz -e sqlite "Path/to/db.wordcount" >  models.py"""

class WordSpider(CrawlSpider):
    name = "words"

    start_urls = []

    #TODO allow

    rules = (
        Rule(
            LinkExtractor(
                allow=r'^.*\.mk.*'
            ),
            callback='parse_site',
            follow=True
        ),
    )

    def __init__(self, *a, **kwargs):
        super(WordSpider, self).__init__(*a, **kwargs)
        self.start_urls = []
        for site in MainSite.select():
            self.start_urls.append( site.site )
            #TODO check dates
            site.checked_date = datetime.now()
            site.save()

        q = MainWordsoup.delete()
        q.execute()

        q = MainNamesoup.delete()
        q.execute()

        #for url in self.start_urls:
           # yield scrapy.Request( url=url, callback=self.parse_site )


    def parse_site(self, response):
        from lxml import html
        from nltk.tokenize import word_tokenize
        from nltk import FreqDist

        tree = html.fromstring(response.body.decode("utf-8"))
        html = tree[1]

        url = response.url

        text = ''

        for element in html.iter():
            element = element.findtext("*")
            if element is not None:
                text = text + element.lower().rstrip('\'\"„“-,.:;!?').rstrip('\'\"„“-,.:;!?') + " "

        words = word_tokenize(text)

        dist = FreqDist(words)

        #TODO add new sites to database

        for key, value in dist.items():
            self.addWord(key, value, url)
            self.addName(key, value, url)

    def addWord(self, key, value, url):
        from urllib.parse import urlparse
        try:
            word = MainWord.get( MainWord.word == value )
            url = urlparse( url )
            url = '{uri.scheme}://{uri.netloc}/'.format(uri=url)

            site = MainSite.get( MainSite.site == url )
            # print ("Have come here")
            q = MainWordsoup.get( (MainWordsoup.word == word) & (MainWordsoup.site == site) )
            q.count = q.count + value
            q.save()
            # print ("Saved")
        except MainSite.DoesNotExist:
            print ("Site error ", url)
        except (MainWord.DoesNotExist, MainSite.DoesNotExist):
            print ("Word error ", key)
        except MainWordsoup.DoesNotExist:
            q = MainWordsoup.create(
                word = word,
                site = site,
                count = value
            )
            # print ("Created")

    def addName(self, key, value, url):
        from urllib.parse import urlparse
        try:
            name = MainName.get(MainName.name == key)
            url = urlparse( url )
            url = '{uri.scheme}://{uri.netloc}/'.format(uri=url)

            site = MainSite.get( MainSite.site == url)
            q = MainNamesoup.get( (MainNamesoup.name == name) & (MainNamesoup.site == site) )
            q.count = q.count + value
            q.save()
        except (MainName.DoesNotExist, MainSite.DoesNotExist):
            return
        except MainNamesoup.DoesNotExist:
            q = MainNamesoup.create(
                name = name,
                site = site,
                count = value
            )

process = CrawlerProcess(get_project_settings())

process.crawl(WordSpider)
process.start()
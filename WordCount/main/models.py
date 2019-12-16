from django.db import models

class Word(models.Model):
    word = models.CharField( max_length=200, primary_key=True )
    gender = models.CharField( max_length=1, null=True, blank=True )

    def __str__(self):
        return u'%s %s' % (self.word, self.gender)

    #TODO add tests
    #Test for adding genders
    def start(self, url):
        from lxml import html
        from urllib.parse import urljoin
        import requests

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        page = requests.get( url=url, headers=headers )
        tree = html.fromstring(page.content.decode("utf-8"))

        links = tree.get_element_by_id("letters").iterlinks()

        for link in links:
            url = urljoin(url, link[2])

            page = requests.get(url=url, headers=headers)
            tree = html.fromstring(page.content.decode("utf-8"))

            elements = tree.get_element_by_id("ranges")[0]

            for option in elements:
                url = urljoin(url, option.attrib["value"])

                page = requests.get(url=url, headers=headers)
                tree = html.fromstring(page.content.decode("utf-8"))

                words = tree.get_element_by_id("lexems").iterlinks()

                for word in words:
                    url = urljoin(url, word[2])

                    page = requests.get(url=url, headers=headers)
                    tree = html.fromstring(page.content.decode("utf-8"))

                    lex = tree.xpath('//*[@id="main_content"]/h2/span[1]')[0].text_content()

                    types = None

                    if len(tree.find_class("grammar")) != 0:
                        types = tree.find_class("grammar")[0].text_content().split(':')[1]

                    english = None

                    if len(tree.find_class("eng")) != 0:
                        english = tree.find_class("eng")

                    self.addWords(lex, types.lower(), english)

    def addWords(self, word, types, english):
        types = types.split(',')

        w = Word()
        w.word = word.lower()

        for element in types:
            if "машки род" in element:
                w.gender = 'm'
                types.remove( element )
            elif "женски род" in element:
                w.gender = 'f'
                types.remove( element )
            elif "среден род" in element:
                w.gender = 'n'
                types.remove( element )

        w.save()

        if english is not None:
            for e in english:
                eng = EnglishWord()
                eng.word = w
                eng.english = e.text_content().split()[1].lower()
                eng.save()

        if type is not None:
            for element in types:
                if "свршен" in element and "несвршен" in element:
                    self.addType(w, "свршен")
                    self.addType(w, "несвршен")
                else:
                    self.addType(w, element.strip())

    def addType(self, word, wordtype):
        type = Type()
        type.word = word
        type.word_type = wordtype
        type.save()


class Type(models.Model):
    #id by default
    word = models.ForeignKey( 'Word', on_delete=models.CASCADE)
    word_type = models.CharField( max_length=200 )

    def __str__(self):
        return u'%s %s' % (self.word, self.word_type)

class EnglishWord(models.Model):
    #id by default
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    english = models.CharField(max_length=200)

    def __str__(self):
        return u'%s %s' % (self.word, self.english)

class Name(models.Model):
    name = models.CharField( max_length=200, primary_key=True )
    gender = models.CharField( max_length=1 )

    visited = []

    def __str__(self):
        return u'%s %s' % (self.name, self.gender)

    #TODO test if Зорица is in the database
    def start(self, url):
        self.purgeVisited()
        self.addNames(url)

    def purgeVisited(self):
        self.visited = []

    def addNames(self, url):
        from lxml import html
        from urllib.parse import urljoin
        import requests

        self.visited.append(url)

        page = requests.get( url=url )
        tree = html.fromstring(page.content)

        names = tree.cssselect('body > div.body-wrapper > div > table > tr:nth-child(2) > td:nth-child(1) > div > div')

        i = 0

        #TODO test
        for element in names:
            if i < 5:
                i += 1
                continue
            names = element.text_content().split()
            if "(" in names[1]:
                del names[1]
            name = Name()
            name.name = names[1].lower()
            if "m" in names and "f" in names:
                name.gender = 'u'
            elif "m" in names:
                name.gender = 'm'
            else:
                name.gender = 'f'
            name.save()

        a = tree.xpath('/html/body/div[2]/div/table/tr[2]/td[1]/div/center/a/@href')

        site = urljoin(url, a[0])

        if site in self.visited:
            self.visited = []
            return

        return self.addNames(site)

class Site(models.Model):
    site = models.URLField( primary_key=True )
    checked_date = models.DateTimeField( 'date checked', null=True, blank=True)

    #TODO save

    def __str__(self):
        return u'%s %s' % (self.site, self.checked_date)

class WordSoup(models.Model):
    #id by default
    word = models.ForeignKey( 'Word', on_delete=models.CASCADE )
    site = models.ForeignKey( 'Site', on_delete=models.CASCADE )
    count = models.IntegerField( default=0 )

    def __str__(self):
        return u'%s %s %d' % (self.word.word, self.site.site, self.count)

class NameSoup(models.Model):
    #id by default
    name = models.ForeignKey( 'Name', on_delete=models.CASCADE)
    site = models.ForeignKey( 'Site', on_delete=models.CASCADE)
    count = models.IntegerField( default=0 )

    def __str__(self):
        return u'%s %s %d' % (self.name.name, self.site.site, self.count)
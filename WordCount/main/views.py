from django.db.models.aggregates import Sum
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from requests.exceptions import MissingSchema

from main.models import *

# Create your views here.
def index(request):

    sites = Site.objects.all().values('site')[:17]

    if request.GET.get('q', '') != '':
        if request.GET.get('q', '') not in sites:
            from itertools import chain
            sites = list( chain( sites, Site.objects.filter(site=request.GET.get('q', '') ) ) )

    context = {
        'sites': sites,
    }

    if 'button' in request.POST:
        context['order'] = request.POST['order']
        context['type'] = request.POST['type']
        context['web'] = request.POST['site']

        if 'genderword' in request.POST:
            context['genderword'] = request.POST['genderword']
        if 'gender' in request.POST:
            context['gender'] = request.POST['gender']

        if request.POST['type'] == 'name':
            return Results(
                context,
                request,
                request.POST['order'],
                request.POST['type'],
                request.POST['site'],
                request.POST['gender'])
        if request.POST['type'] == 'именка':
            return Results(
                context,
                request,
                request.POST['order'],
                request.POST['type'],
                request.POST['site'],
                request.POST['genderword'])
        else:
            return Results(context, request, request.POST['order'], request.POST['type'], request.POST['site'])

    return render(request, 'main/index.html', context=context)

def Results(context, request, ordering, type, site, gender=None, url='main/index.html', splice=True):

    order = '-'
    if ordering == 'least':
        order = ''

    try:

        words = None
        if type == 'name':
            words = returnNames(gender, site, order, splice=True)
        else:
            if type == 'именка':
                words = returnWords(site, type, order, gender, splice=True)
            else:
                words = returnWords(site, type, order, splice=True)

        if len(words) == 0:
            words = ['Нема Резултати']

        context['results'] = words

        return render(request, url, context=context)
    except (NameSoup.DoesNotExist, WordSoup.DoesNotExist):
        pass

def moresites( request ):
    sites = Site.objects.all().values('site')

    context = {
        'sites': sites,
    }

    return render(request, 'main/moresites.html', context=context)

def addSite( request ):

    context = {

    }

    if 'submit' in request.POST:
        if len(request.POST) != 0:
            import requests

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            try:

                page = requests.get(url=request.POST['site'], headers=headers)

                if page.status_code == 200:
                    Site.objects.create(site=request.POST['site'])
                else:
                    context['error'] = 1
            except Exception:
                context['error'] = 1

    return render(request, 'main/addSite.html', context)

def returnNames(gender, site, order, splice=True):
    if gender == 'u':
        if site == 'all':
            if splice is not True:
                return NameSoup.objects.filter(name__gender='u').values('name', 'name__gender').annotate(
                    count=Sum('count')).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='u').values('name', 'name__gender').annotate(count = Sum('count') ).order_by(order + 'count')[:17]
        else:
            if splice is not True:
                return NameSoup.objects.filter(name__gender='u', site__site=site).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='u', site__site=site).order_by(order + 'count')[:17]
    elif gender == 'm':
        if site == 'all':
            if splice is not True:
                return NameSoup.objects.filter(name__gender='m').values('name', 'name__gender').annotate(
                    count=Sum('count')).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='m').values('name', 'name__gender').annotate(count = Sum('count') ).order_by(order + 'count')[:17]
        else:
            if splice is not True:
                return NameSoup.objects.filter(name__gender='m', site__site=site).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='m', site__site=site).order_by(order + 'count')[:17]
    else:
        if site == 'all':
            if splice is not True:
                return NameSoup.objects.filter(name__gender='f').values('name', 'name__gender').annotate(
                    count=Sum('count')).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='f').values('name', 'name__gender').annotate(count = Sum('count') ).order_by(order + 'count')[:17]
        else:
            if splice is not True:
                return NameSoup.objects.filter(name__gender='f', site__site=site).order_by(order + 'count')
            return NameSoup.objects.filter(name__gender='f', site__site=site).order_by(order + 'count')[:17]

def returnWords( site, type, order, gender=None, splice=True):
    from django.db import connection
    if gender is not None:
        if gender == 'e':
            if site == 'all':
                if splice is not True:
                    return WordSoup.objects.filter(word__gender__in=['m', 'f', 'n']).values('word', 'word__type',
                                                                                            'word__gender').annotate(
                        count=Sum('count')).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender__in=['m', 'f', 'n']).values('word', 'word__type', 'word__gender').annotate(count = Sum('count') ).order_by(order + 'count')[:17]
            else:
                if splice is not True:
                    return WordSoup.objects.filter(word__gender__in=['m', 'f', 'n'], site__site=site).order_by(
                        order + 'count')
                return WordSoup.objects.filter(word__gender__in=['m', 'f', 'n'], site__site=site).order_by(order + 'count')[:17]
        elif gender == 'm':
            if site == 'all':
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='m').values('word', 'word__type', 'word__gender') \
                               .annotate(count=Sum('count')).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='m').values('word', 'word__type', 'word__gender')\
                           .annotate(count = Sum('count') ).order_by(order + 'count')[:17]
            else:
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='m', site__site=site).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='m', site__site=site).order_by(order + 'count')[:17]
        elif gender == 'f':
            if site == 'all':
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='f').values('word', 'word__type', 'word__gender') \
                               .annotate(count=Sum('count')).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='f').values('word', 'word__type', 'word__gender')\
                           .annotate(count = Sum('count') ).order_by(order + 'count')[:17]
            else:
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='f', site__site=site).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='f', site__site=site).order_by(order + 'count')[:17]
        else:
            if site == 'all':
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='n').values('word', 'word__type', 'word__gender') \
                               .annotate(count=Sum('count')).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='n').values('word', 'word__type', 'word__gender')\
                           .annotate(count = Sum('count')).order_by(order + 'count')[:17]
            else:
                if splice is not True:
                    return WordSoup.objects.filter(word__gender='n', site__site=site).order_by(order + 'count')
                return WordSoup.objects.filter(word__gender='n', site__site=site).order_by(order + 'count')[:17]
    else:
        if site == 'all':
            with connection.cursor() as cursor:
                if order == '-':
                    cursor.execute(
                        "SELECT word_type, SUM(count) FROM main_wordsoup JOIN main_type USING (word_id) GROUP BY word_type ORDER BY count")
                else:
                    cursor.execute(
                        "SELECT word_type, SUM(count) FROM main_wordsoup JOIN main_type USING (word_id) GROUP BY word_type ORDER BY -count")

                if splice is not True:
                    return cursor.fetchall()
                return cursor.fetchall()[:17]
        else:
            with connection.cursor() as cursor:
                if order == '-':
                    cursor.execute(
                        "SELECT word_type, site_id, SUM(count) FROM main_wordsoup JOIN main_type USING (word_id) WHERE site_id=%s GROUP BY word_type ORDER BY -count",
                    [site])
                else:
                    cursor.execute(
                        "SELECT word_type, site_id, SUM(count) FROM main_wordsoup JOIN main_type USING (word_id) WHERE site_id=%s GROUP BY word_type ORDER BY count",
                    [site])

                if splice is not True:
                    return cursor.fetchall()
                return cursor.fetchall()[:17]

def more(request):

    context = {

    }

    context['order'] = request.GET.get('order')
    context['type'] = request.GET.get('type')
    context['web'] = request.GET.get('site')
    context['genderword'] = request.GET.get('genderword')
    context['gender'] = request.GET.get('gender')

    if request.GET.get('type') == 'name':
        return Results(
            context,
            request,
            request.GET.get('order'),
            request.GET.get('type'),
            request.GET.get('web'),
            request.GET.get('gender'),
            url='main/moreresults.html',
            splice=False
        )
    if request.GET.get('type') == 'именка':
        return Results(
            context,
            request,
            request.GET.get('order'),
            request.GET.get('type'),
            request.GET.get('web'),
            request.GET.get('genderword'),
            url='main/moreresults.html',
            splice=False
        )
    else:
        return Results(context, request, request.GET.get('order'), request.GET.get('type'), request.GET.get('web'), url='main/moreresults.html', splice=False)
from django.shortcuts import render, redirect
from django.conf import settings
import json
from datetime import datetime
import random
import os


def index_view(request):
    context = {}
    with open(os.path.join(settings.BASE_DIR, 'hypernews', settings.NEWS_JSON_PATH), "r") as json_file:
        if request.GET:
            news_from_json = list()
            for news in json.load(json_file):
                if request.GET.get('q') in news['title']:
                    news_from_json.append(news)
        else:
            news_from_json = json.load(json_file)
        context['news'] = sorted(news_from_json, key=lambda n: n['created'], reverse=True)
        date_set = set()
        for news in news_from_json:
            date = datetime.strptime(news['created'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d')
            date_set.add(date)
        context['created'] = sorted(list(date_set), reverse=True)
    return render(request, 'news/index.html', context)


def news_page(request, link):
    context = {}
    with open(os.path.join(settings.BASE_DIR, 'hypernews', settings.NEWS_JSON_PATH), "r") as json_file:
        news_from_json = json.load(json_file)
        for news in news_from_json:
            if news['link'] == link:
                context['news'] = news
                break
    return render(request, 'news/news_page.html', context)


def create_article(request):
    context = {}
    if request.POST:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(settings.BASE_DIR, 'hypernews', settings.NEWS_JSON_PATH), "r") as json_file:
            news_from_json = json.load(json_file)
            links = list(map(lambda news: str(news['link']), news_from_json))
            link = random.randint(0, 100000)
            while link in links:
                link = random.randint(0, 100000)
            news_from_json.append({'title': request.POST.get('title'),
                                   'text': request.POST.get('text'),
                                   'created': date,
                                   'link': link})
        with open(os.path.join(settings.BASE_DIR, 'hypernews', settings.NEWS_JSON_PATH), "w") as json_file:
            json.dump(news_from_json, json_file)
        return redirect(index_view)
    else:
        return render(request, 'news/create.html', context)

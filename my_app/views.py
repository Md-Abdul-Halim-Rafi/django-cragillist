import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'


def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    # getting searc text from post request by form
    search = request.POST.get('search')
    # adding search text to database
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)

    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_posting': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

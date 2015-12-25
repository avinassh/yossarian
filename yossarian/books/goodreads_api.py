from xml.parsers.expat import ExpatError

import requests
import xmltodict
from django.conf import settings


def get_book_details_by_id(goodreads_id):
    goodreads_api_key = settings.GOODREADS_API_KEY
    api_url = 'http://goodreads.com/book/show/{0}?format=xml&key={1}'
    r = requests.get(api_url.format(goodreads_id, goodreads_api_key))
    try:
        book_data = xmltodict.parse(r.content)['GoodreadsResponse']['book']
    except (TypeError, KeyError, ExpatError):
        return False
    keys = ['title', 'average_rating', 'ratings_count', 'description', 'url',
            'image_url']
    book = {}
    for k in keys:
        book[k] = book_data[k]
    if type(book_data['authors']['author']) == list:
        authors = [author['name'] for author in book_data['authors']['author']]
        authors = ', '.join(authors)
    else:
        authors = book_data['authors']['author']['name']
    book['authors'] = authors
    return book

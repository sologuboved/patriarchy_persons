import re
import requests
from bs4 import BeautifulSoup
from basic_operations import *

DB_URL = 'http://www.patriarchia.ru/db/persons/'
FLEXIONS_JSON = 'flexions.json'
CATEGORIES_JSON = 'categories.json'


def collect_categories():
    categories = BeautifulSoup(requests.get(DB_URL).content, 'lxml').find_all('ul', {'class': 'submenu'})[0]
    dump_utf_json({tag_a.text: tag_a.get('href') for tag_a in categories.find_all('a', href=True)},
                  CATEGORIES_JSON)


def collect_flexions_from_category(category_url):
    persons = BeautifulSoup(requests.get(category_url).content,
                            'lxml').find_all('div', {'id': 'main'})[0].find_all('h4', {'class': 'title'})
    return [re.findall(r'/(\d+).html', person.find_all('a', href=True)[0].get('href'))[0] for person in persons]


@which_watch
def collect_all_flexions():
    dump_utf_json({category_name: collect_flexions_from_category(category_url) for category_name, category_url in
                   load_utf_json(CATEGORIES_JSON).items()}, FLEXIONS_JSON)


if __name__ == '__main__':
    collect_all_flexions()

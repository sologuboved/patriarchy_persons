import re
import requests
from bs4 import BeautifulSoup
from basic_operations import *

MAIN_URL = 'http://www.patriarchia.ru/db/persons/'
FLEXIONS_JSON = 'flexions.json'
CATEGORIES_JSON = 'categories.json'
PERSONALIA_JSON = 'personalia.json'
NAME = 'Имя:'
CATEGORY = 'Категория:'
URL = 'Источник:'


def collect_categories():
    categories = BeautifulSoup(requests.get(MAIN_URL).content, 'lxml').find_all('ul', {'class': 'submenu'})[0]
    dump_utf_json({tag_a.text: tag_a.get('href') for tag_a in categories.find_all('a', href=True)},
                  CATEGORIES_JSON)


def collect_flexions_from_category(category_url):
    persons = BeautifulSoup(requests.get(category_url).content,
                            'lxml').find_all('div', {'id': 'main'})[0].find_all('h4', {'class': 'title'})
    return [re.findall(r'/(\d+).html', person.find_all('a', href=True)[0].get('href'))[0] for person in persons]


def collect_all_flexions():
    dump_utf_json({category_name: collect_flexions_from_category(category_url) for category_name, category_url in
                   load_utf_json(CATEGORIES_JSON).items()}, FLEXIONS_JSON)


def compare_number():
    main_page_number = len(BeautifulSoup(requests.get(MAIN_URL).content,
                                         'lxml').find_all('div', {'id': 'main'})[0].find_all('h4', {'class': 'title'}))
    print(main_page_number <= get_total_number())


def get_total_number():
    return sum([len(flexions) for _, flexions in load_utf_json(FLEXIONS_JSON).items()])


def construct_url(flexion):
    return 'http://www.patriarchia.ru/db/print/{}.html'.format(flexion)


def scrape_person(flexion, category):
    url = construct_url(flexion)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    section = BeautifulSoup(str(soup.find_all('div', {'class': 'section'})[0]).replace('<p class="text">',
                                                                                       '\n').replace('</p>',
                                                                                                     ''), 'lxml')
    datum = {key.text.strip(): value.text.strip() for key, value in zip(section.find_all('b'), section.find_all('dd'))}
    datum.update({NAME: section.find_all('h1')[0].text, CATEGORY: category, URL: url})
    return datum


@which_watch
def scrape_all_persons():
    persons = list()
    total_num = get_total_number()
    count = 0
    try:
        for category, flexions in load_utf_json(FLEXIONS_JSON).items():
            for flexion in flexions:
                count += 1
                print('\r{} of {}'.format(count, total_num), end='', flush=True)
                persons.append(scrape_person(flexion, category))
    except Exception as e:
        print('\n' + str(e))
    finally:
        print('\nDumping...')
        dump_utf_json(persons, PERSONALIA_JSON)


def list_fields():
    fields = set()
    for person in load_utf_json(PERSONALIA_JSON):
        fields |= set(person.keys())
    for field in sorted(list(fields)):
        print(field)


if __name__ == '__main__':
    scrape_all_persons()
    # list_fields()

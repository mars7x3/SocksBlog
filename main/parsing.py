import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def get_dates(html):
    soup = BeautifulSoup(html, 'lxml')
    get_data_div = soup.find('div', class_='content')
    return get_data_div


def get_every_date(html):
    get_list = html.find_all('div', class_='blog__item blog__item_loop')
    list_ = []
    for list in get_list:
        try:
            photo = list.find('div', class_='blog__thumb blog__thumb_loop').find('img').get('src')
        except:
            photo = ""

        try:
            description = list.find('div', class_='blog__excerpt').find('p').text
        except:
            description = ''

        try:
            title = list.find('div', class_='blog__side blog__side_text').find('a').text
        except:
            title = ''


        data = {'title': title.replace('\n', ''), 'description': description.replace('\n', '').strip(),
                'photo': photo}
        list_.append(data)
    return list_


def pars():
    akg_url = 'https://www.fabrikanoskov.ru/blog/'
    html = get_html(akg_url)
    html = get_dates(html)
    list_ = get_every_date(html)
    return list_
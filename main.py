import requests
from bs4 import BeautifulSoup
import pprint
import json

url = 'https://ria.ru/'
response = requests.get(url)
print('Статус главной страницы:', response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
lst_news = soup.find_all('div', class_='cell-list__item m-no-image')
news = []
i = 1
for one_news in lst_news:
    one = {}
    url_news = one_news.find('a').get('href')
    response = requests.get(url_news)
    print(f'Статус {i}-й страницы:', response.status_code)
    soup_news = BeautifulSoup(response.text, 'html.parser')
    date_news = soup_news.find('div', class_='article__info-date').find('a')
    # print(date_news.text)
    one['date'] = date_news.text
    title_news = soup_news.find('div', class_='article__title')
    # print(title_news.text)
    one['title'] = title_news.text
    text_news = soup_news.find_all('div', class_='article__text')
    text_all = ''
    for text in text_news:
        text_all += text.text + '\n'
    # print(text_all)
    one['text'] = text_all
    news.append(one)
    i += 1
pprint.pprint(news)
with open('news.json', 'w') as f:
    json.dump(news, f, ensure_ascii=False)
import requests
from bs4 import BeautifulSoup
import pprint
import json
import telebot

TOKEN = '6176024349:AAHR00r-5W7cdIX-ZY-9zvzz_BcijHMI3CY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Добро пожаловать в канал, где можно узнать о новостях через сайт РИА. Чтобы получить список последних ' \
           'новостей, наберите "/news".\nПомощь: "/help".'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])
def start(message):
    mess = '"/news" - получить список последних новостей\n"/news X" - получить подробную новость, где X - номер ' \
           'позиции из полученного списка '
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['news'])
def news(message):
    print(message)
    lst = message.text.split(' ')
    # print(lst)
    mess = 'Последние новости:'
    if len(lst) == 1:
        url = 'https://ria.ru/'
        response = requests.get(url)
        print('Статус главной страницы:', response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        lst_news = soup.find_all('div', class_='cell-list__item m-no-image')
        ria_news = []
        # i = 1
        for one_news in lst_news:
            one = {}
            title_news = one_news.find('a').get('title')
            url_news = one_news.find('a').get('href')
            one['title'] = title_news
            one['url'] = url_news
            #     response = requests.get(url_news)
            #     print(f'Статус {i}-й страницы:', response.status_code)
            #     soup_news = BeautifulSoup(response.text, 'html.parser')
            #     date_news = soup_news.find('div', class_='article__info-date').find('a')
            #     # print(date_news.text)
            #     one['date'] = date_news.text
            #     title_news = soup_news.find('div', class_='article__title')
            #     # print(title_news.text)
            #     one['title'] = title_news.text
            #     text_news = soup_news.find_all('div', class_='article__text')
            #     text_all = ''
            #     for text in text_news:
            #         text_all += text.text + '\n'
            #     # print(text_all)
            #     one['text'] = text_all
            ria_news.append(one)
        #
        # pprint.pprint(ria_news)
        with open('ria_news.json', 'w') as f:
            json.dump(ria_news, f, ensure_ascii=False)

        for i in range(len(ria_news)):
            mess += f'\n{i + 1}. ' + ria_news[i]['title']
            # i += 1
    else:
        with open('ria_news.json', 'r') as f:
            ria_news = json.load(f)
        response = requests.get(ria_news[int(lst[1])-1]['url'])
        print(f'Статус {lst[1]}-й страницы:', response.status_code)
        soup_news = BeautifulSoup(response.text, 'html.parser')
        date_news = soup_news.find('div', class_='article__info-date').find('a')
        # print(date_news.text)
        # one['date'] = date_news.text
        title_news = soup_news.find('div', class_='article__title')
        # print(title_news.text)
        # one['title'] = title_news.text
        text_news = soup_news.find_all('div', class_='article__text')
        text_all = ''
        for text in text_news:
            text_all += text.text + '\n'
        # print(text_all)
        # one['text'] = text_all
        mess = date_news.text + '\n' + title_news.text + '\n' + text_all
    bot.send_message(message.chat.id, mess)


bot.infinity_polling()

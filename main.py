import datetime
import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='2398'):
    """Текущие дата и временя"""
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    """Юзерагент"""
    ua = UserAgent().random

    """Формируем заголовки с сайта, HeadersRequests"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua,
        'X-Requested-With': 'XMLHttpRequest'
    }

    """Формируем коды городов с сайта, Cookies"""
    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    """Запрос на сайт"""
    response = requests.get(url='https://magnit.ru/promo/', headers=headers, cookies=cookies)

    # """Сохранение полученных данных в файл"""
    # with open('index.html', 'w', encoding='UTF-8') as file:
    #     file.write(response.text)

    # """Работа с полученными данными"""
    # with open('index.html', 'r', encoding='UTF-8') as file:
    #     src = file.read()

    soup = BeautifulSoup(response.text, 'lxml')

    """Поиск города в тегах сайта"""
    city = soup.find('a', class_='header__contacts-link_city').text.strip()
    """Сбор всех карточек товаров со страницы"""
    cards = soup.find_all('a', class_='card-sale_catalogue')
    #print(city, len(cards))


    data = []
    """Проходим по списку с карточками товаров"""
    for card in cards:
        card_title = card.find('div', class_='card-sale__title').text.strip()

        """Проверка на присутствие скидки в блоке div, т.к. на сайте есть товары без скидок"""
        try:
            card_discount = card.find('div', class_='card-sale__discount').text.strip()
        except AttributeError:
            continue

        """Сбор данных цен без скидок и цен со скидками"""
        card_price_old_integer = card.find('div', class_='label__price_old').find(
                                           'span', class_='label__price-integer').text.strip()
        card_price_old_decimal = card.find('div', class_='label__price_old').find(
                                           'span', class_='label__price-decimal').text.strip()
        card_old_price = f'{card_price_old_integer}.{card_price_old_decimal}'

        card_price_integer = card.find('div', class_='label__price_new').find(
                                       'span', class_='label__price-integer').text.strip()
        card_price_decimal = card.find('div', class_='label__price_new').find(
                                       'span', class_='label__price-decimal').text.strip()
        card_price = f'{card_price_integer}.{card_price_decimal}'

        """Сбор данных дат скидок"""
        card_sale_date: object = card.find('div', class_='card-sale__date').text.strip().replace('\n', ' ')
        #print(card_sale_date)

        """Добавляем собранные данные в список"""
        data.append(
            [
                card_title,
                card_old_price,
                card_price,
                card_discount,
                card_sale_date,
            ]
        )


    """Запись в CSV файл"""
    with open(f'{city}_{cur_time}.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
                'Время акции',
            )
        )
        writer.writerows(
            data
        )

    print(f'Файл {city}_{cur_time}.csv успешно записан.')


def main():
    collect_data(city_code='2398')


if __name__ == '__main__':
    main()
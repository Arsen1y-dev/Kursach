import requests
import time
import random
from bs4 import BeautifulSoup
from settings import headers, cookies, params


base_url = 'https://www.avito.ru/moskva/kvartiry/prodam/studii-ASgBAgICAkSSA8YQygj~WA'


def get_listing_links(page=1, session=None):
    params.update({'p': page})
    response = session.get(base_url, params=params)

    if response.status_code != 200:
        print(f"Ошибка на странице {page}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', attrs={'data-marker': 'item'})
    links = []

    for item in items:
        a_tag = item.find('a', href=True)
        if a_tag:
            href = a_tag['href']
            if href.startswith('/'):
                href = 'https://www.avito.ru' + href
            links.append(href)
    return list(set(links))


def parse_avito_links(max_pages=1700, output_file='avito_links.txt'): #кол-во страниц
    all_links = []

    with requests.Session() as session:
        session.headers.update(headers)
        session.cookies.update(cookies)

        for page in range(1, max_pages + 1):
            print(f"Парсим страницу {page}...")
            links = get_listing_links(page, session=session)
            print(f"Найдено {len(links)} ссылок")
            if not links:
                break

            all_links.extend(links)
            delay = random.uniform(5, 8) #задержка
            print(f"Ожидание: {delay:.2f} секунд")
            print("=" * 90)
            time.sleep(delay)

    all_links = list(set(all_links))
    print(f"Найдено {len(all_links)} уникальных ссылок")

    with open(output_file, 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + '\n')

    print(f"Ссылки сохранены в файл {output_file}")


# Вызов функции
if __name__ == '__main__':
    parse_avito_links()

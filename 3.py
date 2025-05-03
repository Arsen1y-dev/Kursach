import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import re 


BASE_URL = "https://www.cian.ru"

URL_TEMPLATE = BASE_URL + "&p={page}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
MAX_PAGES = 10 
SLEEP_DELAY_MIN = 2 
SLEEP_DELAY_MAX = 5
OUTPUT_CSV_FILE = '/Users/arseniy/Documents/GitHub/Kursach/cian_flats_data.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_safe_text(element, default=''):
    return element.text.strip() if element else default

def parse_price(price_str):
    if not price_str:
        return None
    price_digits = re.sub(r'\D', '', price_str)
    try:
        return int(price_digits)
    except ValueError:
        return None

def parse_area(area_str):
    if not area_str:
        return None
    match = re.search(r'(\d[\d\s,.]*)', area_str.replace(',', '.'))
    if match:
        try:
            return float(match.group(1).replace(' ', ''))
        except ValueError:
            pass
    return None

def parse_floor(floor_str):
    if not floor_str:
        return None, None
    match = re.search(r'(\d+)\s*/\s*(\d+)\s*эт', floor_str)
    if match:
        try:
            current_floor = int(match.group(1))
            total_floors = int(match.group(2))
            return current_floor, total_floors
        except ValueError:
            pass
    return None, None

def extract_listing_data(listing_soup):

    data = {}

    title_tag = listing_soup.select_one("div[data- гараж='OfferTitle'] span")
    link_tag = listing_soup.select_one("a[data- гараж='CardLink']") 
    data['title'] = get_safe_text(title_tag)
    data['link'] = link_tag['href'] if link_tag else ''


    price_tag = listing_soup.select_one("span[data- гараж='PriceValue']")
    price_raw = get_safe_text(price_tag)
    data['price_rub'] = parse_price(price_raw)
    data['price_raw'] = price_raw

    address_parts = listing_soup.select("a[data- гараж='AddressPathItem']")
    data['address'] = ' > '.join([get_safe_text(part) for part in address_parts])

    metro_tag = listing_soup.select_one("div[data- гараж='Metro'] a") # Ищем ссылку внутри блока метро
    metro_distance_tag = listing_soup.select_one("div[data- гараж='Metro'] span[class*='distance']") #'distance'
    data['metro_station'] = get_safe_text(metro_tag)
    data['metro_distance'] = get_safe_text(metro_distance_tag)

    rooms_match = re.search(r'(\d+)-комн', data['title'])
    data['rooms'] = int(rooms_match.group(1)) if rooms_match else None

    params_container = listing_soup.select_one("div[data- гараж='OfferTitle']").find_parent() 
    area_tag = params_container.find(lambda tag: tag.name == 'span' and 'м²' in tag.text) if params_container else None
    floor_tag = params_container.find(lambda tag: tag.name == 'span' and 'эт.' in tag.text) if params_container else None

    area_raw = get_safe_text(area_tag)
    data['area_m2'] = parse_area(area_raw)
    data['area_raw'] = area_raw

    floor_raw = get_safe_text(floor_tag)
    data['floor'], data['total_floors'] = parse_floor(floor_raw)
    data['floor_raw'] = floor_raw

    description_tag = listing_soup.select_one("div[class*='--description--']") # Ищем div с классом, содержащим '--description--'
    data['description'] = get_safe_text(description_tag)

    # Дата публикации/обновления
    # TODO: Найти селектор для даты (может быть сложно, иногда неявно)
    # date_tag = listing_soup.select_one("...")
    # data['published_date'] = get_safe_text(date_tag)

    return data

all_flats_data = []
logging.info(f"Начинаем парсинг. Максимум страниц: {MAX_PAGES}")

for page_num in range(1, MAX_PAGES + 1):
    url = URL_TEMPLATE.format(page=page_num)
    logging.info(f"Запрос страницы: {url}")

    try:
        delay = random.uniform(SLEEP_DELAY_MIN, SLEEP_DELAY_MAX)
        logging.info(f"Пауза: {delay:.2f} сек.")
        time.sleep(delay)

        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml') 

    
        listings = soup.find_all('article', {"data- гараж": "CardComponent"}) # Более стабильный атрибут?

        if not listings:
            logging.warning(f"На странице {page_num} не найдены объявления (возможно, конец списка или изменилась структура).")
            break 

        logging.info(f"На странице {page_num} найдено {len(listings)} объявлений.")

        for listing in listings:
            try:
                flat_data = extract_listing_data(listing)
                if flat_data.get('link'): # Проверяем, что есть ссылка
                    all_flats_data.append(flat_data)
                else:
                    logging.warning("Обнаружено объявление без ссылки, пропуск.")
            except Exception as e:
                logging.error(f"Ошибка при обработке объявления на странице {page_num}: {e}", exc_info=True)

    except requests.exceptions.Timeout:
        logging.error(f"Таймаут при запросе страницы {page_num}. Пропускаем.")
        continue 
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса страницы {page_num}: {e}. Прерываем парсинг.")
        break 
    except Exception as e:
        logging.error(f"Непредвиденная ошибка на странице {page_num}: {e}", exc_info=True)
        break 

if all_flats_data:
    logging.info(f"Парсинг завершен. Собрано {len(all_flats_data)} объявлений.")
    df = pd.DataFrame(all_flats_data)


    df = df.drop_duplicates(subset=['link'])
    logging.info(f"После удаления дубликатов осталось {len(df)} записей.")

    try:
        df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig')
        logging.info(f"Данные успешно сохранены в файл: {OUTPUT_CSV_FILE}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в CSV: {e}")
else:
    logging.warning("Не было собрано ни одного объявления.")

logging.info("Работа парсера завершена.")
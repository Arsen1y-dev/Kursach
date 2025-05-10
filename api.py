import requests
import csv
import time
import random
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='avito_api_errors.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Параметры API
BASE_URL = "https://api.avito.ru"
CLIENT_ID = "_TWrdb-tfwx6-YfNaPoy"  # Замените на свой
CLIENT_SECRET = "v6173zA0k-bwxC_IrD9j3Es5owS28YvFSofzN4x9"  # Замените на свой
OUTPUT_FILE = "avito_data_api.csv"

# Получение токена
def get_access_token():
    url = f"{BASE_URL}/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        token_data = response.json()
        logging.info("Токен успешно получен")
        return token_data.get("access_token")
    except Exception as e:
        logging.error(f"Ошибка получения токена: {e}")
        raise

# Получение списка объявлений (примерный эндпоинт, зависит от доступа)
def fetch_ads(access_token, page=1):
    url = f"{BASE_URL}/core/v1/items"  # Уточните, открыт ли этот доступ
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "page": page,
        "limit": 100
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        print(response.json()) # Для отладки
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка запроса объявлений на странице {page}: {e}")
        return {}

# Сохранение данных в CSV
def save_to_csv(data, first_write=False):
    fieldnames = ['URL', 'Цена', 'Общая площадь', 'Этаж', 'Адрес', 'Тип дома', 'Год постройки', 'Item ID']
    mode = 'w' if first_write else 'a'
    with open(OUTPUT_FILE, mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if first_write:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

# Основная логика
def main():
    access_token = get_access_token()

    all_ads = []
    page = 1
    first_write = True

    while True:
        data = fetch_ads(access_token, page)
        ads = data.get('items', [])  # Уточните ключ на основе вашего ответа
        if not ads:
            logging.info("Нет больше объявлений")
            break

        for ad in ads:
            ad_data = {
                'URL': ad.get('url', ''),
                'Цена': str(ad.get('price', '')).replace(' ₽', '').replace(' ', ''),
                'Общая площадь': str(ad.get('area', '')).replace(' м²', '').replace(',', '.'),
                'Этаж': ad.get('floor', ''),
                'Адрес': ad.get('address', ''),
                'Тип дома': ad.get('house_type', ''),
                'Год постройки': ad.get('build_year', ''),
                'Item ID': ad.get('id', '')
            }
            all_ads.append(ad_data)

        logging.info(f"Получено {len(ads)} объявлений на странице {page}")
        save_to_csv(all_ads, first_write=first_write)
        first_write = False
        all_ads.clear()

        if not data.get('pagination', {}).get('next_page'):  # Уточните, как выглядит пагинация
            break
        page += 1
        time.sleep(random.uniform(3, 8))

    print(f"Данные сохранены в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
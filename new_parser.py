import requests
import csv
import time
import random
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from settings import params_announcement, headers_announcement, cookies_announcement

input_file = "clean_links.txt"
output_file = "avito_data_new.csv"

from fake_useragent import UserAgent
ua = UserAgent()


# Настройка сессии с повторными попытками
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.headers.update(headers_announcement)
session.cookies.update(cookies_announcement)
session.headers['User-Agent'] = ua.random

# Загрузка существующих данных
try:
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_links = {row.get('URL', '') for row in reader}
except FileNotFoundError:
    existing_links = set()

# Загрузка и фильтрация ссылок
with open(input_file, "r", encoding="utf-8") as file_read:
    all_links = [link.strip() for link in file_read if link.strip() not in existing_links]

all_keys = set()
data_list = []

def save_to_csv(first_write=False):
    if not data_list:
        return
    
    all_keys_sorted = sorted(all_keys)
    
    # Добавляем URL в список полей
    if 'URL' not in all_keys_sorted:
        all_keys_sorted.insert(0, 'URL')
    
    mode = 'w' if first_write else 'a'
    with open(output_file, mode, encoding="utf-8", newline="") as file_write:
        writer = csv.DictWriter(file_write, fieldnames=all_keys_sorted)
        
        if first_write:
            writer.writeheader()
        
        for row in data_list:
            writer.writerow({key: row.get(key, "") for key in all_keys_sorted})
    
    data_list.clear()
    print(f"Данные сохранены ({len(data_list)} записей)")

try:
    first_write = not existing_links
    for index, link in enumerate(all_links):
        try:
            response = session.get(
                link, 
                params=params_announcement,
                timeout=10
            )
            response.raise_for_status()
            
            bs4 = BeautifulSoup(response.text, "html.parser")
            divs = bs4.find_all("ul", class_="params-paramsList-_awNW")
            
            data = {'URL': link}
            for div in divs:
                for li in div.find_all("li"):
                    try:
                        col, _, text = li.text.partition(': ')
                        if not _:
                            continue
                        data[col] = text.strip()
                        all_keys.add(col)
                    except Exception as e:
                        print(f"Ошибка парсинга: {e}")
            
            data_list.append(data)
            print(f"{index} [OK] {link}")
            
            if (index + 1) % 10 == 0:
                save_to_csv(first_write=first_write)
                first_write = False
            
            time.sleep(random.uniform(3, 7))
            
        except Exception as e:
            print(f"{index} [ERROR] {link} - {str(e)}")
            continue

except KeyboardInterrupt:
    print("\nПрерывание пользователем. Сохраняем данные...")
    
finally:
    save_to_csv(first_write=first_write)

print(f"Данные успешно сохранены в {output_file}")
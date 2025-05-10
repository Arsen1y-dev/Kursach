import requests
import csv
import time
import random
import logging
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from settings import params_announcement, headers_announcement, cookies_announcement
from fake_useragent import UserAgent

# Настройка логгирования
logging.basicConfig(
    filename="errors_log.txt",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Прогресс-бар, если установлен tqdm
try:
    from tqdm import tqdm
    use_tqdm = True
except ImportError:
    use_tqdm = False

# Прокси (замените на ваши реальные прокси)
# Прокси (замените на ваши реальные прокси)
proxies_list = [
    {"http": "http://USER:PASS@proxy_ip:port", "https": "http://USER:PASS@proxy_ip:port"},
    {"http": "http://23.82.137.158:80", "https": "http://23.82.137.158:80"},
    {"http": "http://23.247.136.254:80", "https": "http://23.247.136.254:80"},
    {"http": "http://54.245.27.232:999", "https": "http://54.245.27.232:999"},
    {"http": "http://18.236.65.56:3129", "https": "http://18.236.65.56:3129"},
    {"http": "http://52.11.48.124:3128", "https": "http://52.11.48.124:3128"},
    {"http": "http://54.245.220.196:8118", "https": "http://54.245.220.196:8118"},
    {"http": "http://54.184.124.175:14581", "https": "http://54.184.124.175:14581"},
    {"http": "http://162.223.90.150:80", "https": "http://162.223.90.150:80"},
    {"http": "http://144.126.216.57:80", "https": "http://144.126.216.57:80"},
    {"http": "http://68.185.57.66:80", "https": "http://68.185.57.66:80"},
    {"http": "http://167.99.236.14:80", "https": "http://167.99.236.14:80"},
    {"http": "http://159.65.245.255:80", "https": "http://159.65.245.255:80"},
    {"http": "http://74.207.235.213:1221", "https": "http://74.207.235.213:1221"},
    {"http": "http://162.240.19.30:80", "https": "http://162.240.19.30:80"},
    {"http": "http://50.221.230.186:80", "https": "http://50.221.230.186:80"},
    {"http": "http://192.73.244.36:80", "https": "http://192.73.244.36:80"},
    {"http": "http://169.56.21.242:8080", "https": "http://169.56.21.242:8080"},
    {"http": "http://130.245.32.202:80", "https": "http://130.245.32.202:80"},
    {"http": "http://32.223.6.94:80", "https": "http://32.223.6.94:80"},
    {"http": "http://107.150.37.86:1723", "https": "http://107.150.37.86:1723"},
    {"http": "http://54.191.48.147:3129", "https": "http://54.191.48.147:3129"},
    {"http": "http://34.102.48.89:8080", "https": "http://34.102.48.89:8080"},
    {"http": "http://18.236.175.208:10001", "https": "http://18.236.175.208:10001"},
    {"http": "http://104.225.220.233:80", "https": "http://104.225.220.233:80"},
    {"http": "http://47.251.87.199:1036", "https": "http://47.251.87.199:1036"},
    {"http": "http://138.91.159.185:80", "https": "http://138.91.159.185:80"},
    {"http": "http://170.106.144.64:8090", "https": "http://170.106.144.64:8090"},
    {"http": "http://63.143.57.119:80", "https": "http://63.143.57.119:80"},
    {"http": "http://47.88.59.79:82", "https": "http://47.88.59.79:82"},
    {"http": "http://47.254.88.250:13001", "https": "http://47.254.88.250:13001"},
    {"http": "http://23.82.137.159:80", "https": "http://23.82.137.159:80"},
    {"http": "http://35.90.245.227:31293", "https": "http://35.90.245.227:31293"},
    {"http": "http://54.245.34.166:10001", "https": "http://54.245.34.166:10001"},
    {"http": "http://63.143.57.116:80", "https": "http://63.143.57.116:80"},
    {"http": "http://50.122.86.118:80", "https": "http://50.122.86.118:80"},
    {"http": "http://23.247.136.248:80", "https": "http://23.247.136.248:80"},
    {"http": "http://165.232.129.150:80", "https": "http://165.232.129.150:80"},
    {"http": "http://54.214.109.103:10001", "https": "http://54.214.109.103:10001"},
    {"http": "http://40.76.69.94:8080", "https": "http://40.76.69.94:8080"},
    {"http": "http://198.199.86.11:8080", "https": "http://198.199.86.11:8080"},
    {"http": "http://66.191.31.158:80", "https": "http://66.191.31.158:80"},
    {"http": "http://138.68.60.8:80", "https": "http://138.68.60.8:80"},
    {"http": "http://63.143.57.117:80", "https": "http://63.143.57.117:80"},
    {"http": "http://198.49.68.80:80", "https": "http://198.49.68.80:80"},
    {"http": "http://47.251.122.81:8888", "https": "http://47.251.122.81:8888"},
    {"http": "http://47.252.29.28:11222", "https": "http://47.252.29.28:11222"},
    {"http": "http://198.74.51.79:8888", "https": "http://198.74.51.79:8888"},
    {"http": "http://47.90.205.231:33333", "https": "http://47.90.205.231:33333"},
    {"http": "http://170.106.83.149:13001", "https": "http://170.106.83.149:13001"},
    {"http": "http://23.82.137.156:80", "https": "http://23.82.137.156:80"},
    {"http": "http://34.221.119.219:999", "https": "http://34.221.119.219:999"},
    {"http": "http://47.251.43.115:33333", "https": "http://47.251.43.115:33333"},
    {"http": "http://216.229.112.25:8080", "https": "http://216.229.112.25:8080"},
    {"http": "http://63.143.57.115:80", "https": "http://63.143.57.115:80"},
    {"http": "http://107.150.37.85:1723", "https": "http://107.150.37.85:1723"},
    {"http": "http://82.180.132.69:80", "https": "http://82.180.132.69:80"},
    {"http": "http://35.86.81.136:3128", "https": "http://35.86.81.136:3128"},
    {"http": "http://206.233.201.150:3128", "https": "http://206.233.201.150:3128"},
    {"http": "http://34.122.187.196:80", "https": "http://34.122.187.196:80"},
    {"http": "http://159.65.221.25:80", "https": "http://159.65.221.25:80"},
    {"http": "http://72.14.178.181:50513", "https": "http://72.14.178.181:50513"},
    {"http": "http://185.77.220.44:8085", "https": "http://185.77.220.44:8085"},
    {"http": "http://5.161.103.41:88", "https": "http://5.161.103.41:88"},
    {"http": "http://185.250.180.238:8080", "https": "http://185.250.180.238:8080"}
    # Добавьте остальные прокси по аналогии
]

input_file = "clean_links_studii.txt"
output_file = "avito_data_studii.csv"

ua = UserAgent()

# Настройка сессии с повторными попытками
session = requests.Session()
retry_strategy = Retry(
    total=5,  # увеличено количество попыток
    backoff_factor=2,  # экспоненциальная задержка
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.headers.update(headers_announcement)
session.cookies.update(cookies_announcement)
session.headers['User-Agent'] = ua.random

# Загрузка существующих ссылок
try:
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_links = {row.get('URL', '') for row in reader}
except FileNotFoundError:
    existing_links = set()

# Загрузка и фильтрация ссылок
with open(input_file, "r", encoding="utf-8") as file_read:
    all_links = [link.strip() for link in file_read if link.strip() and link.strip() not in existing_links]

all_keys = set()
data_list = []

def save_to_csv(first_write=False):
    if not data_list:
        return
    
    all_keys_sorted = sorted(all_keys)
    if 'URL' not in all_keys_sorted:
        all_keys_sorted.insert(0, 'URL')

    mode = 'w' if first_write else 'a'
    count = len(data_list)

    with open(output_file, mode, encoding="utf-8", newline="") as file_write:
        writer = csv.DictWriter(file_write, fieldnames=all_keys_sorted)
        if first_write:
            writer.writeheader()
        for row in data_list:
            writer.writerow({key: row.get(key, "") for key in all_keys_sorted})
    
    data_list.clear()
    print(f"Данные сохранены ({count} записей)")

# Основной цикл
try:
    first_write = not os.path.exists(output_file)
    iterable = tqdm(enumerate(all_links), total=len(all_links)) if use_tqdm else enumerate(all_links)

    for index, link in iterable:
        try:
            # Выбор случайного прокси
            proxy = random.choice(proxies_list)

            session.headers['User-Agent'] = ua.random  # Обновляем UA перед каждым запросом
            response = session.get(
                link, 
                params=params_announcement,
                timeout=10,
                proxies=proxy  # Используем прокси
            )
            response.raise_for_status()

            # Проверка на капчу или бан
            if "Вы робот?" in response.text or "captcha" in response.url:
                logging.warning(f"{index} [BAN/CAPTCHA] {link}")
                print(f"{index} [BAN/CAPTCHA] {link}")
                continue

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
                        logging.warning(f"{index} [LI_PARSE_ERROR] {li.text} — {str(e)}")
                        continue

            data_list.append(data)
            print(f"{index} [OK] {link}")

            if (index + 1) % 10 == 0:
                save_to_csv(first_write=first_write)
                first_write = False

            # Увеличенная задержка между запросами
            time.sleep(random.uniform(7, 12))

        except Exception as e:
            logging.error(f"{index} [ERROR] {link} — {str(e)}")
            print(f"{index} [ERROR] {link} - {str(e)}")

except KeyboardInterrupt:
    print("\nПрерывание пользователем. Сохраняем данные...")

finally:
    save_to_csv(first_write=first_write)

print(f"Данные успешно сохранены в {output_file}")
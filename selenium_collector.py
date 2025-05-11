import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

base_url = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&f=ASgBAQICAUSSA8YQAUDKCCT8zzKEWQ'

def setup_driver():
    """Настройка веб-драйвера Chrome с оптимизациями."""
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Раскомментировать для работы без интерфейса
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def load_existing_links(file_path):
    """Загрузка существующих ссылок из файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def scroll_page(driver):
    """Прокрутка страницы до конца для загрузки всех элементов."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Пауза для загрузки контента
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_listing_links(page, driver, max_retries=2):
    """Сбор ссылок с указанной страницы с повторными попытками."""
    for attempt in range(max_retries):
        try:
            url = f"{base_url}&p={page}"  # Исправлено: добавлен & для корректного URL
            driver.get(url)
            
            # Прокрутка страницы
            scroll_page(driver)
            
            # Ожидание загрузки всех объявлений
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-marker="item"]'))
            )
            
            # Проверка на капчу
            if 'captcha' in driver.current_url or 'access-restricted' in driver.page_source:
                print(f"[!] Обнаружена капча на странице {page}, попытка {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(5, 10))
                    continue
                return None
            
            # Парсинг страницы
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find_all('div', attrs={'data-marker': 'item'})
            links = ['https://www.avito.ru' + item.find('a')['href'] for item in items if item.find('a')]
            
            # Проверка минимального количества ссылок
            if len(links) < 10:  # Увеличено до 10
                print(f"[!] Мало ссылок на странице {page}: {len(links)}, попытка {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(5, 10))
                    continue
                return None
            
            return links
        
        except Exception as e:
            print(f"[!] Ошибка на странице {page}, попытка {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(5, 10))
                continue
            return None

def parse_avito_links(max_pages=100, output_file='links_2.txt'):
    """Основная функция парсинга ссылок с Avito."""
    existing_links = load_existing_links(output_file)
    print(f"[*] Начато обновление базы. Существующих ссылок: {len(existing_links)}")
    
    driver = setup_driver()
    try:
        total_new = 0
        current_page = 1
        error_count = 0
        max_errors = 3
        
        while current_page <= max_pages and error_count < max_errors:
            print(f"\n[+] Страница {current_page}/{max_pages}")
            
            try:
                base_delay = random.uniform(4, 8)
                jitter = random.uniform(-1, 1)
                delay = max(3, base_delay + jitter)
                
                links = get_listing_links(current_page, driver)
                
                if links is None:
                    error_count += 1
                    print(f"[!] Ошибка ({error_count}/{max_errors})")
                    time.sleep(delay * 2)
                    continue
                
                new_links = [link for link in links if link not in existing_links]
                new_count = len(new_links)
                total_new += new_count
                
                print(f"  Найдено: {len(links)} ссылок")
                print(f"  Новых: {new_count} ссылок")
                print(f"  Всего уникальных: {len(existing_links) + new_count}")
                
                if new_count > 0:
                    with open(output_file, 'a', encoding='utf-8') as f:
                        f.write('\n'.join(new_links) + '\n')
                    existing_links.update(new_links)
                    error_count = 0
                
                print(f"  Задержка: {delay:.2f} сек.")
                time.sleep(delay)
                
                current_page += 1
                
            except Exception as e:
                print(f"[!] Необработанная ошибка: {str(e)}")
                error_count += 1
                time.sleep(15)
    
    finally:
        driver.quit()
    
    print(f"\n[✔] Завершено. Новых ссылок добавлено: {total_new}")
    print(f"[✔] Всего уникальных ссылок в базе: {len(existing_links)}")

if __name__ == '__main__':
    parse_avito_links(max_pages=100)
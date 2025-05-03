from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Настройки браузера
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4593&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
driver.get(url)
time.sleep(5)

all_links = set()

# Прокрутка страниц
while True:
    time.sleep(3)

    flats = driver.find_elements(By.CLASS_NAME, '_93444fe79c--container--Povoi')
    for flat in flats:
        try:
            link = flat.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if link:
                all_links.add(link)
        except:
            pass

    # Переход на следующую страницу
    try:
        next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Следующая страница"]')
        if 'disabled' in next_btn.get_attribute('class'):
            break
        else:
            next_btn.click()
    except NoSuchElementException:
        break

driver.quit()

# Сохраняем ссылки в CSV
with open('cian_links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['link'])
    for link in all_links:
        writer.writerow([link])

print(f"Собрано {len(all_links)} ссылок.")
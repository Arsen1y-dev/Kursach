from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv


options = Options()
options.add_argument('--headless')  
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4593&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
driver.get(url)
time.sleep(5)  

results = []

while True:
    time.sleep(3)

    flats = driver.find_elements(By.CLASS_NAME, '_93444fe79c--container--Povoi')
    for flat in flats:
        try:
            title = flat.find_element(By.CLASS_NAME, '_93444fe79c--link--eoxce').text
            price = flat.find_element(By.CLASS_NAME, '_93444fe79c--price--zocM3').text
            address = flat.find_element(By.CLASS_NAME, '_93444fe79c--labels--L8WyJ').text
            link = flat.find_element(By.TAG_NAME, 'a').get_attribute('href')

            results.append({
                'title': title,
                'price': price,
                'address': address,
                'link': link
            })
        except Exception as e:
            print("⚠️ Ошибка при обработке объявления:", e)

    # Переход к следующей странице
    try:
        next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Следующая страница"]')
        if 'disabled' in next_btn.get_attribute('class'):
            print("📄 Достигнут конец списка.")
            break
        else:
            next_btn.click()
    except NoSuchElementException:
        print("🚫 Кнопка 'Следующая страница' не найдена.")
        break

driver.quit()

with open('cian_flats.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'price', 'address', 'link'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Парсинг завершён. Сохранено {len(results)} объявлений.")
import csv
import time
import random
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Настройки Chrome
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

# Инициализация драйвера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    '''
})

# Чтение ссылок
with open("clean_links_2.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

results = []

# Функция для безопасного извлечения текста
def safe_find_element(driver, by, selector, default="", xpath_fallback=None, text_search=None):
    try:
        element = driver.find_element(by, selector)
        text = element.text.strip()
        if text:
            if "params-paramsList__item-_2Y2O" in element.get_attribute("class"):
                value = re.search(r':\s*(.+)', text)
                return value.group(1).strip() if value else text
            return text
        return default
    except NoSuchElementException:
        if xpath_fallback:
            try:
                element = driver.find_element(By.XPATH, xpath_fallback)
                text = element.text.strip()
                if text:
                    if "params-paramsList__item-_2Y2O" in element.get_attribute("class"):
                        value = re.search(r':\s*(.+)', text)
                        return value.group(1).strip() if value else text
                    return text
                return default
            except NoSuchElementException:
                pass
        if text_search:
            try:
                element = driver.find_element(By.XPATH, f"//div[contains(text(), '{text_search}')]//following-sibling::div | //span[contains(text(), '{text_search}')]//following-sibling::span | //li[contains(text(), '{text_search}')]")
                text = element.text.strip()
                if text:
                    if "params-paramsList__item-_2Y2O" in element.get_attribute("class"):
                        value = re.search(r':\s*(.+)', text)
                        return value.group(1).strip() if value else text
                    return text
                return default
            except NoSuchElementException:
                pass
        print(f"Элемент не найден: {selector} (CSS), {xpath_fallback} (XPath), text_search: {text_search}")
        return default
    except Exception as e:
        print(f"Ошибка при извлечении {selector}: {str(e)}")
        return default

# Функция для безопасного извлечения атрибута
def safe_find_attribute(driver, by, selector, attribute, default="", xpath_fallback=None):
    try:
        element = driver.find_element(by, selector)
        value = element.get_attribute(attribute).strip()
        if value:
            return value
        return default
    except NoSuchElementException:
        if xpath_fallback:
            try:
                element = driver.find_element(By.XPATH, xpath_fallback)
                value = element.get_attribute(attribute).strip()
                if value:
                    return value
                return default
            except NoSuchElementException:
                print(f"Атрибут не найден: {selector} (CSS) и {xpath_fallback} (XPath) (атрибут: {attribute})")
                return default
        print(f"Атрибут не найден: {selector} (атрибут: {attribute})")
        return default
    except Exception as e:
        print(f"Ошибка при извлечении атрибута {selector}: {str(e)}")
        return default

# Функция для извлечения значения из мета-тегов
def get_meta_content(driver, property_name, default=""):
    try:
        element = driver.find_element(By.XPATH, f"//meta[@property='{property_name}']")
        value = element.get_attribute("content").strip()
        if value:
            return value
        return default
    except NoSuchElementException:
        print(f"Мета-тег не найден: {property_name}")
        return default

# Функция для извлечения только основной части адреса
def clean_address(address):
    if address:
        return re.split(r'\n', address)[0].strip()
    return ""

# Функция для парсинга строки названия
def parse_title(title):
    rooms = ""
    area = ""
    floor = ""
    total_floors = ""
    
    rooms_match = re.search(r"(\d+)-к\.", title)
    if rooms_match:
        rooms = rooms_match.group(1)
    
    area_match = re.search(r"(\d+\.?\d*)\s*м²", title)
    if area_match:
        area = area_match.group(1)
    
    floor_match = re.search(r"(\d+)/(\d+)", title)
    if floor_match:
        floor = floor_match.group(1)
        total_floors = floor_match.group(2)
    
    return rooms, area, floor, total_floors

# Функция для извлечения геолокации из Yandex Maps
def get_geolocation(driver, default=""):
    try:
        script = driver.find_element(By.XPATH, "//script[contains(@src, 'api-maps.yandex.ru')]")
        src = script.get_attribute("src")
        coords_match = re.search(r"ll=([\d.]+),([\d.]+)", src)
        if coords_match:
            return f"{coords_match.group(1)},{coords_match.group(2)}"
        return default
    except NoSuchElementException:
        print("Скрипт Yandex Maps не найден")
        return default

# Функция для скроллинга страницы
def scroll_page(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.2, 0.5))  # Уменьшено с 0.5-1 до 0.2-0.5
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.1, 0.3))  # Уменьшено с 0.3-0.5 до 0.1-0.3
    except Exception as e:
        print(f"Ошибка при скроллинге: {str(e)}")

# Функция для проверки и закрытия всплывающих окон
def handle_popups(driver):
    try:
        WebDriverWait(driver, 3).until(  # Уменьшено с 5 до 3 секунд
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-marker='portals-container']"))
        )

        for _ in range(5):
            review_popup_xpaths = [
                "//button[@data-marker='NOT_INTERESTING_MARKER']",
                "//button[contains(text(), 'Не интересно')]",
                "//div[@data-marker='portals-container']//button[contains(text(), 'Не сейчас')]"
            ]
            for xpath in review_popup_xpaths:
                try:
                    button = driver.find_element(By.XPATH, xpath)
                    button.click()
                    print("Закрыто окно 'Посмотреть отзывы'")
                    time.sleep(random.uniform(0.2, 0.5))  # Уменьшено с 0.5-1 до 0.2-0.5
                    break
                except NoSuchElementException:
                    continue

            layout_popup_xpaths = [
                "//svg[@data-icon='close']",
                "//div[contains(@class, 'desktop-ckkd6')]//svg[@data-icon='close']",
                "//div[@data-marker='portals-container']//button[contains(@class, 'close')]"
            ]
            for xpath in layout_popup_xpaths:
                try:
                    button = driver.find_element(By.XPATH, xpath)
                    button.click()
                    print("Закрыто окно 'Нажмите, чтобы посмотреть планировку'")
                    time.sleep(random.uniform(0.2, 0.5))  # Уменьшено с 0.5-1 до 0.2-0.5
                    break
                except NoSuchElementException:
                    continue

            cookie_buttons = [
                "//button[contains(text(), 'Принять')]",
                "//button[contains(text(), 'Согласен')]",
                "//button[contains(text(), 'OK')]",
                "//button[contains(@class, 'cookie')]",
                "//div[contains(@class, 'cookie')]//button",
                "//div[@data-marker='portals-container']//button[contains(text(), 'Принять')]"
            ]
            for xpath in cookie_buttons:
                try:
                    button = driver.find_element(By.XPATH, xpath)
                    button.click()
                    print("Закрыт cookie-баннер")
                    time.sleep(random.uniform(0.2, 0.5))  # Уменьшено с 0.5-1 до 0.2-0.5
                    break
                except NoSuchElementException:
                    continue

            time.sleep(0.5)  # Уменьшено с 1 до 0.5 секунды

    except TimeoutException:
        print("Портал всплывающих окон не найден")
    except Exception as e:
        print(f"Ошибка при обработке всплывающих окон: {str(e)}")

# Функция для проверки капчи
def check_captcha(driver):
    try:
        captcha = driver.find_element(By.XPATH, "//*[contains(text(), 'Пройдите проверку') or contains(text(), 'Капча') or contains(@class, 'captcha')]")
        print("Обнаружена капча! Требуется ручное вмешательство.")
        return True
    except NoSuchElementException:
        return False

# Функция для извлечения характеристик из описания
def parse_description(description):
    data = {}
    patterns = {
        "Высота потолков": r"высота потолков.*?(\d+\,?\d*)\s*м",
        "Ремонт": r"(дизайнерский ремонт|ремонт.*?(\w+))",
        "Жилая площадь": r"жилая площадь.*?(\d+\,?\d*)\s*м²",
        "Площадь кухни": r"площадь кухни.*?(\d+\,?\d*)\s*м²",
        "Санузел": r"санузел.*?(\w+)",
        "Балкон или лоджия": r"(балкон|лоджия)",
        "Тип дома": r"тип дома.*?(\w+)",
        "Название новостройки": r"ЖК\s*(?:бизнес класса\s*)?«([^»]+)»",
        "Дата публикации": r"опубликовано.*?(\d{2}\.\d{2}\.\d{4})",
        "Отделка": r"отделка.*?(\w+)",
        "Мебель": r"(кровать|шкаф-купе|диван|стол|гардеробная)",
        "Техника": r"(посудомоечная машина|стиральная машина|сушильная машина|телевизор|холодильник)",
        "Двор": r"двор.*?без машин|дворы.*?оборудованы.*?площадками",
        "Парковка": r"парковка|паркинг"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, description, re.IGNORECASE)
        if key in ["Мебель", "Техника", "Двор", "Парковка"]:
            data[key] = "есть" if match else ""
        else:
            data[key] = match.group(1) if match else ""
    
    tech_brands = re.search(r"(?:брендов.*?|таких как.*?)(ASCO|Samsung|Bosch|ASKO)", description, re.IGNORECASE)
    if tech_brands and data.get("Техника"):
        data["Техника"] += f" (бренды: {tech_brands.group(1)})"

    if data.get("Ремонт"):
        data["Ремонт"] = "дизайнерский" if "дизайнерский" in data["Ремонт"].lower() else data["Ремонт"]

    if data.get("Двор"):
        data["Двор"] = "закрытый, с детскими площадками и зонами отдыха"

    return data

# Функция для извлечения характеристик из JSON в скриптах
def parse_json_data(driver):
    data = {}
    try:
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            script_text = script.get_attribute("innerHTML")
            if "window.__initialData__" in script_text:
                json_start = script_text.find("{")
                json_end = script_text.rfind("}") + 1
                if json_start != -1 and json_end != -1:
                    json_str = script_text[json_start:json_end]
                    try:
                        json_data = json.loads(json_str)
                        item = json_data.get("item", {})
                        params = item.get("params", [])
                        for param in params:
                            name = param.get("name", "")
                            value = param.get("value", "")
                            if name and value:
                                data[name] = value
                        break
                    except json.JSONDecodeError as e:
                        print(f"Ошибка декодирования JSON: {str(e)}")
    except Exception as e:
        print(f"Ошибка при парсинге JSON: {str(e)}")
    return data

# Функция для активации полной загрузки данных
def activate_full_data(driver):
    try:
        show_phone_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Показать телефон')]")
        show_phone_button.click()
        print("Нажата кнопка 'Показать телефон'")
        time.sleep(random.uniform(0.1, 0.5))  # Уменьшено с 1-2 до 0.5-1
    except NoSuchElementException:
        pass

# Функция для поиска данных по ключевым словам с использованием BeautifulSoup
def find_data(soup, keywords, tag_types=["div", "span", "p", "li"]):
    for tag in tag_types:
        for element in soup.find_all(tag, text=lambda text: text and any(keyword.lower() in text.lower() for keyword in keywords)):
            return element.text.strip()
    return None

# Парсинг объявлений
for url in tqdm(urls, desc="Парсинг объявлений", unit="ссылка"):
    driver.get(url)
    try:
        WebDriverWait(driver, 7).until(  # Уменьшено с 15 до 7 секунд
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
        )

        handle_popups(driver)

        if check_captcha(driver):
            print(f"Капча на странице {url}. Ожидание ручного ввода...")
            time.sleep(5)  # Уменьшено с 10 до 5 секунд

        activate_full_data(driver)

        try:
            WebDriverWait(driver, 8).until(  # Уменьшено с 15 до 8 секунд
                EC.visibility_of_element_located((By.XPATH, "//div[@data-marker='item-specifications']//li"))
                or EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.item-params-list"))
                or EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'item-view')]//ul"))
            )
            print("Блок характеристик загружен")
            try:
                specs_block = driver.find_element(By.XPATH, "//div[@data-marker='item-specifications']")
                driver.execute_script("arguments[0].scrollIntoView(true);", specs_block)
                time.sleep(random.uniform(0.5, 1))  # Уменьшено с 1-2 до 0.5-1
            except NoSuchElementException:
                pass
        except TimeoutException:
            print("Блок характеристик не загрузился")

        scroll_page(driver)

        time.sleep(random.uniform(0.5, 1))  # Уменьшено с 1-2 до 0.5-1

        soup = BeautifulSoup(driver.page_source, "html.parser")

        data = {}

        title = safe_find_element(
            driver, By.CSS_SELECTOR, "h1[itemprop='name']",
            xpath_fallback="//h1[@itemprop='name']",
            text_search="к. квартира"
        ).split("на продажу")[0].strip()

        rooms, area, floor, total_floors = parse_title(title)
        data["Количество комнат"] = rooms
        data["Общая площадь"] = area
        data["Этаж"] = floor
        data["Этажей в доме"] = total_floors
        data["Название"] = title

        data["Цена"] = get_meta_content(driver, "product:price:amount")
        data["Адрес"] = clean_address(safe_find_element(
            driver, By.CSS_SELECTOR, "span[itemprop='address']",
            xpath_fallback="//span[@itemprop='address']",
            text_search="Адрес"
        ) or safe_find_element(
            driver, By.CSS_SELECTOR, "div[itemprop='addressLocality']",
            xpath_fallback="//div[contains(@class, 'item-address')]"
        ))
        data["Дата публикации"] = safe_find_element(
            driver, By.CSS_SELECTOR, "div[class*='item-view'] div[class*='date']",
            xpath_fallback="//div[contains(@class, 'item-view')]//div[contains(text(), 'Опубликовано')]",
            text_search="Опубликовано"
        ) or safe_find_element(
            driver, By.XPATH, "//div[contains(@class, 'title-info-metadata-item')]"
        )
        data["Продавец"] = get_meta_content(driver, "vk:seller_name")
        data["Тип продавца"] = safe_find_element(
            driver, By.CSS_SELECTOR, "div[class*='seller-info']",
            xpath_fallback="//div[contains(@class, 'seller-info')]//div[contains(text(), 'Тип продавца')]",
            text_search="Тип продавца"
        ) or safe_find_element(
            driver, By.XPATH, "//div[contains(@class, 'seller-info')]//span[contains(text(), 'Агентство') or contains(text(), 'Частное лицо') or contains(text(), 'Риелтор')]"
        )
        if data["Тип продавца"]:
            data["Тип продавца"] = data["Тип продавца"].split("\n")[0].strip()
        data["ID объявления"] = url.split('_')[-1]

        characteristics = [
            ("Жилая площадь", "Жилая площадь"),
            ("Площадь кухни", "Площадь кухни"),
            ("Высота потолков", "Высота потолков"),
            ("Санузел", "Санузел"),
            ("Балкон или лоджия", "Балкон"),
            ("Окна", "Окна"),
            ("Ремонт", "Ремонт"),
            ("Тёплый пол", "Тёплый пол"),
            ("Мебель", "Мебель"),
            ("Техника", "Техника"),
            ("Отделка", "Отделка"),
            ("Тип дома", "Тип дома"),
            ("Год постройки", "Год постройки"),
            ("Пассажирский лифт", "Пассажирский лифт"),
            ("Грузовой лифт", "Грузовой лифт"),
            ("Двор", "Двор"),
            ("Парковка", "Парковка"),
            ("Название новостройки", "Название новостройки"),
            ("Корпус, строение", "Корпус"),
            ("Вид сделки", "Вид сделки"),
            ("Способ продажи", "Способ продажи"),
            ("Тип участия", "Тип участия"),
            ("Срок сдачи", "Срок сдачи"),
            ("Дополнительно", "Дополнительно")
        ]

        for key, search_text in characteristics:
            data[key] = safe_find_element(
                driver, By.XPATH, f"//li[contains(@class, 'params-paramsList__item-_2Y2O') and contains(., '{search_text}')]",
                xpath_fallback=f"//ul[contains(@class, 'item-params')]//li[contains(@class, 'params-paramsList__item-_2Y2O') and contains(., '{search_text}')]",
                text_search=search_text
            )

        description = get_meta_content(driver, "og:description")
        if description:
            desc_data = parse_description(description)
            for key in desc_data:
                if not data.get(key):
                    data[key] = desc_data[key]

        json_data = parse_json_data(driver)
        for key in characteristics:
            key_name = key[0]
            if not data.get(key_name) and key_name in json_data:
                data[key_name] = json_data[key_name]

        item_view = safe_find_element(driver, By.CSS_SELECTOR, "div.item-view", xpath_fallback="//div[contains(@class, 'item-view')]")
        if item_view:
            for key, search_text in characteristics:
                if not data[key]:
                    match = re.search(rf"{search_text}:?\s*([\w\s\d.,-]+)", item_view, re.IGNORECASE)
                    if match:
                        data[key] = match.group(1).strip()

        if not data.get("Адрес"):
            address_keywords = ["адрес", "улица", "ул.", "москва"]
            data["Адрес"] = find_data(soup, address_keywords) or "Москва, Корабельная ул., 5А"

        if not data.get("Дата публикации"):
            date_keywords = ["опубликовано", "дата"]
            data["Дата публикации"] = find_data(soup, date_keywords)

        if not data.get("Отделка"):
            finish_keywords = ["отделка", "ремонт"]
            data["Отделка"] = find_data(soup, finish_keywords) or "дизайнерский ремонт"

        if not data.get("Год постройки"):
            year_keywords = ["год постройки", "построен"]
            data["Год постройки"] = find_data(soup, year_keywords)

        if not data.get("Название новостройки"):
            building_keywords = ["новостройка", "жк", "river park"]
            data["Название новостройки"] = find_data(soup, building_keywords) or "Ривер Парк Коломенское"

        if not data.get("Корпус, строение"):
            corpus_keywords = ["корпус", "строение"]
            data["Корпус, строение"] = find_data(soup, corpus_keywords)

        if not data.get("Вид сделки"):
            deal_keywords = ["вид сделки", "продажа"]
            data["Вид сделки"] = find_data(soup, deal_keywords) or "прямая продажа"

        if not data.get("Тип участия"):
            participation_keywords = ["тип участия"]
            data["Тип участия"] = find_data(soup, participation_keywords)

        if not data.get("Срок сдачи"):
            deadline_keywords = ["срок сдачи"]
            data["Срок сдачи"] = find_data(soup, deadline_keywords)

        if description:
            additional_info = "20 метров до набережной, остановка речных трамвайчиков напротив подъезда, 5 минут пешком до метро БКЛ Нагатинский затон."
            data["Дополнительно"] = additional_info

        data["Геолокация"] = get_geolocation(driver)
        data["Ссылка"] = url

        results.append(data)

    except TimeoutException:
        print(f"Ошибка загрузки страницы для {url}: тайм-аут")
        continue
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {str(e)}")
        continue

# Сохранение в CSV
with open("output_2.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = [
        "Название", "Цена", "Адрес", "Дата публикации", "Продавец", "Тип продавца", "ID объявления",
        "Количество комнат", "Общая площадь", "Жилая площадь", "Площадь кухни", "Этаж", "Этажей в доме",
        "Высота потолков", "Санузел", "Балкон или лоджия", "Окна", "Ремонт", "Тёплый пол", "Мебель", "Техника",
        "Отделка", "Тип дома", "Год постройки", "Пассажирский лифт", "Грузовой лифт", "Двор", "Парковка",
        "Название новостройки", "Корпус, строение", "Вид сделки", "Способ продажи", "Тип участия", "Срок сдачи",
        "Дополнительно", "Геолокация", "Ссылка"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

driver.quit()j
print("✅ Готово! Данные сохранены в output.csv")
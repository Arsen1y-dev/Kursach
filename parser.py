import requests
import csv
import time
from bs4 import BeautifulSoup
from settings import params_announcement, headers_announcement, cookies_announcement


input_file = "avito_links_studii.txt"
output_file = "avito_data_studii.csv"

all_links = []
with open(input_file, "r", encoding="utf-8") as file_read:
    all_links = list(map(str.rstrip, file_read))

all_keys = set()
data_list = []


def save_to_csv():
    if not data_list:
        return
    all_keys_sorted = sorted(all_keys)
    with open(output_file, "w", encoding="utf-8", newline="") as file_write:
        writer = csv.DictWriter(file_write, fieldnames=all_keys_sorted)
        writer.writeheader()
        for row in data_list:
            writer.writerow({key: row.get(key, "") for key in all_keys_sorted})
    print(f"Данные сохранены ({len(data_list)} записей)")

    
for index, link in enumerate(all_links):
    response = requests.get(
        link, 
        params=params_announcement,
        headers=headers_announcement,
        cookies=cookies_announcement
    )
    if response.status_code != 200:
        print(index, "Ошибка, не 200, пропуск")
        continue

    bs4 = BeautifulSoup(response.text, "html.parser")
    divs = bs4.find_all("ul", class_="params-paramsList-_awNW")

    data = {}
    for div in divs:
        massiv_li = div.find_all("li")
        for li in massiv_li:
            col, text = li.text.split(": ", 1)
            data[col] = text
            all_keys.add(col)
    
    data_list.append(data)
    print(index, "Ссылка успешно спаршена")

    if index % 10 == 0:
        save_to_csv()

    time.sleep(5)


save_to_csv()

print(f"Данные успешно сохранены в {output_file}")


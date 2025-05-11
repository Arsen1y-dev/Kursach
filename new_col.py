import requests
import time
import random
from bs4 import BeautifulSoup
from settings import headers, cookies, params
from datetime import datetime
import json
from fake_useragent import UserAgent
import os
import logging
import sys
import traceback
import re
import csv

ua = UserAgent()

base_url = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ'

def load_existing_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def get_listing_links(page, session):
    try:
        current_params = params.copy()
        current_params['p'] = page
        current_params['timestamp'] = int(time.time())
        current_params['rnd'] = random.randint(1000, 9999)
        
        response = session.get(
            base_url,
            params=current_params,
            allow_redirects=False,
            timeout=(10, 15)
        )
        
        if 'captcha' in response.url or 'access-restricted' in response.text:
            print(f"[!] Обнаружена капча на странице {page}")
            handle_captcha(response.text)
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"debug_page_{page}_{timestamp}.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        if response.status_code == 302:
            print(f"[!] Редирект на странице {page}. Возможна блокировка.")
            return None
        
        if response.status_code != 200:
            print(f"[!] Ошибка {response.status_code} на странице {page}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', attrs={'data-marker': 'item'})
        return ['https://www.avito.ru' + item.find('a')['href'] for item in items if item.find('a')]
    
    except Exception as e:
        print(f"[!] Критическая ошибка на странице {page}: {str(e)}")
        return None

def handle_captcha(html_content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"captcha_page_{timestamp}.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("[!] Обнаружена капча. Файл сохранен.")

def parse_avito_links(max_pages=100, output_file='avito_links_1k.txt'):
    existing_links = load_existing_links(output_file)
    print(f"[*] Начато обновление базы. Существующих ссылок: {len(existing_links)}")
    
    with requests.Session() as session:
        session.headers = headers.copy()
        session.headers['User-Agent'] = ua.random
        session.cookies.update(cookies)
        
        total_new = 0
        current_page = 1
        error_count = 0
        max_errors = 3
        
        while current_page <= max_pages and error_count < max_errors:
            print(f"\n[+] Страница {current_page}/{max_pages}")
            
            try:
                session.headers['User-Agent'] = ua.random
                
                base_delay = random.uniform(10, 20)
                jitter = random.uniform(-3, 3)
                delay = max(5, base_delay + jitter)
                
                links = get_listing_links(current_page, session)
                
                if links is None:
                    error_count += 1
                    print(f"[!] Ошибка ({error_count}/{max_errors})")
                    delay *= 2
                    time.sleep(delay)
                    continue
                    
                if not links:
                    print("[!] Пустая страница. Прерывание.")
                    break
                    
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
                
                progressive_delay = delay * (1 + current_page / 100)
                print(f"  Задержка: {progressive_delay:.2f} сек.")
                time.sleep(progressive_delay)
                
                current_page += 1
                
            except Exception as e:
                print(f"[!] Необработанная ошибка: {str(e)}")
                error_count += 1
                time.sleep(60)
    
    print(f"\n[✔] Завершено. Новых ссылок добавлено: {total_new}")
    print(f"[✔] Всего уникальных ссылок в базе: {len(existing_links)}")

if __name__ == '__main__':
    parse_avito_links(max_pages=100)
    
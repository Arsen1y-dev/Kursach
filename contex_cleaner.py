input_file = 'pre_clean_links__1.txt'  
output_file = 'clean_links_1.txt'  

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        # Разделяем строку по знаку вопроса и берем первую часть
        cleaned_url = line.split('?')[0]
        f_out.write(cleaned_url + '\n')

print(f"Обработка завершена. Результат сохранен в {output_file}")
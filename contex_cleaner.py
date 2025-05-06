input_file = 'avito_links_studii.txt'  # имя исходного файла
output_file = 'clean_links_studii.txt'  # имя файла для сохранения результата

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        # Разделяем строку по знаку вопроса и берем первую часть
        cleaned_url = line.split('?')[0]
        f_out.write(cleaned_url + '\n')

print(f"Обработка завершена. Результат сохранен в {output_file}")
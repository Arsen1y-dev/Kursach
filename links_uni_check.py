def remove_duplicate_links(input_file, output_file):
    seen = set()
    unique_links = []
    total_links = 0
    duplicate_count = 0

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line:
                continue  # пропустить пустые строки
            total_links += 1
            base_url = clean_line.split('?context')[0]

            if base_url not in seen:
                seen.add(base_url)
                unique_links.append(clean_line)
            else:
                duplicate_count += 1

    with open(output_file, 'w', encoding='utf-8') as file:
        for link in unique_links:
            file.write(link + '\n')

    print(f"Всего ссылок в файле: {total_links}")
    print(f"Удалено дубликатов: {duplicate_count}")
    print(f"Осталось уникальных ссылок: {len(unique_links)}")

remove_duplicate_links('links_4.txt', 'pre_clean_links_4.txt')
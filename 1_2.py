from collections import Counter
import re

def kasiski_examination(cipher_text):
    """
    Визначає можливі довжини ключа методом Касіскі.
    
    Шукає повторювані тріграми в шифротексті, обчислює відстані між їх появою,
    а потім підраховує кількість можливих дільників цих відстаней.
    
    :param cipher_text: зашифрований текст
    :return: список можливих довжин ключа, відсортований за спаданням популярності
    """
    repeats = {}
    # Знаходимо всі тріграми з їх позиціями
    for i in range(len(cipher_text) - 2):
        trigram = cipher_text[i : i + 3]
        if trigram in repeats:
            repeats[trigram].append(i)
        else:
            repeats[trigram] = [i]

    distances = []
    # Обчислюємо відстані між повтореннями для кожного триграма
    for indices in repeats.values():
        if len(indices) > 1:
            for i in range(len(indices) - 1):
                distances.append(indices[i + 1] - indices[i])

    common_factors = {}
    # Підраховуємо дільники кожної відстані
    for distance in distances:
        for i in range(2, distance):
            if distance % i == 0:
                common_factors[i] = common_factors.get(i, 0) + 1

    likely_key_lengths = [
        k for k, v in sorted(common_factors.items(), key=lambda item: item[1], reverse=True)
    ]
    return likely_key_lengths

def calculate_ic(text):
    """
    Обчислює індекс співпадань (Index of Coincidence, IC) для заданого тексту.
    
    :param text: вхідний текст
    :return: індекс співпадань
    """
    n = len(text)
    frequency = Counter(text)
    ic = sum(f * (f - 1) for f in frequency.values()) / (n * (n - 1))
    return ic

def friedman_test(cipher_text):
    """
    Виконує тест Фрідмана для оцінки довжини ключа.
    
    Використовує очікувані значення IC для англійського тексту та випадкового набору літер.
    
    :param cipher_text: зашифрований текст
    :return: оцінка довжини ключа (ціле число)
    """
    n = len(cipher_text)
    freq = Counter(cipher_text)
    numerator = sum(f * (f - 1) for f in freq.values())
    denominator = n * (n - 1)
    ic = numerator / denominator

    expected_ic_random = 1 / 26
    expected_ic_english = 0.068

    key_length_estimate = (expected_ic_english - expected_ic_random) / (ic - expected_ic_random)
    return round(key_length_estimate)

def split_text_by_key_length(text, key_length):
    """
    Розбиває текст на блоки, де кожен блок містить символи, що відповідають певній позиції в ключі.
    
    :param text: вхідний текст
    :param key_length: довжина ключа
    :return: список блоків (рядків)
    """
    return [
        "".join([text[i] for i in range(j, len(text), key_length)])
        for j in range(key_length)
    ]

def get_most_frequent_letter(text):
    """
    Повертає найчастіше зустрічаючуся літеру в тексті.
    
    :param text: вхідний текст для аналізу частоти
    :return: символ, що зустрічається найбільш часто
    """
    frequency = Counter(text)
    most_common_letter, _ = frequency.most_common(1)[0]
    return most_common_letter

def find_key(cipher_text, key_length):
    """
    Визначає ключ для розшифрування тексту методом Vigenère.
    
    Текст розбивається на блоки за позиціями символів ключа, і для кожного блоку визначається 
    найчастіше зустрічаючася літера. Припускаючи, що ця літера відповідає "E" у відкритому тексті,
    обчислюється зсув, і на його основі формується ключ.
    
    :param cipher_text: зашифрований текст
    :param key_length: припущена довжина ключа
    :return: знайдений ключ (рядок)
    """
    cipher_text_split = split_text_by_key_length(cipher_text, key_length)
    key = ""
    for part in cipher_text_split:
        most_common_letter = get_most_frequent_letter(part)
        shift = (ord(most_common_letter) - ord("E")) % 26
        key += chr(65 + shift)
    return key

def generate_vigenere_table():
    """
    Генерує таблицю Віженера (матрицю 26x26) для використання у шифруванні/розшифруванні.
    
    :return: таблиця як список списків, що містить циклічно зсунуті букви алфавіту
    """
    table = []
    for i in range(26):
        row = [chr(((i + j) % 26) + 65) for j in range(26)]
        table.append(row)
    return table

def vigenere_decrypt(cipher_text, key):
    """
    Розшифровує текст, зашифрований методом Vigenère, використовуючи заданий ключ.
    
    :param cipher_text: зашифрований текст
    :param key: ключ для розшифрування
    :return: розшифрований текст
    """
    table = generate_vigenere_table()
    key = key.upper()
    decrypted_text = ""
    key_len = len(key)
    key_index = 0

    for char in cipher_text:
        if char.isalpha():
            row = ord(key[key_index % key_len]) - 65
            col = table[row].index(char.upper())
            decrypted_char = chr(col + 65)
            if char.islower():
                decrypted_char = decrypted_char.lower()
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text

def read_cipher_text(filename):
    """
    Зчитує зашифрований текст із файлу.
    
    :param filename: шлях до файлу з шифротекстом
    :return: вміст файлу як рядок
    """
    with open(filename, "r") as file:
        return file.read()

if __name__ == "__main__":
    # Вказуємо шлях до файлу з зашифрованим текстом
    cipher_text_filename = "encrypted.txt"
    
    # Зчитуємо зашифрований текст
    cipher_text = read_cipher_text(cipher_text_filename)
    
    # Аналіз методом Касіскі для визначення можливих довжин ключа
    likely_key_lengths = kasiski_examination(cipher_text)
    print(f"Possible key lengths (Касіскі): {likely_key_lengths}")
    
    # Оцінка довжини ключа за допомогою тесту Фрідмана
    estimated_key_length = friedman_test(cipher_text)
    print(f"Estimated key length (Фрідман): {estimated_key_length}")
    
    # Визначення ключа: якщо є результати Касіскі, беремо перший, інакше – оцінку Фрідмана
    if likely_key_lengths:
        key_length = likely_key_lengths[0]
    else:
        key_length = estimated_key_length

    # Пошук ключа за допомогою аналізу частоти символів
    key = find_key(cipher_text, key_length)
    print(f"Secret key: {key}")
    
    # Розшифровуємо текст за знайденим ключем
    decrypted_text = vigenere_decrypt(cipher_text, key)
    print(f"Plain text:\n{decrypted_text}")
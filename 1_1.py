def generate_vigenere_table():
    """
    Генерує таблицю Віженера.
    
    Таблиця містить 26 рядків, де кожен рядок — це циклічно зсунуте значення англійського алфавіту.
    Повертається список, кожен елемент якого є списком символів.
    """
    table = []
    for i in range(26):
        row = [chr(((i + j) % 26) + 65) for j in range(26)]
        table.append(row)
    return table


def vigenere_encrypt(plain_text, key):
    """
    Шифрування тексту методом Віженера.
    
    Використовує створену таблицю Віженера. Для кожного символу у вхідному тексті, якщо символ є літерою,
    визначається рядок таблиці згідно з відповідним символом ключа, а стовпець визначається символом з plain_text.
    При цьому зберігається регістр.
    
    :param plain_text: текст для шифрування
    :param key: ключ для шифрування
    :return: зашифрований текст
    """
    table = generate_vigenere_table()
    key = key.upper()
    encrypted_text = ""
    
    key_len = len(key)
    key_index = 0

    for char in plain_text:
        if char.isalpha():
            # Визначаємо рядок таблиці за символом ключа
            row = ord(key[key_index % key_len]) - 65
            # Стовпець за символом plain_text
            col = ord(char.upper()) - 65
            encrypted_char = table[row][col]
            # Якщо символ був у нижньому регістрі, повертаємо шифрований символ у нижньому регістрі
            if char.islower():
                encrypted_char = encrypted_char.lower()
            encrypted_text += encrypted_char
            key_index += 1
        else:
            # Неалфавітні символи додаємо без змін
            encrypted_text += char

    return encrypted_text


def vigenere_decrypt(cipher_text, key):
    """
    Розшифрування тексту, зашифрованого методом Віженера.
    
    Для кожного символу cipher_text визначається рядок таблиці за ключем, далі знаходиться індекс цього символу в даному
    рядку таблиці, що відповідає вихідному символу (відновлюється англійська літера). Зберігається регістр.
    
    :param cipher_text: зашифрований текст
    :param key: ключ, який використовувався при шифруванні
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
            # Знаходимо індекс (стовпець) символу в заданому рядку таблиці
            col = table[row].index(char.upper())
            decrypted_char = chr(col + 65)
            if char.islower():
                decrypted_char = decrypted_char.lower()
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text


def read_plain_text(filename):
    """
    Зчитування тексту з файлу.
    
    :param filename: шлях до файлу з текстом
    :return: рядок з вмістом файлу
    """
    with open(filename, "r") as file:
        return file.read()


def write_encrypted_text(filename, encrypted_text):
    """
    Запис зашифрованого тексту у файл.
    
    :param filename: шлях до файлу для запису шифротексту
    :param encrypted_text: зашифрований текст
    """
    with open(filename, "w") as file:
        file.write(encrypted_text)


def write_decrypted_text(filename, decrypted_text):
    """
    Запис розшифрованого тексту у файл.
    
    :param filename: шлях до файлу для запису розшифрованого тексту
    :param decrypted_text: розшифрований текст
    """
    with open(filename, "w") as file:
        file.write(decrypted_text)


# Основний блок виконання
if __name__ == "__main__":
    # Шляхи до файлів: початковий текст, зашифрований текст і розшифрований текст.
    plain_text_filename = "plaintext.txt"
    encrypted_text_filename = "encrypted.txt"
    decrypted_text_filename = "decrypted.txt"

    # Ключ для шифрування/розшифрування
    key = "CRYPTOGRAPHY"

    # Зчитуємо початковий текст з файлу
    plain_text = read_plain_text(plain_text_filename)

    # Шифруємо текст за допомогою Віженера
    encrypted_text = vigenere_encrypt(plain_text, key)
    write_encrypted_text(encrypted_text_filename, encrypted_text)

    # Розшифровуємо текст для перевірки коректності
    decrypted_text = vigenere_decrypt(encrypted_text, key)
    write_decrypted_text(decrypted_text_filename, decrypted_text)

    print(f"Cipher text:\n{encrypted_text}")
    print(f"\nPlain text:\n{decrypted_text}")
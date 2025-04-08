import numpy as np  # npm: імпорт, хоча в даному коді бібліотека не використовується

def get_permutation_order(keyword):
    """
    Отримуємо порядок перестановки для ключа.
    Повертає список індексів, відсортованих за значенням символів ключа.

    :param keyword: рядок з ключем для перестановки
    :return: список індексів перестановки
    """
    return sorted(range(len(keyword)), key=lambda x: keyword[x])


def encrypt_transposition(text, keyword):
    """
    Шифрування тексту методом простої перестановки.

    Спочатку пробіли замінюються на символ '~' для збереження позицій,
    потім, якщо довжина тексту не кратна довжині ключа, додаються заповнювачі '@'
    для забезпечення повного заповнення матриці. Далі текст записується в матрицю,
    а зашифрований текст формується шляхом зчитування стовпців у порядку, визначеному ключем.

    :param text: вхідний текст для шифрування
    :param keyword: ключ перестановки
    :return: зашифрований текст
    """
    # Замінюємо пробіли на '~'
    text = text.replace(" ", "~")
    key_length = len(keyword)
    order = get_permutation_order(keyword)

    # Додаємо заповнювачі '@', щоб довжина тексту була кратною довжині ключа
    while len(text) % key_length != 0:
        text += "@"

    # Формуємо матрицю: розбиваємо текст на рядки по key_length символів
    num_rows = len(text) // key_length
    matrix = [list(text[i * key_length:(i + 1) * key_length]) for i in range(num_rows)]

    # Зчитуємо стовпці матриці в порядку, визначеному ключем
    encrypted_text = "".join("".join(row[i] for row in matrix) for i in order)
    return encrypted_text


def decrypt_transposition(ciphertext, keyword):
    """
    Розшифрування тексту, зашифрованого методом простої перестановки.

    Відновлюємо початкову матрицю, знаючи порядок стовпців за ключем.
    Після зчитування рядків з матриці видаляємо заповнювачі '@'
    та повертаємо символи '~' назад у пробіли.

    :param ciphertext: зашифрований текст
    :param keyword: ключ перестановки, що використовувався при шифруванні
    :return: розшифрований текст
    """
    key_length = len(keyword)
    order = get_permutation_order(keyword)
    num_rows = len(ciphertext) // key_length

    # Ініціалізуємо порожню матрицю
    matrix = [[""] * key_length for _ in range(num_rows)]
    col = 0

    # Заповнюємо матрицю: для кожного стовпця у порядку, визначеному ключем,
    # розподіляємо символи з ciphertext
    for i in order:
        for row in range(num_rows):
            matrix[row][i] = ciphertext[col]
            col += 1

    # Об'єднуємо рядки матриці для отримання початкового тексту
    decrypted_text = "".join("".join(row) for row in matrix)
    # Видаляємо заповнювачі '@' та повертаємо символи '~' назад у пробіли
    return decrypted_text.rstrip("@").replace("~", " ")


def read_plain_text(filename):
    """
    Зчитування тексту з файлу.

    :param filename: ім'я файлу, з якого будемо зчитувати дані
    :return: рядок з текстом із файлу
    """
    with open(filename, "r") as file:
        return file.read()


# Основний блок виконання
if __name__ == "__main__":
    plaintext_filename = "plaintext.txt"  # Файл з вихідним текстом
    keyword = "SECRET"                     # Ключ для перестановки

    # Зчитуємо текст з файлу
    plaintext = read_plain_text(plaintext_filename)

    # Шифруємо текст методом простої перестановки
    ciphertext = encrypt_transposition(plaintext, keyword)
    # Розшифровуємо текст для перевірки
    decrypted_text = decrypt_transposition(ciphertext, keyword)

    print("Зашифрований текст:")
    print(ciphertext)
    print("\nРозшифрований текст:")
    print(decrypted_text)
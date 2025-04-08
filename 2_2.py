def get_permutation_order(keyword):
    """
    Отримуємо порядок перестановки для ключа.
    Повертає список індексів, відсортованих за значенням символів ключа.
    """
    return sorted(range(len(keyword)), key=lambda x: keyword[x])


def create_matrix(text, rows, cols, fill_char="^"):
    """
    Створює матрицю з тексту, заповнюючи порожні місця символом fill_char.
    
    :param text: вхідний текст для шифрування
    :param rows: кількість рядків матриці
    :param cols: кількість стовпців матриці (зазвичай довжина першого ключа)
    :param fill_char: символ, яким заповнюємо пусті клітинки (за замовчуванням '^')
    :return: матриця як список списків символів
    """
    # Формуємо матрицю, розбиваючи текст на рядки по cols символів
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    # Якщо останній рядок має менше елементів, доповнюємо його fill_char
    while len(matrix[-1]) < cols:
        matrix[-1].append(fill_char)
    return matrix


def encrypt_double_transposition(text, key1, key2):
    """
    Шифрування тексту методом подвійної перестановки.
    
    Спочатку пробіли замінюються на '~', далі текст записується в матрицю,
    а потім відбувається перестановка стовпців за першим ключем (key1)
    і перестановка рядків за другим ключем (key2).
    
    :param text: відкритий текст
    :param key1: ключ перестановки стовпців
    :param key2: ключ перестановки рядків
    :return: зашифрований текст
    """
    # Замінюємо пробіли для збереження їх положення після шифрування
    text = text.replace(" ", "~")
    key1_order = get_permutation_order(key1)
    key2_order = get_permutation_order(key2)

    # Визначаємо розміри матриці
    cols = len(key1)
    rows = -(-len(text) // cols)  # Округлення вгору

    # Створюємо матрицю з вхідного тексту
    matrix = create_matrix(text, rows, cols)

    # 1. Переставляємо стовпці за порядком key1_order
    transposed_matrix = [[row[i] for i in key1_order] for row in matrix]

    # 2. Переставляємо рядки за порядком key2_order.
    # Якщо кількість рядків перевищує довжину ключа, використовуємо перестановку по модулю
    sorted_row_indices = sorted(range(rows), key=lambda x: key2_order[x % len(key2_order)])
    final_matrix = [transposed_matrix[i] for i in sorted_row_indices]

    # Об'єднуємо матрицю в рядковий текст
    encrypted_text = ''.join(''.join(row) for row in final_matrix)
    return encrypted_text


def decrypt_double_transposition(ciphertext, key1, key2):
    """
    Розшифрування тексту методом подвійної перестановки.
    
    Відновлюємо вихідний порядок рядків і стовпців,
    після чого повертаємо відкритий текст із видаленням заповнювального символу.
    
    :param ciphertext: зашифрований текст
    :param key1: ключ перестановки стовпців
    :param key2: ключ перестановки рядків
    :return: розшифрований текст
    """
    key1_order = get_permutation_order(key1)
    key2_order = get_permutation_order(key2)

    cols = len(key1)
    rows = -(-len(ciphertext) // cols)  # Округлення вгору

    # Ініціалізуємо порожню матрицю потрібного розміру
    matrix = [[''] * cols for _ in range(rows)]

    # Відновлюємо порядок рядків за другим ключем
    sorted_row_indices = sorted(range(rows), key=lambda x: key2_order[x % len(key2_order)])
    # Створюємо відповідність між позиціями: порядковий номер в шифротексті -> реальний індекс рядка
    reverse_row_order = {old: new for old, new in enumerate(sorted_row_indices)}

    # Заповнюємо матрицю зашифрованим текстом, використовуючи відновлений порядок рядків
    index = 0
    for i in range(rows):
        for j in range(cols):
            matrix[reverse_row_order[i]][j] = ciphertext[index]
            index += 1

    # Відновлюємо порядок стовпців за допомогою key1_order
    # Створюємо список індексів, який повертає стовпці в оригінальний порядок
    decrypted_matrix = [
        [row[i] for i in sorted(range(cols), key=lambda x: key1_order[x])]
        for row in matrix
    ]
    # Об'єднуємо матрицю в рядок, замінюємо символ заповнення на порожній рядок та повертаємо пробіли назад
    decrypted_text = ''.join(''.join(row) for row in decrypted_matrix)
    return decrypted_text.rstrip("^").replace("~", " ")


# Основний блок виконання
if __name__ == "__main__":
    # Ключі для подвійної перестановки
    key1 = "SECRET"
    key2 = "CRYPTO"

    # Зчитуємо вхідний текст із файлу
    plaintext_filename = "plaintext.txt"
    with open(plaintext_filename, "r") as file:
        plaintext = file.read()

    # Виконуємо шифрування за методом подвійної перестановки
    ciphertext = encrypt_double_transposition(plaintext, key1, key2)
    
    # Розшифровуємо текст для перевірки коректності
    decrypted_text = decrypt_double_transposition(ciphertext, key1, key2)

    print("Зашифрований текст:")
    print(ciphertext)
    print("\nРозшифрований текст:")
    print(decrypted_text)
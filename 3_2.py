import string


# Зчитування тексту з файлу
def read_plain_text(filename):
    with open(filename, "r") as file:
        return file.read()

# Шифрування методом Віженера
def vigenere_encrypt(plaintext, key):
    encrypted = ""
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord("A")
            if char.isupper():
                encrypted += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                encrypted += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        else:
            encrypted += char # Неалфавітні символи залишаються
    return encrypted

# Створення таблиці для Playfair
def create_playfair_table(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    table = []
    for char in key.upper():
        if char not in table and char != "J":
            table.append(char)
    for char in alphabet:
        if char not in table:
            table.append(char)
    return table

# Шифрування методом Playfair
def playfair_encrypt(text, table):
    def get_position(c):
        idx = table.index(c)
        return divmod(idx, 5)

# Попереднє очищення тексту
    cleaned = (
        text.upper()
        .replace("J", "I")
        .replace(" ", "")
        .replace(".", "")
        .replace("'", "")
        .replace(",", "")
        .replace("-", "")
    )
    if len(cleaned) % 2 != 0:
        cleaned += "X" # Додаємо X якщо непарна довжина

    encrypted = ""
    for i in range(0, len(cleaned), 2):
        a, b = cleaned[i], cleaned[i + 1]
        row_a, col_a = get_position(a)
        row_b, col_b = get_position(b)

        if row_a == row_b:
            encrypted += table[row_a * 5 + (col_a + 1) % 5]
            encrypted += table[row_b * 5 + (col_b + 1) % 5]
        elif col_a == col_b:
            encrypted += table[((row_a + 1) % 5) * 5 + col_a]
            encrypted += table[((row_b + 1) % 5) * 5 + col_b]
        else:
            encrypted += table[row_a * 5 + col_b]
            encrypted += table[row_b * 5 + col_a]

    return encrypted


# Основний блок виконання
if __name__ == "__main__":
    plaintext_filename = "plaintext.txt"
    vigenere_key = "KEY"
    playfair_key = "CRYPTO"

    plaintext = read_plain_text(plaintext_filename)

# Крок 1: Шифрування Віженером
    vigenere_encrypted = vigenere_encrypt(plaintext, vigenere_key)
    print(f"Зашифровано методом Віженера:\n{vigenere_encrypted}\n")

# Крок 2: Додаткове шифрування Playfair
    playfair_table = create_playfair_table(playfair_key)
    playfair_encrypted = playfair_encrypt(vigenere_encrypted, playfair_table)
    playfair_encrypted += "."  # Додаємо крапку назад
    print(f"Додатково зашифровано Playfair:\n{playfair_encrypted}")
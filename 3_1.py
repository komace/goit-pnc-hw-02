import string

# Генерує шифрувальну таблицю (матрицю 5x5) для Playfair шифру
def generate_cipher_table(keyword):
    alphabet = string.ascii_uppercase.replace("J", "")
    key_letters = "".join(sorted(set(keyword), key=keyword.index))
    remaining_letters = "".join([c for c in alphabet if c not in key_letters])
    return key_letters + remaining_letters

# Розбиває текст на пари символів для Playfair шифру
def split_text(text):
    text = text.replace("J", "I").upper() # Замінюємо J -> I та до верхнього регістру
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if a not in string.ascii_uppercase:
            pairs.append(a)
            i += 1
            continue
        if i + 1 < len(text):
            b = text[i + 1]
            if b not in string.ascii_uppercase:
                pairs.append(a + "X")
                pairs.append(b)
                i += 2
            elif a == b:
                pairs.append(a + "X")
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + "X")
            i += 1

    if len(pairs[-1]) == 1 and pairs[-1] not in string.ascii_uppercase:
        pairs[-1] = pairs[-1] + "X"

    return pairs

# Шифрування Playfair
def playfair_encrypt(text, keyword):
    cipher_table = generate_cipher_table(keyword)
    pairs = split_text(text)
    encrypted = ""

    for pair in pairs:
        if len(pair) == 1:
            encrypted += pair
            continue

        a, b = pair
        if a not in cipher_table or b not in cipher_table:
            encrypted += a + b
            continue

        row_a, col_a = divmod(cipher_table.index(a), 5)
        row_b, col_b = divmod(cipher_table.index(b), 5)

        if row_a == row_b:
            encrypted += cipher_table[row_a * 5 + (col_a + 1) % 5]
            encrypted += cipher_table[row_b * 5 + (col_b + 1) % 5]
        elif col_a == col_b:
            encrypted += cipher_table[((row_a + 1) % 5) * 5 + col_a]
            encrypted += cipher_table[((row_b + 1) % 5) * 5 + col_b]
        else:
            encrypted += cipher_table[row_a * 5 + col_b]
            encrypted += cipher_table[row_b * 5 + col_a]

    return encrypted

# Дешифрування Playfair
def playfair_decrypt(encrypted_text, keyword):
    cipher_table = generate_cipher_table(keyword)
    pairs = split_text(encrypted_text)
    decrypted = ""

    for pair in pairs:
        if len(pair) == 1:
            decrypted += pair
            continue

        a, b = pair
        if a not in cipher_table or b not in cipher_table:
            decrypted += a + b
            continue

        row_a, col_a = divmod(cipher_table.index(a), 5)
        row_b, col_b = divmod(cipher_table.index(b), 5)

        if row_a == row_b:
            decrypted += cipher_table[row_a * 5 + (col_a - 1) % 5]
            decrypted += cipher_table[row_b * 5 + (col_b - 1) % 5]
        elif col_a == col_b:
            decrypted += cipher_table[((row_a - 1) % 5) * 5 + col_a]
            decrypted += cipher_table[((row_b - 1) % 5) * 5 + col_b]
        else:
            decrypted += cipher_table[row_a * 5 + col_b]
            decrypted += cipher_table[row_b * 5 + col_a]

    return decrypted.replace("X", "")

# Зчитування тексту з файлу
def read_text_from_file(filename):
    with open(filename, "r") as file:
        return file.read()


# Основний блок
if __name__ == "__main__":
    plaintext_filename = "plaintext.txt"
    keyword = "MATRIX"
    
    plaintext = read_text_from_file(plaintext_filename)
    ciphertext = playfair_encrypt(plaintext, keyword)
    decrypted = playfair_decrypt(ciphertext, keyword)

    print(f"Зашифрований текст:\n{ciphertext}")
    print(f"Розшифрований текст:\n{decrypted}")
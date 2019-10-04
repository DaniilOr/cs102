def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    new_key = keyword * (len(plaintext) // len(keyword))
    new_key = new_key + keyword * (len(plaintext) % len(keyword))
    for i in range(len(plaintext)):
        char = plaintext[i]
        code = ord(new_key[i])
        if char.isalpha() and chr(code).islower():
            code = ord(new_key[i]) - ord('a')
            code = code + ord(char)
            code -= ord('a') * int(char.islower())
            code -= ord('A')*int(char.isupper())
            code %= 26
            code = code + ord('a') * int(char.islower())
            code += ord('A') * int(char.isupper())
        if char.isalpha() and chr(code).isupper():
            code = ord(new_key[i]) - ord('A')
            code = code + ord(char) - ord('a') * int(char.islower())
            code -= ord('A') * int(char.isupper())
            code %= 26
            code = code + ord('a') * int(char.islower())
            code += ord('A') * int(char.isupper())
        ciphertext += chr(code)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    new_key = keyword * (len(ciphertext) // len(keyword))
    new_key = new_key + keyword * (len(ciphertext) % len(keyword))
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        code = ord(new_key[i])
        if char.isalpha() and chr(code).islower():
            code = ord(new_key[i]) - ord('a')
            code = ord(char) - code - ord('a') * int(char.islower())
            code -= ord('A') * int(char.isupper())
            code %= 26
            code = code + ord('a') * int(char.islower())
            code += ord('A') * int(char.isupper())
        if char.isalpha() and chr(code).isupper():
            code = ord(new_key[i]) - ord('A')
            code = ord(char) - code - ord('a') * int(char.islower())
            code -= ord('A') * int(char.isupper())
            code %= 26
            code = code + ord('a') * int(char.islower())
            code += ord('A') * int(char.isupper())

        plaintext += chr(code)
    return plaintext


if __name__ == '__main__':
    print(encrypt_vigenere('python', 'gone'))
    print(decrypt_vigenere(encrypt_vigenere('python', 'gone'), "gone"))

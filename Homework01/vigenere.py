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
        shift = ord('A') if char.isupper() else ord('a')
        if char.isalpha():
            code = ord(new_key[i]) - shift
            code = code + ord(char)
            code -= shift
            code %= 26
            code = code + shift
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
        shift = ord('A') if char.isupper() else ord('a')
        if char.isalpha():
            code = ord(new_key[i]) - shift
            code = ord(char) - code - shift
            code %= 26
            code = code + shift
        plaintext += chr(code)
    return plaintext


if __name__ == '__main__':
    print(encrypt_vigenere('python', 'gone'))
    print(decrypt_vigenere(encrypt_vigenere('python', 'gone'), "gone"))

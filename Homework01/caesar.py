def encrypt_caesar(plaintext: str, shift: int) -> str:
    """
    >>> encrypt_caesar("PYTHON",3)
    'SBWKRQ'
    >>> encrypt_caesar("python",3)
    'sbwkrq'
    >>> encrypt_caesar("Python3.6",3)
    'Sbwkrq3.6'
    >>> encrypt_caesar("",3)
    ''
    """
    ciphertext = ''
    for char in plaintext:
        char_int = ord(char)
        code = ord('A') if char.isupper() else ord('a')
        if char.isalpha():
            char_int -= code
            char_int += shift
            char_int %= 26
            char_int += code
        ciphertext += chr(char_int)

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    """
    >>> decrypt_caesar("SBWKRQ",3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq",3)
    'python'
    >>> decrypt_caesar("Sbwkrq3.6",3)
    'Python3.6'
    >>> decrypt_caesar("",3)
    ''
    """

    plaintext = ''
    for char in ciphertext:
        char_int = ord(char)
        code = ord('A') if char.isupper() else ord('a')
        if char.isalpha() and char.isupper():
            char_int -= code
            char_int -= shift
            char_int %= 26
            char_int += code
        if char.isalpha() and char.islower():
            char_int -= code
            char_int -= shift
            char_int %= 26
            char_int += code

        plaintext += chr(char_int)

    return plaintext


if __name__ == '__main__':
    print(encrypt_caesar('python3.2', 1))

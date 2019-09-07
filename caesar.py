def encrypt_caesar(plaintext: str) -> str:
    ciphertext = ''
    for char in plaintext:
        char_int = ord(char)
        if char.isalpha() and char.isupper():
            char_int-=ord('A')
            char_int+=3
            char_int%=26
            char_int += ord('A')
        if char.isalpha() and char.islower():
            char_int-=ord('a')
            char_int+=3
            char_int%=26
            char_int += ord('a')

        ciphertext+=chr(char_int)

    return ciphertext
def decrypt_caesar(ciphertext: str) -> str:
    plaintext = ''
    for char in ciphertext:
        char_int = ord(char)
        if char.isalpha() and char.isupper():
            char_int-=ord('A')
            char_int-=3
            char_int%=26
            char_int += ord('A')
        if char.isalpha() and char.islower():
            char_int-=ord('a')
            char_int-=3
            char_int%=26
            char_int += ord('a')

        plaintext+=chr(char_int)

    return plaintext


if __name__=='__main__':
    print(decrypt_caesar(''))

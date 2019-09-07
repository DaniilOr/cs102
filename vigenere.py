def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext=''
    new_key = keyword * ((len(plaintext)//len(keyword)) + int(len(plaintext)//len(keyword)==0))
    for i in range(len(plaintext)):
        char = plaintext[i]
        code = ord(new_key[i])
        if char.isalpha() and chr(code).islower():
            code = ord(new_key[i])-ord('a')
            code = code + ord(char) - ord('a')*int(char.islower()) - ord('A')*int(char.isupper())
            code%=26
            code=code+ord('a')*int(char.islower()) + ord('A')*int(char.isupper())
        if char.isalpha() and chr(code).isupper():
            code = ord(new_key[i])-ord('A')
            code =code + ord(char) - ord('a')*int(char.islower()) - ord('A')*int(char.isupper())
            code%=26
            code= code+ ord('a')*int(char.islower()) + ord('A')*int(char.isupper())
        ciphertext+=chr(code)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext=''
    new_key = keyword * ((len(ciphertext)//len(keyword)) + int(len(ciphertext)//len(keyword)==0))
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        code = ord(new_key[i])
        if char.isalpha() and chr(code).islower():
            code = ord(new_key[i])-ord('a')
            code = ord(char)-code  - ord('a')*int(char.islower()) - ord('A')*int(char.isupper())
            code%=26
            code=code+ord('a')*int(char.islower()) + ord('A')*int(char.isupper())
        if char.isalpha() and chr(code).isupper():
            code = ord(new_key[i])-ord('A')
            code =ord(char)-code  - ord('a')*int(char.islower()) - ord('A')*int(char.isupper())
            code%=26
            code= code+ ord('a')*int(char.islower()) + ord('A')*int(char.isupper())

        plaintext+=chr(code)
    return plaintext
if __name__=='__main__':
    print(decrypt_vigenere("LXFOPVEFRNHR", "LEMONLEMONLE"))

from math import sqrt
import random
def is_prime(n: int) -> bool:

    if n == 1:
        return False
    for i in range(2,int(sqrt(n))+1):
        if not n%i:
            return False
    return True
def gcd(a: int, b: int) -> int:
    while(a and b):
        if a>b:
            a%=b
        else:
            b%=a
    return a|b
def extended_gcd(a: int, b:int):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y



def multiplicative_inverse(e: int, phi: int) -> int:
    g, x, y = extended_gcd(e, phi)
    return x % phi

def generate_keypair(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p*q

    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
if __name__=="__main__":
    p = int(input("Enter a prime number: "))
    q = int(input("Enter ANOTHER prime number: "))
    public, private = generate_keypair(p, q)
    print ("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print (encrypted_msg)
    print (decrypt(public, encrypted_msg))

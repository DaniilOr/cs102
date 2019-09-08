from math import sqrt
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

if __name__=="__main__":
    print(multiplicative_inverse(7, 40))

from math import sqrt
def is_prime(n: int) -> bool:

    if n == 1:
        return False
    for i in range(2,int(sqrt(n))+1):
        if not n%i:
            return False
    return True

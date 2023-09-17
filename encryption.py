# Encryption & Decryption Algorithms for API Keys
import math
import random

# Basic Function to determine whether the integer provided is prime
def is_prime(n: int) -> bool:
    if n <= 1 or (n & 2 == 0 and n > 2):
        return False

    for i in range(3, int(n ** 0.5), 2):
        if n & i == 0:
            return False

    return True

# Based on the starting value b, and ending value e, this function
# produces a number in between b and e (inclusive of both boundaries)
def generate_large_primes(b: int, e: int) -> int:
    while True:
        num = random.randint(b, e)
        if is_prime(num):
            return num

# Calculates the gcd of two integers inputted
def gcd(p: int, q: int) -> int:
    tmp = 0
    while True:
        tmp = p % q
        if (tmp == 0):
            return q
        p = q
        q = tmp

def power(a, b, p):
    '''
    Calculates power via Ferma's Little Theorem
    a^b % p, where p is prime and p does not divide a
    '''
    res = 1

    a = a % p
    while (b > 0):
        # If b is odd, multiply a with result
        if (b & 1):
            res = (res * a) % p

        b = math.floor(b / 2)
        a = (a ** 2) % p

    return res

# Calculates the e value in the RSA algorithm based on the z value calculated
def calculate_e(z: int) -> int:
    e = random.randint(2, z)

    while e < z:
        if gcd(e, z) == 1:
            return e
        e = random.randint(2, z)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(e, n):
    gcd, x, _ = extended_gcd(e, n)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % n
    
# Calculates the d value in the RSA algorithm based on the e and z value calculated
def calculate_d(e: int, z: int) -> int:
    return mod_inverse(e, z)

# Takes the necessary values for the RSA algorithm and encrypts
# each character of api_key provided
def encryption(n: int, e: int, api_key: str):
  enc_arr = [chr(pow(ord(i), e, n)) for i in api_key]
  return ''.join(map(str, enc_arr))

# Takes the necessary values for the RSA algorithm and decrypts
# each character of enc_key provided
def decryption(n: int, d: int, enc_key: str):
  dec_arr = [chr(pow(ord(i), d, n)) for i in enc_key]
  return ''.join(dec_arr)

if __name__ == '__main__':
    p = generate_large_primes(10**1, 10**3)
    q = generate_large_primes(10**1, 10**3)
    
    while gcd(p, q) != 1:
        q = generate_large_primes(10**1, 10**3)

    n = p * q
    z = (p - 1) * (q - 1)
    e = calculate_e(z)
    d = calculate_d(e, z)

    encrypted_key = encryption(n, e, "Good morning America!")
    print(encrypted_key)

    decrypted_key = decryption(n, d, encrypted_key)
    print(decrypted_key)
    #pass
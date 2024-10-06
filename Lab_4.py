import random

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функция для вычисления мультипликативного обратного
def mod_inverse(e, phi):
    gcd, x, _ = gcd_extended(e, phi)
    if gcd != 1:
        raise ValueError("e and phi are not coprime")
    return x % phi

# Функция для генерации ключей RSA
def generate_rsa_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while gcd_extended(e, phi)[0] != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

# Бинарный алгоритм возведения в степень для шифрования/расшифрования
def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def encrypt(message, public_key):
    e, n = public_key
    return [modular_exponentiation(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(modular_exponentiation(char, d, n)) for char in ciphertext])

p, q = 101, 233
keys = [generate_rsa_keys(p, q) for _ in range(3)]

message = "Hello RSA"

results = []
for i, (public_key, private_key) in enumerate(keys):
    encrypted_message = encrypt(message, public_key)
    decrypted_message = decrypt(encrypted_message, private_key)
    results.append((public_key, private_key, encrypted_message, decrypted_message))

print(results)

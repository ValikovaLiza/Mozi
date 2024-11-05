import random

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, _ = gcd_extended(e, phi)
    if gcd != 1:
        raise ValueError("e and phi are not coprime")
    return x % phi

def generate_rsa_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while gcd_extended(e, phi)[0] != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

def compute_private_key(e, n, p, q):
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    return (d, n)

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


print("Выберите вариант:")
print("1. Автоматическая генерация ключей")
print("2. Ввод открытых ключей вручную")
    
choice = input("Введите номер варианта (1 или 2): ")
    
keys = []
if choice == '1':
    p, q = 197, 349
    keys = [generate_rsa_keys(p, q) for _ in range(3)]
elif choice == '2':
    for i in range(3):
        e = int(input(f"Введите e для пары ключей {i+1}: "))
        n = int(input(f"Введите n для пары ключей {i+1}: "))
        p = int(input(f"Введите p (для вычисления d) для пары ключей {i+1}: "))
        q = int(input(f"Введите q (для вычисления d) для пары ключей {i+1}: "))
        private_key = compute_private_key(e, n, p, q)
        keys.append(((e, n), private_key))
else:
    print("Неверный выбор.")
    
message = input("Введите сообщение для шифрования: ")
results = []
for i, (public_key, private_key) in enumerate(keys):
    encrypted_message = encrypt(message, public_key)
    decrypted_message = decrypt(encrypted_message, private_key)
    results.append((public_key, private_key, encrypted_message, decrypted_message))

for i, (public_key, private_key, encrypted_message, decrypted_message) in enumerate(results):
    print(f"Пара ключей {i+1}:")
    print(f"Публичный ключ: {public_key}")
    print(f"Приватный ключ: {private_key}")
    print(f"Зашифрованное сообщение: {encrypted_message}")
    print(f"Расшифрованное сообщение: {decrypted_message}")
    print()

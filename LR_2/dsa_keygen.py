# dsa_keygen.py
import random
import sys
from dsa_math import generate_large_prime, find_primitive_root, mod_inverse
from dsa_math import generate_p_and_q
import md5  # ваш модуль хеширования!


def get_seed_from_password(password):
    # Получить хэш через собственную функцию
    hashed = md5.md5(password.encode())
    # Преобразовать хэш в целое число
    return int.from_bytes(hashed, byteorder='big')


def generate_keys(bits=1024, password=None):
    if password:
        seed = get_seed_from_password(password)
        random.seed(seed)
    else:
        random.seed()

    # # Генерация p
    # print("[*] Генерация p...")
    # p = generate_large_prime(bits)
    #
    # # Генерация q
    # print("[*] Генерация q...")
    # while True:
    #     q = generate_large_prime(160)  # q ~ 160 бит
    #     if (p - 1) % q == 0:
    #         break

    print("[*] Генерация p и q")
    p, q = generate_p_and_q()

    # Генерация g
    print("[*] Поиск g...")
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1

    # Генерация закрытого ключа x
    print("[*] Генерация x (закрытого ключа)...")
    x = random.randint(1, q - 1)

    # Генерация открытого ключа y
    print("[*] Генерация y (открытого ключа)...")
    y = pow(g, x, p)

    return {
        'p': p,
        'q': q,
        'g': g,
        'x': x,
        'y': y
    }


def save_keys(keys, private_filename="private_key.txt", public_filename="public_key.txt"):
    with open(private_filename, 'w') as f:
        f.write(f"{keys['p']}\n{keys['q']}\n{keys['g']}\n{keys['x']}\n")

    with open(public_filename, 'w') as f:
        f.write(f"{keys['p']}\n{keys['q']}\n{keys['g']}\n{keys['y']}\n")


if __name__ == "__main__":
    print("=== DSA Генерация ключей ===")
    mode = input("Сгенерировать ключи по паролю? (yes/no): ").strip().lower()
    if mode == 'yes':
        password = input("Введите пароль: ").strip()
        keys = generate_keys(1024, password)
    else:
        keys = generate_keys(1024)

    save_keys(keys)
    print("[+] Ключи успешно сгенерированы!")

import random
from dsa_math import generate_p_and_q
import md5


def get_seed_from_password(password):
    hashed = md5.md5(password.encode())
    return int.from_bytes(hashed, byteorder='big')


def generate_keys(bits=1024, password=None):
    if password:
        seed = get_seed_from_password(password)
        random.seed(seed)
    else:
        random.seed()

    print("[*] Генерация p и q")
    p, q = generate_p_and_q()

    print("[*] Поиск g...")
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1

    print("[*] Генерация x (закрытого ключа)...")
    x = random.randint(1, q - 1)

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
    print("[+] Ключи успешно сгенерированы")

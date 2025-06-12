import random
from dsa_math import generate_p_and_q


def generate_keys(bits=1024):
    print("Генерация p и q")
    p, q = generate_p_and_q()

    print("Поиск g")
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1

    print("Генерация x (закрытого ключа)")
    x = random.randint(1, q - 1)

    print("Генерация y (открытого ключа)")
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
    print("DSA Генерация ключей")

    keys = generate_keys(1024)

    save_keys(keys)
    print("Ключи успешно сгенерированы")

import random
from dsa_math import mod_inverse
import md5

def load_private_key(filename="private_key.txt"):
    with open(filename, 'r') as f:
        p = int(f.readline())
        q = int(f.readline())
        g = int(f.readline())
        x = int(f.readline())
    return p, q, g, x

def hash_message(message_bytes):
    message_string = message_bytes.decode('utf-8')
    hash_hex = md5.md5(message_string)
    hash_bytes = bytes.fromhex(hash_hex)
    return int.from_bytes(hash_bytes, byteorder='big')

def sign_message(message_filename, signature_filename="signature.txt", private_key_filename="private_key.txt"):
    p, q, g, x = load_private_key(private_key_filename)

    with open(message_filename, 'rb') as f:
        message = f.read()

    h = hash_message(message)
    k = None
    while True:
        k = random.randint(1, q-1)
        try:
            r = pow(g, k, p) % q
            if r == 0:
                continue
            k_inv = mod_inverse(k, q)
            s = (k_inv * (h + x * r)) % q
            if s == 0:
                continue
            break
        except FileNotFoundError:
            print("FILE NOT FOUND!")
            return
        except Exception:
            continue
    file = open("opened_k.txt", "w")
    file.write(str(k))
    file.close()

    with open(signature_filename, 'w') as f:
        f.write(f"{r}\n{s}\n")

    print(f"Сообщение '{message_filename}' подписано")
    print(f"Подпись сохранена в '{signature_filename}'.")

if __name__ == "__main__":
    print("DSA Постановка подписи")
    message_filename = input("Введите имя файла сообщения: ").strip()
    print("Начинается процесс подписи")
    sign_message(message_filename)

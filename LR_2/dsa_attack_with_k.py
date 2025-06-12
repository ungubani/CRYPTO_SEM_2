# DOP Реализовать атаку на систему DSA в случае, если стал известен
# случайный параметр k.

# x = (r^(-1) [mod q] * (k*s-h)) [mod q]

from dsa_math import mod_inverse
from dsa_verify import load_public_key
from dsa_verify import load_signature
from dsa_sign import hash_message
from dsa_sign import load_private_key


def attack_with_open_k(message_filename, opened_k_filename="opened_k.txt", public_key_filename="public_key.txt", signature_filename="signature.txt"):
    p, q, g, y = load_public_key(public_key_filename)
    r, s = load_signature(signature_filename)

    try:
        with open(opened_k_filename) as f:
            k_open = int(f.readline())
            print("k_open =", k_open, end="\n\n")
    except FileNotFoundError:
        print(f"Файл {f} not found")
        return

    inverse_r = mod_inverse(r, q)

    with open(message_filename, 'rb') as f:
        message = f.read()
    h = hash_message(message)

    attack_x = inverse_r * (k_open * s - h) % q

    return attack_x


if __name__ == "__main__":

    attack_a = attack_with_open_k("text_dlya_podpisi.txt")
    _, _, _, true_a = load_private_key()

    print(f"attack_a = {attack_a}\n"
          f"true_original_a = {true_a}")

    print("\nАТАКА УДАЛАСЬ" if attack_a == true_a else "АТАКА ПРОВАЛИЛАСЬ")

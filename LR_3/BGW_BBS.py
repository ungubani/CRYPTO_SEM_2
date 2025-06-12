import random
from math import gcd
from LR_2.dsa_math import is_prime, mod_inverse, mod_pow


def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p) and p % 4 == 3:
            return p


def generate_keys(bits=512):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    n = p * q
    return (n, p, q)


def bbs_generator(x, n, num_bits):
    bits = []
    for _ in range(num_bits):
        x = mod_pow(x, 2, n)
        bits.append(x & 1)
    return bits, x


def encrypt(message_bits, n):
    t = len(message_bits)

    while True:
        x = random.randint(2, n - 1)
        if gcd(x, n) == 1:
            break

    x0 = mod_pow(x, 2, n)
    bbs_bits, xt = bbs_generator(x0, n, t)

    cipher_bits = [m ^ b for m, b in zip(message_bits, bbs_bits)]

    return cipher_bits, xt


def decrypt(cipher_bits, xt, p, q):
    n = p * q
    t = len(cipher_bits)

    a = pow((p + 1) // 4, t, p - 1)
    b = pow((q + 1) // 4, t, q - 1)
    u = mod_pow(xt % p, a, p)
    v = mod_pow(xt % q, b, q)
    x0 = (u * q * mod_inverse(q, p) + v * p * mod_inverse(p, q)) % n

    bbs_bits, _ = bbs_generator(x0, n, t)

    message_bits = [c ^ b for c, b in zip(cipher_bits, bbs_bits)]

    return message_bits


def str_to_bits(s):
    return [int(bit) for byte in s.encode() for bit in bin(byte)[2:].zfill(8)]


def bits_to_str(bits):
    bytes_list = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(map(str, byte)), 2)) for byte in bytes_list)


if __name__ == "__main__":
    message = "KukuTebePrivet"
    message_bits = str_to_bits(message)

    print("<Генерация ключей>")
    n, p, q = generate_keys(bits=512)  # 512 бит для безопасности

    print("<Шифрование>")
    cipher_bits, xt = encrypt(message_bits, n)

    print("Зашифрованный текст:", bits_to_str(cipher_bits))
    # print("Последнее состояние xt:", xt)

    print("\n<Дешифровка>")
    recovered_bits = decrypt(cipher_bits, xt, p, q)
    recovered_message = bits_to_str(recovered_bits)

    print("Оригинал:", message)
    print("Дешифровка:", recovered_message)

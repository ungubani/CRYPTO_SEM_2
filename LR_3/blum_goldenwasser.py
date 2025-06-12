import random
from LR_2.dsa_math import is_prime
from LR_2.dsa_math import extended_gcd
from LR_2.dsa_math import mod_inverse
from LR_2.dsa_math import mod_pow


def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p) and p % 4 == 3:
            return p


def CRT(a1, m1, a2, m2):
    m1_inv = mod_inverse(m1, m2)
    return (a1 * m2 * mod_inverse(m2, m1) + a2 * m1 * m1_inv) % (m1 * m2)


def generate_keys(bits=128):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    return (n, p, q)


def encrypt(message_bits, n):
    k = len(bin(n)) - 3
    r = random.randint(2, n - 1)
    r_list = []
    x_list = []
    c_list = []

    for m_bit in message_bits:
        r = mod_pow(r, 2, n)
        x = r % (1 << k)
        x_list.append(x & 1)
        c_list.append(m_bit ^ (x & 1))
        r_list.append(r)

    return c_list, r, r_list


def decrypt(cipher_bits, x_t, p, q):
    n = p * q
    t = len(cipher_bits)
    d_p = mod_pow(x_t, pow((p + 1) // 4, t, p - 1), p)
    d_q = mod_pow(x_t, pow((q + 1) // 4, t, q - 1), q)
    x_0 = CRT(d_p, p, d_q, q)

    k = len(bin(n)) - 3
    x = x_0
    m = []

    for c in cipher_bits:
        x = mod_pow(x, 2, n)
        z = x % (1 << k)
        m.append(c ^ (z & 1))
    return m


def str_to_bits(s):
    return [int(bit) for byte in s.encode() for bit in bin(byte)[2:].zfill(8)]

def bits_to_str(bits):
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(str(b) for b in byte), 2)) for byte in bytes_list)

if __name__ == "__main__":
    message = "KukuTebePrivet"
    message_bits = str_to_bits(message)
    print(f"m= {message_bits}")
    print("Генерация ключей...")
    n, p, q = generate_keys(bits=64)

    print("Шифрование...")
    c, x_t, _ = encrypt(message_bits, n)

    print(f"c= {c}")


    print("Расшифровка...")
    recovered_bits = decrypt(c, x_t, p, q)
    recovered_message = bits_to_str(recovered_bits)

    print("Оригинал:", message)
    print("Дешифровка:", recovered_message)

# 12 Dop

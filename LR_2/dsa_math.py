import random

def mod_pow(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n == 2:
        return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        if mod_pow(a, n - 1, n) != 1:
            return False
    return True

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, y, x = extended_gcd(b, a % b)
        return (g, x, y - (a // b) * x)

def mod_inverse(a, modulus):
    g, x, _ = extended_gcd(a, modulus)
    if g != 1:
        raise Exception('Inverse does not exist')
    else:
        return x % modulus

def generate_large_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1  # сделать старший и младший бит единицами
        if is_prime(candidate):
            return candidate

def find_primitive_root(p):
    if p == 2:
        return 1
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        ok = True
        for factor in factors:
            if mod_pow(g, phi // factor, p) == 1:
                ok = False
                break
        if ok:
            return g
    raise Exception('Primitive root not found')

def prime_factors(n):
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.add(f)
            n //= f
        f += 2
    if n > 1:
        factors.add(n)
    return factors

def generate_p_and_q(bits=1024, q_bits=160):
    print("[*] Генерация q...")
    while True:
        q = generate_large_prime(q_bits)
        if is_prime(q):
            break

    print("[*] Генерация p...")
    k = random.getrandbits(bits - q_bits)
    k |= (1 << (bits - q_bits - 1))  # чтобы k было достаточно большим
    p = q * k + 1

    while not is_prime(p):
        k += 1
        print(f"Поиск p, сейчас k={k}")
        p = q * k + 1

    return p, q


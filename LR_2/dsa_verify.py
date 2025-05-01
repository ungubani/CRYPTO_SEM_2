from dsa_math import mod_inverse, mod_pow
import md5

def load_public_key(filename="public_key.txt"):
    with open(filename, 'r') as f:
        p = int(f.readline())
        q = int(f.readline())
        g = int(f.readline())
        y = int(f.readline())
    return p, q, g, y

def load_signature(filename="signature.txt"):
    with open(filename, 'r') as f:
        r = int(f.readline())
        s = int(f.readline())
    return r, s

def hash_message(message_bytes):
    message_string = message_bytes.decode('utf-8')
    hash_hex = md5.md5(message_string)
    hash_bytes = bytes.fromhex(hash_hex)
    return int.from_bytes(hash_bytes, byteorder='big')

def verify_signature(message_filename, signature_filename="signature.txt", public_key_filename="public_key.txt"):
    p, q, g, y = load_public_key(public_key_filename)
    r, s = load_signature(signature_filename)

    if not (0 < r < q and 0 < s < q):
        print("[-] Подпись недействительна: r или s вне допустимого диапазона.")
        return False

    with open(message_filename, 'rb') as f:
        message = f.read()

    h = hash_message(message)

    try:
        w = mod_inverse(s, q)
    except Exception:
        print("[-] Не удалось найти обратный элемент для s.")
        return False

    u1 = (h * w) % q
    u2 = (r * w) % q

    v = ((mod_pow(g, u1, p) * mod_pow(y, u2, p)) % p) % q

    if v == r:
        print("[+] Подпись действительна.")
        return True
    else:
        print("[-] Подпись недействительна.")
        return False

if __name__ == "__main__":
    print("DSA Проверка подписи")
    message_filename = input("Введите имя файла сообщения: ").strip()
    verify_signature(message_filename)

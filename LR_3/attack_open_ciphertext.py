from LR_3.blum_goldenwasser import *


if __name__ == "__main__":
    true_message = "KukuTebePrivet"
    message_bits = str_to_bits(true_message)
    print(f"m= {message_bits}")
    print("\n<Генерация ключей>")
    n, p, q = generate_keys(bits=64)

    print("<Шифрование>")
    c, x_t, _ = encrypt(message_bits, n)

    print(f"c= {c}")


    print("\n<<<АТАКА на Blum-Goldwasser>>>")
    alpha_message_bits = [random.randint(0, 1) for _ in range(len(c))]
    print("alpha=", alpha_message_bits)

    alpha_decrypt_message_bits = decrypt(alpha_message_bits, x_t, p, q)

    attack_message_bits = []
    for i in range(len(c)):
        bit = (alpha_decrypt_message_bits[i] ^
               c[i] ^
               alpha_message_bits[i])
        attack_message_bits.append(bit)

    print("attack=", attack_message_bits)

    attack_message = bits_to_str(attack_message_bits)
    print("Сообщение, полученное после атаки:", attack_message)
    print("Исходное сообщение:", true_message)

    # print("\nРасшифровка...")
    # recovered_bits = decrypt(c, x_t, p, q)
    # recovered_message = bits_to_str(recovered_bits)
    #
    # print("Оригинал:", true_message)
    # print("Дешифровка:", recovered_message)
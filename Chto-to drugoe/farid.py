from collections import Counter

def build_alphabet(text):
    # Частоты символов + алфавит по убыванию частоты
    freq = Counter(text)
    alphabet = sorted(freq.keys(), key=lambda ch: (-freq[ch], text.index(ch)))
    print("Алфавит (по убыванию частоты):")
    for i, ch in enumerate(alphabet, 1):
        if ch == ' ':
            symb = "' '"  # для красоты
        elif ch == '\n':
            symb = "'\\n'"
        else:
            symb = ch
        print(f"{i:2d}: {symb}  (частота: {freq[ch]})")
    return alphabet

def mtf_transform(text, alphabet):
    alph = alphabet[:]
    codes = []
    print("\nПреобразование «стопкой книг» (MTF):")
    print(f"{'N':>2} | {'Символ':^6} | {'Позиция+1':^10} | {'Новый алфавит'}")
    for idx, ch in enumerate(text):
        pos = alph.index(ch)
        codes.append(pos + 1)
        alph.insert(0, alph.pop(pos))
        # Показываем первые 10 алфавитов, дальше не захламляем
        preview_alph = ''.join(alph[:10]) + ('...' if len(alph) > 10 else '')
        display = "' '" if ch == ' ' else ch
        print(f"{idx+1:2d} |   {display:^4}  |     {pos+1:^6}   | {preview_alph}")
    print("\nРезультат преобразования: ", codes)
    return codes

def golomb_encode(seq, m=2):
    import math
    print("\nКод Голомба (m=2):")
    print(f"{'N':>2} | {'Число':>6} | {'q':>2} | {'r':>2} | {'Унарная':>9} | {'Двоич.':>7} | {'Код':>12} | {'Длина':>6}")
    total_bits = 0
    for idx, n in enumerate(seq):
        q = n // m
        r = n % m
        unary = '1' * q + '0'
        bin_part = f"{r:01b}"  # m=2 => 1 бит
        code = unary + bin_part
        code_len = len(unary) + 1  # +1 за остаток
        total_bits += code_len
        print(f"{idx+1:2d} | {n:6d} | {q:2d} | {r:2d} | {unary:9} | {bin_part:7} | {code:12} | {code_len:6d}")
    print(f"\nДлина кодированной кодом Голомба последовательности: {total_bits} бит.")
    return total_bits

def uniform_code_length(alphabet, text):
    import math
    M = len(alphabet)
    L = len(text)
    bits = (math.ceil(math.log2(M))) * L
    print(f"\nДлина кодированной равномерным кодом последовательности: {bits} бит (⎡log2({M})⎤ * {L})")
    return bits

def gamma_code(n):
    # Монотонный (гамма-)код для l (для LZ-77)
    # n >= 1
    b = bin(n)[2:]
    return '0' * (len(b) - 1) + b

def lz77_compress(text):
    tokens = []
    i = 0
    N = len(text)
    while i < N:
        match_len = 0
        match_dist = 0
        for j in range(max(0, i - N), i):
            l = 0
            while (i + l < N) and (text[j + l] == text[i + l]):
                l += 1
                if j + l >= i:
                    break
            if l > match_len:
                match_len = l
                match_dist = i - j
        if match_len >= 2:
            tokens.append(('match', match_dist, match_len))
            i += match_len
        else:
            tokens.append(('lit', text[i]))
            i += 1
    return tokens

def lz77_table(tokens, text):
    # Вывод таблицы и подсчёт бит
    print("\nКод LZ-77:")
    print(f"{'N':>3} | {'Флаг':>4} | {'Слово':>8} | {'d':>3} | {'l':>2} | {'W (код l)':>8} | {'Кодовое слово':>20} | {'Затраты':>7}")
    total_bits = 0
    offset = 0
    for n, token in enumerate(tokens, 1):
        if token[0] == 'lit':
            flag = 0
            symb = token[1]
            word_disp = "' '" if symb == ' ' else symb
            codeword = f"{flag}{format(ord(symb),'08b')}"
            bits = 1 + 8
            total_bits += bits
            print(f"{n:3d} | {flag:4d} | {word_disp:^8} | {'-':>3} | {'-':>2} | {'-':>8} | {codeword:>20} | {bits:7d}")
            offset += 1
        else:
            flag = 1
            d, l = token[1], token[2]
            match_str = text[offset:offset + l]
            w_code = gamma_code(l)
            d_code = format(d, '06b')
            codeword = f"{flag}{w_code}{d_code}"
            bits = 1 + len(w_code) + 6
            total_bits += bits
            print(f"{n:3d} | {flag:4d} | {match_str:^8} | {d:3d} | {l:2d} | {w_code:>8} | {codeword:>20} | {bits:7d}")
            offset += l
    print(f"\nДлина кодированной кодом LZ-77 последовательности: {total_bits} бит.")
    return total_bits

def main():
    text = "испугались медвежонка еж с ежихой и с еж"
    print("Исходный текст:\n" + text)
    alphabet = build_alphabet(text)
    mtf_codes = mtf_transform(text, alphabet)
    total_golomb_bits = golomb_encode(mtf_codes, m=2)
    uniform_bits = uniform_code_length(alphabet, text)
    tokens = lz77_compress(text)
    lz77_bits = lz77_table(tokens, text)

if __name__ == '__main__':
    main()

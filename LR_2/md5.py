import time


def md5(string: str) -> str:
    buffer = bytearray(string, 'utf-8')

    shifts = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21]
    sines = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
                0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,

                0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
                0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,

                0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
                0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,

                0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
                0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

    blocks = (len(buffer) + 8) // 64 + 1

    aa = 0x67452301
    bb = 0xefcdab89
    cc = 0x98badcfe
    dd = 0x10325476

    for i in range(0, blocks):
        block = buffer
        offset = i * 64

        if offset + 64 > len(buffer):
            block = bytearray(0 for _ in range(64))

            for j in range(offset, len(buffer)):
                block[j - offset] = buffer[j]
            if offset <= len(buffer):
                block[len(buffer) - offset] = 0x80
            if i == blocks - 1:
                block[56] = (len(buffer) << 3) & 0xFF
                block[57] = (len(buffer) >> 5) & 0xFF
                block[58] = (len(buffer) << 13) & 0xFF
                block[59] = (len(buffer) >> 21) & 0xFF

            offset = 0

        a = aa
        b = bb
        c = cc
        d = dd

        f = 0
        g = 0

        for j in range(0, 64):
            if j < 16:
                f = b & c | ~b & d
                g = j
            elif j < 32:
                f = b & d | c & ~d
                g = 5 * j + 1
            elif j < 48:
                f = b ^ c ^ d
                g = 3 * j + 5
            else:
                f = c ^ (b | ~d)
                g = 7 * j

            g = (g & 0x0F) * 4 + offset

            hold = d
            d = c
            c = b

            b = (a + f + sines[j] + (block[g] + (block[g + 1] << 8) + (block[g + 2] << 16) + (block[g + 3] << 24))) & 0xFFFFFFFF

            shift_amount = shifts[(j & 3) | ((j >> 2) & ~3)]
            b = ((b << shift_amount) | (b >> (32 - shift_amount))) & 0xFFFFFFFF

            b = (b + c) & 0xFFFFFFFF

            a = hold

        aa += a
        bb += b
        cc += c
        dd += d

    return bytearray([aa & 0xFF, (aa >> 8) & 0xFF, (aa >> 16) & 0xFF, (aa >> 24) & 0xFF,
            bb & 0xFF, (bb >> 8) & 0xFF, (bb >> 16) & 0xFF, (bb >> 24) & 0xFF,
            cc & 0xFF, (cc >> 8) & 0xFF, (cc >> 16) & 0xFF, (cc >> 24) & 0xFF,
            dd & 0xFF, (dd >> 8) & 0xFF, (dd >> 16) & 0xFF, (dd >> 24) & 0xFF]).hex()


def num_to_base(number: int, base: int, length: int) -> list:
    represent = []
    while number != 0:
        represent.append(number % base)
        number //= base

    while len(represent) < length:
        represent.append(0)

    return represent


def forming_password(number, length, alphabet):
    indexes = num_to_base(number, len(alphabet), length)

    password = "".join([alphabet[i] for i in indexes])

    return password


def brute_force(source_hash: str, length_pass: int, alphabet: list) -> float:
    start = time.time()

    for i in range(length_pass ** len(alphabet)):
        prob_password = forming_password(i, length_pass, alphabet)

        if source_hash == md5(prob_password):
            print(f"Finded Pass: {prob_password}")
            end = time.time()

            break

    return end - start

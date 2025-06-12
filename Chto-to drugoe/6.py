from prettytable import PrettyTable

string = "выдрав с выдры в тундре гетры, вытру выд"
# string = "а мне не до недомогания, на меду медовик"
# string = "испугались медвежонка еж с ежихой и с еж"
print(len(string))
string = string.replace(' ', '_')

#------------
# Стопка книг
#------------

x_string = ''

x_set = set()
for c in string:
    if c not in x_set:
        print(c, end=" ")
        x_set.add(c)
        x_string += c

alphabet = x_string
M = len(x_string)

x_string += string

books_array = [None] * M
for i in range(M, len(x_string)):
    char = x_string[i]
    unique_chars = set()
    for j in range(i - 1, -1, -1):
        left_char = x_string[j]
        unique_chars.add(left_char)
        if left_char == char:
            books_array.append(len(unique_chars))
            break

print("\nBOOKS:", books_array)



def unar(i):
    return "1" * (i-1) + "0"

def my_bin(i):
    return bin(i)[2::]

def my_bin_m(i, m=2):
    return bin(i)[2::].rjust(m, "0")

def my_bin_s(i):
    return bin(i)[3::]

def gol(i, m=2):
    T = 2**m
    first = unar((i // T) + 1)
    second = (my_bin_m(i % T))
    weight = len(first) + len(second)
    return f"[{first}, {second}]", weight

#---------------------
# GOLOMB
#----------------------

# table = PrettyTable()
# table.field_names = ["Filename", "Source", "Predicted", "Status"]
#
# for result in results:
#     table.add_row([result["filename"], result["true"], result["predicted"], result["correct"]])

table_golomb = PrettyTable()
table_golomb.field_names = ['Число i', 'Кодовое слово', 'Затраты']

for i in range(M, len(x_string)):
    code_word, weight = gol(books_array[i])
    table_golomb.add_row([books_array[i], code_word, weight])

print(table_golomb)


import math

def mon(i):
    bin_i = bin(i)[2::]
    return f"[{unar(len(bin_i))}, {my_bin_s(i)}]"

def lz77(flag, word, d, w, l):
    if flag == 0:
        print("Слово", "Затраты")
        print(f"0bin({word})", 9)

    elif flag == 1:
        len_d = math.floor(math.log2(w)) + 1

        word = f"[1, {bin(d)[2::].zfill(len_d)}, {mon(l)}]"
        print("Слово", "Затраты")
        print(word, 1 + len_d + len(mon(l)))


    else:
        print("Not correct format")

print("\n---LZ-77---")
print("Для выхода нажмите Ctrl+C")

try:
    while True:
        print("Введите <flag> <word> <d> <w> <l>")
        flag, word, d, w, l = map(str, input().split())
        flag = int(flag)
        d = int(d)
        w = int(w)
        l = int(l)

        lz77(flag, word, d, w, l)

except KeyboardInterrupt:
    print("---Завершение программы---")

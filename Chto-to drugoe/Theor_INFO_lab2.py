"""
___ВАРИАНТ_81___
Дан текст:
«выдрав с выдры в тундре гетры, вытру выдрой ядра кедра. »

Найти:
<+> – двумерное распределение вероятностей X^2;
<+> – условное распределение X|X по выборке;
<+> – одномерное распределение X из выборки, считая её одномерной;
<+> – одномерную энтропию H(X);
<+> – двумерную энтропию H(X^2) и энтропию на сообщение H_{2}(X);
<+> – условную энтропию H(X|X).

Указания:
– считать, что буквы в алфавитах X и X2 расположены в порядке
встречаемости в тексте;
– ответы округлить до двух знаков после запятой;
– считать, что 0 · log 0 = 0.
"""

from decimal import Decimal, ROUND_HALF_UP
import math


def round_math(value: float, ndigits: int) -> float:
    """
    Округляет число по стандартным математическим правилам (round half up),
    когда 5 округляется вверх.

    :param value: Число для округления
    :param ndigits: Количество знаков после запятой
    :return: Округлённое число
    """
    factor = Decimal("1." + "0" * ndigits)  # Формируем множитель 10^(-ndigits)
    return float(Decimal(value).quantize(factor, rounding=ROUND_HALF_UP))



def dvumernoe_raspredelenie(text: str, auto_round=True):
    """Разбитие на непересекающиеся биграммы и подсчет вероятностей относительно их"""
    # Код ужасен, никто и не спорит. Так заумано
    bigramms = []
    for i in range(0, len(text), 2):
        # print(text[i:i+2])
        bigramms.append(text[i:i + 2])

    bidict = dict()

    raspredelenie = []
    for index, bi in enumerate(bigramms):
        if bi not in bidict:
            bidict[bi] = len(raspredelenie)
            raspredelenie.append([bi, 1, None])

        else:
            raspredelenie[bidict[bi]][1] += 1

    count_bigrams = len(text) / 2
    for bistat in raspredelenie:
        bistat[2] = bistat[1] / count_bigrams
        if auto_round:
            bistat[2] = round(bistat[2], 2)

    # print(raspredelenie)
    return raspredelenie


def odnomernoe_raspredelenie(text: str, auto_round=True):
    """разбитие на буковки длины 1 и подсчет веротяности относительно их"""
    # Код ужасен, никто и не спорит. Так заумано
    nebigramms = []
    for i in range(0, len(text), 1):
        # print(text[i:i+2])
        nebigramms.append(text[i:i + 1])

    nebidict = dict()

    raspredelenie = []
    for index, nebi in enumerate(nebigramms):
        if nebi not in nebidict:
            nebidict[nebi] = len(raspredelenie)
            raspredelenie.append([nebi, 1, None])

        else:
            raspredelenie[nebidict[nebi]][1] += 1

    count_nebigrams = len(text)
    for nebistat in raspredelenie:
        nebistat[2] = nebistat[1] / count_nebigrams
        if auto_round:
            nebistat[2] = round(nebistat[2], 2)

    # print(raspredelenie)
    return raspredelenie


def uslovnoe_raspredelenie(text: str, auto_round=True):
    """Разбитие на пересекающиеся биграммы и подсчет вероятностей относительно их"""
    # Код ужасен, никто и не спорит. Так заумано
    crossed_bigramms = []
    for i in range(0, len(text) - 1):
        # print(text[i:i+2])
        crossed_bigramms.append(text[i:i + 2][::-1])

    # print(crossed_bigramms)
    crossed_bidict = dict()
    raspredelenie = []
    for index, bi in enumerate(crossed_bigramms):
        if bi not in crossed_bidict:
            crossed_bidict[bi] = len(raspredelenie)
            raspredelenie.append([bi, None, None, 1, None, None])

        else:
            raspredelenie[crossed_bidict[bi]][3] += 1

    count_crossed_bigrams = len(text) - 1

    for bistat in raspredelenie:
        bistat[0] = bistat[0][0] + "|" + bistat[0][1]
        bistat[1] = text.count(bistat[0][0])  # N_{y}
        bistat[2] = text.count(bistat[0][2])  # N_{x}
        p_YX = bistat[3] / bistat[2]  # p(Y|X) = N_{'xy'} / N_{'x'}
        x_prob = text.count(bistat[0][2]) / len(text)

        if auto_round:
            p_YX = round(p_YX, 2)
            bistat[3] = p_YX
            bistat[4] = round(p_YX * round(x_prob, 2) * math.log2(p_YX), 2)
            bistat[5] = round(x_prob, 2)
        else:
            bistat[3] = p_YX
            bistat[4] = p_YX * x_prob * math.log2(p_YX)
            bistat[5] = x_prob


    # print(len(raspredelenie), sum(elem[1] for elem in raspredelenie), raspredelenie)
    return raspredelenie


def H_X_mode(stat, explain=False, mode="X"):
    entropy = 0
    if explain:
        print(f"H({mode})= ", end="")
    for x in stat:
        if explain:
            print(f"{x[2]}*log2({x[2]}) +", end=" ")

        entropy -= x[2] * math.log2(round(x[2], 2))

    if explain:
        print(f"\nH({mode})= {round(entropy, 2)}")
    return round(entropy, 2)


def H_YX(stat, explain=False):
    entropy = 0
    if explain:
        print(f"H(Y|X)= -(", end="")
    for yx in stat:
        if explain:
            print(f"{yx[4]} ", end=" ")

        entropy -= yx[4]

    if explain:
        print(f")\nH(Y|X)= {round(entropy, 2)}")
    return round(entropy, 2)


if __name__ == "__main__":
    print("!!!WARNING!!!"
          "Так как питон гениален, то используемое в данной программе округление round(x, 2) "
          "[до двух знаков после запятой] может выдавать неожиданный на первый взгляд результат:"
          "(n.dd5 -> n.dd вместо n.d[d+1])"
          "Если кто-то надумает пользоваться кодом, то это все на его страх и риск"
          "P.s. мне повезло и у меня округляет по правилам математики")

    # text = "выдрав с выдры в тундре гетры, вытру выдрой ядра кедра. "
    # text = "белый снег, белый мел, белый заяц тоже бел, а вот белка не бела - белой даже не была. "
    # text = "цыпленок цапли цепко цеплялся за цеп. "
    text = "банкиров ребрендили-ребрендили-ребрендили, да не выребрендировали."
    # text = "мы ели-ели ершей у ели, их еле-еле у ели доели. "  # Вариант 17
    if "_" not in text:
        text = text.replace(" ", "_")
        print("' ' was replaced by '_'")
    else:
        print("WARNING: ' ' was not replaced by '_'")


    print("\nODNOMERNOE")
    print(["X", "N", "p_{X}"])
    o_r = odnomernoe_raspredelenie(text)
    for o_stat in o_r:
        print(o_stat, end=" ")
        print("%.2f" % round(o_stat[2], 2))

    print(H_X_mode(o_r, explain=True, mode="X"))


    print("\nDVUMERNOE")
    print(["X^2", "N", "p_{X^2}"])
    d_r = dvumernoe_raspredelenie(text)
    for d_stat in d_r:
        print(d_stat, end=" ")
        print("%.2f" % round(d_stat[2], 2))

    print(f'H_{2}(X)= {H_X_mode(d_r, explain=True, mode="X^2") / 2}')


    print("\nUSLOVNOE")
    print(["Y|X", "N_{y}", "N_{x}", "p_{Y|X}", "p_{Y|X}*p_{X}*log2(p_{Y|X})",
           "p_{X} - не нужно писать, но стоит посмотреть, чтобы совпало с первой таблицей"])
    u_r = uslovnoe_raspredelenie(text)
    for u_stat in u_r:
        print(u_stat)
        # print(u_stat, "%.2f" % round(u_stat[3], 2))

    print(H_YX(u_r, True))


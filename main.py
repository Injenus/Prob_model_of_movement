# ТОЛЬКО ДЛЯ ПИТОН 3 (где словарь упорядочен!) !!!
# 0-зеленый 1-красный 2-черный 3- желтый 4-голубой (просто индикатор)
import csv
import random
import matplotlib.pyplot as plt

UNDETERMINED_START = True
RANDOM_MOVE = True
WORLD_NUMBER = 0  # номер карты

path = []
if not RANDOM_MOVE:
    for i in range(5000):
        path.append(random.randint(1, 6))
    path = [1, 1, 2, 2, 3, 2, 4, 6, 3, 2, 6, 6, 3, 1, 4, 5, 1, 1, 5, 6, 4, 2,
            1, 3, 4, 6, 6, 5, 4, 3, 2, 2, 1]

world = []

hit_color = 0.8
miss_color = 0.2

p_red = 0.8
p_green = 0.75
p_yellow = 0.60
ratio = 1 / 3
test_color = 0
stone_counter = 0

p_back = 0.05
p_stay = 0.15
p_forward = 1 - p_back - p_stay
p_turn = 0.1
p_straight = 1 - 2 * p_turn
p_exact = p_forward * p_straight

color_error_prob = 0.2

prob_tolerance = 0.01

limit_step = 30000


def filter(data):
    top = max(data)
    for i in range(len(data)):
        try:
            data[i] *= 100 / top
        except ZeroDivisionError:
            data[i] = 0

    members = [0, 0, 0]  # медианный фильтр
    for i in range(1, len(data)):
        if i < (len(data) - 1):
            members[0] = data[i - 1]
            members[1] = data[i]
            members[2] = data[i + 1]
            members.sort()
            data[i] = members[1]
        else:
            data[-2] = (data[-2] + data[-1]) / 2
            data[-1] = data[-2]

        delta = abs(data[i - 1] - data[i])  # скользящий фильтр
        k = 0.85 if delta > 3 else 0.07
        # k = 0.7
        data[i] = data[i] * k + data[i - 1] * (1 - k)

        # data[i] *= 1.1
        top = max(data)
        for i in range(len(data)):
            try:
                data[i] *= 100 / top
            except ZeroDivisionError:
                data[i] = 0


def rad_coord(center, rad):
    is_even = True if not (center[0] % 2) else False
    if is_even:
        if rad == 1:  # (a,b)
            return [((center[0] - 1) % height, (center[1]) % width),
                    ((center[0]) % height, (center[1] + 1) % width),
                    ((center[0] + 1) % height, (center[1]) % width),
                    ((center[0] + 1) % height, (center[1] - 1) % width),
                    ((center[0]) % height, (center[1] - 1) % width),
                    ((center[0] - 1) % height, (center[1] - 1) % width)]
        elif rad == 2:
            return [((center[0] - 2) % height, (center[1]) % width),
                    ((center[0] - 2) % height, (center[1] + 1) % width),
                    ((center[0] - 1) % height, (center[1] + 1) % width),
                    ((center[0]) % height, (center[1] + 2) % width),
                    ((center[0] + 1) % height, (center[1] + 1) % width),
                    ((center[0] + 2) % height, (center[1] + 1) % width),
                    ((center[0] + 2) % height, (center[1]) % width),
                    ((center[0] + 2) % height, (center[1] - 1) % width),
                    ((center[0] + 1) % height, (center[1] - 2) % width),
                    ((center[0]) % height, (center[1] - 2) % width),
                    ((center[0] - 1) % height, (center[1] - 2) % width),
                    ((center[0] - 2) % height, (center[1] - 1) % width)]
        elif rad == 3:
            return [((center[0] - 3) % height, (center[1]) % width),
                    ((center[0] - 3) % height, (center[1] + 1) % width),
                    ((center[0] - 2) % height, (center[1] + 2) % width),
                    ((center[0] - 1) % height, (center[1] + 2) % width),
                    ((center[0]) % height, (center[1] + 3) % width),
                    ((center[0] + 1) % height, (center[1] + 2) % width),
                    ((center[0] + 2) % height, (center[1] + 2) % width),
                    ((center[0] + 3) % height, (center[1] + 1) % width),
                    ((center[0] + 3) % height, (center[1]) % width),
                    ((center[0] + 3) % height, (center[1] - 1) % width),
                    ((center[0] + 3) % height, (center[1] - 2) % width),
                    ((center[0] + 2) % height, (center[1] - 2) % width),
                    ((center[0] + 1) % height, (center[1] - 3) % width),
                    ((center[0]) % height, (center[1] - 3) % width),
                    ((center[0] - 1) % height, (center[1] - 3) % width),
                    ((center[0] - 2) % height, (center[1] - 2) % width),
                    ((center[0] - 3) % height, (center[1] - 2) % width),
                    ((center[0] - 3) % height, (center[1] - 1) % width)]
        elif rad == 4:
            return [((center[0] - 4) % height, (center[1]) % width),
                    ((center[0] - 4) % height, (center[1] + 1) % width),
                    ((center[0] - 4) % height, (center[1] + 2) % width),
                    ((center[0] - 3) % height, (center[1] + 2) % width),
                    ((center[0] - 2) % height, (center[1] + 3) % width),
                    ((center[0] - 1) % height, (center[1] + 3) % width),
                    ((center[0] - 1) % height, (center[1] + 4) % width),
                    ((center[0]) % height, (center[1] + 4) % width),
                    ((center[0] + 1) % height, (center[1] + 4) % width),
                    ((center[0] + 1) % height, (center[1] + 3) % width),
                    ((center[0] + 2) % height, (center[1] + 3) % width),
                    ((center[0] + 3) % height, (center[1] + 2) % width),
                    ((center[0] + 3) % height, (center[1] - 3) % width),
                    ((center[0] + 2) % height, (center[1] - 3) % width),
                    ((center[0] - 2) % height, (center[1] - 3) % width),
                    ((center[0] - 3) % height, (center[1] - 3) % width),
                    ((center[0] - 4) % height, (center[1] - 2) % width),
                    ((center[0] - 4) % height, (center[1] - 1) % width)]
        elif rad == 5:
            return [((center[0] - 4) % height, (center[1] + 3) % width),
                    ((center[0] - 3) % height, (center[1] + 3) % width),
                    ((center[0] - 3) % height, (center[1] + 4) % width),
                    ((center[0] - 2) % height, (center[1] + 4) % width),
                    ((center[0] + 2) % height, (center[1] + 4) % width),
                    ((center[0] + 3) % height, (center[1] + 4) % width),
                    ((center[0] + 3) % height, (center[1] + 3) % width),
                    ((center[0] - 4) % height, (center[1] - 3) % width)]
        else:
            return [((center[0] - 4) % height, (center[1] + 4) % width)]
    else:
        if rad == 1:
            return [((center[0] - 1) % height, (center[1]) % width),
                    ((center[0] - 1) % height, (center[1] + 1) % width),
                    ((center[0]) % height, (center[1] + 1) % width),
                    ((center[0] + 1) % height, (center[1] + 1) % width),
                    ((center[0] + 1) % height, (center[1]) % width),
                    ((center[0]) % height, (center[1] - 1) % width)]
        elif rad == 2:
            return [((center[0] - 2) % height, (center[1]) % width),
                    ((center[0] - 2) % height, (center[1] + 1) % width),
                    ((center[0] - 1) % height, (center[1] + 2) % width),
                    ((center[0]) % height, (center[1] + 2) % width),
                    ((center[0] + 1) % height, (center[1] + 2) % width),
                    ((center[0] + 2) % height, (center[1] + 1) % width),
                    ((center[0] + 2) % height, (center[1]) % width),
                    ((center[0] + 2) % height, (center[1] - 1) % width),
                    ((center[0] + 1) % height, (center[1] - 1) % width),
                    ((center[0]) % height, (center[1] - 2) % width),
                    ((center[0] - 1) % height, (center[1] - 1) % width),
                    ((center[0] - 2) % height, (center[1] - 1) % width)]
        elif rad == 3:
            return [((center[0] - 3) % height, (center[1]) % width),
                    ((center[0] - 3) % height, (center[1] + 1) % width),
                    ((center[0] - 3) % height, (center[1] + 2) % width),
                    ((center[0] - 2) % height, (center[1] + 2) % width),
                    ((center[0] - 1) % height, (center[1] + 3) % width),
                    ((center[0]) % height, (center[1] + 3) % width),
                    ((center[0] + 1) % height, (center[1] + 3) % width),
                    ((center[0] + 2) % height, (center[1] + 2) % width),
                    ((center[0] + 3) % height, (center[1] + 2) % width),
                    ((center[0] + 3) % height, (center[1] + 1) % width),
                    ((center[0] + 3) % height, (center[1]) % width),
                    ((center[0] + 3) % height, (center[1] - 1) % width),
                    ((center[0] + 2) % height, (center[1] - 2) % width),
                    ((center[0] + 1) % height, (center[1] - 2) % width),
                    ((center[0]) % height, (center[1] - 3) % width),
                    ((center[0] - 1) % height, (center[1] - 2) % width),
                    ((center[0] - 2) % height, (center[1] - 2) % width),
                    ((center[0] - 3) % height, (center[1] - 1) % width)]
        elif rad == 4:
            return [((center[0] - 4) % height, (center[1]) % width),
                    ((center[0] - 4) % height, (center[1] + 1) % width),
                    ((center[0] - 4) % height, (center[1] + 2) % width),
                    ((center[0] - 3) % height, (center[1] + 3) % width),
                    ((center[0] - 2) % height, (center[1] + 3) % width),
                    ((center[0] - 1) % height, (center[1] + 4) % width),
                    ((center[0]) % height, (center[1] + 4) % width),
                    ((center[0] + 1) % height, (center[1] + 4) % width),
                    ((center[0] + 2) % height, (center[1] + 3) % width),
                    ((center[0] + 3) % height, (center[1] + 3) % width),
                    ((center[0] - 4) % height, (center[1] - 1) % width),
                    ((center[0] - 4) % height, (center[1] - 2) % width),
                    ((center[0] + 3) % height, (center[1] - 2) % width),
                    ((center[0] + 2) % height, (center[1] - 3) % width),
                    ((center[0] + 1) % height, (center[1] - 3) % width),
                    ((center[0] - 1) % height, (center[1] - 3) % width),
                    ((center[0] - 2) % height, (center[1] - 3) % width),
                    ((center[0] - 3) % height, (center[1] - 2) % width)]
        elif rad == 5:
            return [((center[0] - 3) % height, (center[1] + 4) % width),
                    ((center[0] - 2) % height, (center[1] + 4) % width),
                    ((center[0] + 2) % height, (center[1] + 4) % width),
                    ((center[0] + 3) % height, (center[1] + 4) % width),
                    ((center[0] - 4) % height, (center[1] + 3) % width),
                    ((center[0] - 4) % height, (center[1] - 3) % width),
                    ((center[0] + 3) % height, (center[1] - 3) % width),
                    ((center[0] - 3) % height, (center[1] - 3) % width)]
        else:
            return [((center[0] + 4) % height, (center[1] + 4) % width)]


def distance(cell1, cell2):
    for i in range(1, 7):
        if (cell2[0], cell2[1]) in rad_coord(cell1, i):
            return i
    else:
        return 'err'


def print_p(array):
    odd = True
    for stroka in array:
        odd = not odd
        if odd:
            print('   ', '   ',
                  "   ".join(['{:.3f}'.format(x) for x in stroka]))
        else:
            print('   ', "   ".join(['{:.3f}'.format(x) for x in stroka]))
    print()


def print_t(array):
    for el in array:
        print(el)
    print()


start, finish = [0, 0], [0, 0]
if WORLD_NUMBER == 1:
    NAME = 'map1.csv'
    start[0], start[1], finish[0], finish[1] = 2, 3, 5, 6
elif WORLD_NUMBER == 2:
    NAME = 'map2.csv'
    start[0], start[1], finish[0], finish[1] = 2, 3, 5, 6
elif WORLD_NUMBER == 3:
    NAME = 'map3.csv'
    start[0], start[1], finish[0], finish[1] = 2, 3, 5, 6
elif WORLD_NUMBER == 0:
    NAME = 'map0.csv'
    start[0], start[1], finish[0], finish[1] = 0, 0, 5, 5
else:
    NAME = 'doesn`t_exist'

try:
    with open(NAME, newline='') as myFile:
        reader = csv.reader(myFile, delimiter='/', quoting=csv.QUOTE_NONE)
        for el in reader:
            line = el[0].split(';')
            for i, item in enumerate(line):
                line[i] = int(item)
            for cell in line:
                if cell == '2':
                    stone_counter += 1
            world.append(line)
except NameError:
    print('Такого мира нет!')
    exit(0)
height = len(world)
width = len(world[0])

probability = [[1 / (height * width - stone_counter)] * width for i in
               range(height)]
for i in range(height):
    for j in range(width):
        if world[i][j] == '2':
            probability[i][j] = 0

print('The World:')
odd = True
for el in world:
    odd = not odd
    if odd:
        print('  ', ' ', end='')
    else:
        print('  ', end='')
    for item in el:
        print(item, end='  ')
    print()
print()


# printt(probability)
# print('########################')

def sense(prob, color):
    new_probability = [[] * width for i in range(height)]
    summ = 0
    # for i in range(height):
    #     for j in range(width):
    #         match = (color == world[i][j])
    #         new_probability[i].append(
    #             prob[i][j] * (match * hit_color + (1 - match) * miss_color))
    #         summ += new_probability[i][j]

    for i in range(height):
        for j in range(width):
            if world[i][j] == 0:
                if color == 0:
                    new_probability[i].append(prob[i][j] * p_green)
                elif color == 1:
                    new_probability[i].append(
                        prob[i][j] * (1 - p_green) * ratio)
                elif color == 3:
                    new_probability[i].append(
                        prob[i][j] * (1 - p_green) * (1 - ratio))
            elif world[i][j] == 1:
                if color == 0:
                    new_probability[i].append(prob[i][j] * (1 - p_red) * ratio)
                elif color == 1:
                    new_probability[i].append(prob[i][j] * p_red)
                elif color == 3:
                    new_probability[i].append(
                        prob[i][j] * (1 - p_red) * (1 - ratio))
            elif world[i][j] == 3:
                if color == 0:
                    new_probability[i].append(
                        prob[i][j] * (1 - p_yellow) * (1 - ratio))
                elif color == 1:
                    new_probability[i].append(
                        prob[i][j] * (1 - p_yellow) * ratio)
                elif color == 3:
                    new_probability[i].append(prob[i][j] * p_yellow)
            summ += new_probability[i][j]

    # print(summ)
    # printt(new_probability)
    # print('dfghjkjhgvghjhgfdfghujhgfcdfg')

    for i in range(height):
        for j in range(width):
            new_probability[i][j] /= summ
    return new_probability


posterior_probability = sense(probability, test_color)
print('Вероятность с учётом цвета ', test_color, ':', sep='')
print_p(posterior_probability)


def change_color(cell):
    r = random.randint(0, 1)
    if int(cell) == 0 and not r:
        return 1
    elif int(cell) == 0 and r:
        return 3
    elif int(cell) == 1 and not r:
        return 0
    elif int(cell) == 1 and r:
        return 3
    elif int(cell) == 3 and not r:
        return 0
    elif int(cell) == 3 and r:
        return 1


def maxs_coords(lst):
    precison = 10
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = round(lst[i][j], precison)
    result = []  # здесь будут коориднаты всех максимальных значений
    maximum = 0
    if type(lst[0]) == list:
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if lst[i][j] > maximum:
                    maximum = lst[i][j]
        el_counter = 0
        for i in range(len(lst)):
            strt = 0
            str_counter = 0
            for j in range(lst[i].count(maximum)):
                result.append([i, lst[i].index(maximum, strt, len(lst[i]))])
                str_counter += 1
                strt = result[el_counter + str_counter - 1][1] + 1
            el_counter += lst[i].count(maximum)
    else:
        for i in range(len(lst)):
            if lst[i] > maximum:
                maximum = lst[i]
        strt = 0
        for i in range(lst.count(maximum)):
            result.append(lst.index(maximum, strt, len(lst)))
            strt = result[i] + 1
    return result


def median(lst):
    new_lst = []
    if type(lst[0]) == list:
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                new_lst.append(lst[i][j])
    else:
        new_lst = [el for el in lst]

    new_lst.sort()
    if len(new_lst) % 2:
        return new_lst[len(new_lst) // 2]
    else:
        return (new_lst[len(new_lst) // 2] + new_lst[
            len(new_lst) // 2 - 1]) / 2


def argmax(pos):
    global predict_pos
    coord = [0, 0]
    global max_prob
    max_prob = 0
    for i in range(height):
        for j in range(width):
            if pos[i][j] > max_prob:
                max_prob = pos[i][j]
                coord[0] = i
                coord[1] = j
    med = median(pos)
    if max_prob - prob_tolerance <= med:
        print('Максимум {} неотличим от медианы {}'.format(round(max_prob, 3),
                                                           round(med, 3)))
        for i in range(len(pos)):
            for j in range(len(pos[i])):
                if pos[i][j] == med:
                    pos[i][j] = max_prob
        temp = maxs_coords(pos)
        # print(temp)
        nm = random.randint(0, len(temp) - 1)
        print('Рандомно выбрано', temp[nm], 'из', temp)
        return temp[nm]
        # max_prob = 0
        # near_prob = []
        # global el_num
        # el_num = 0
        #
        # lst_prob = rad_coord([predict_pos[0], predict_pos[1]], 1)
        # print('Список координат вероятнсрей дял выбора:', lst_prob)
        # for el in lst_prob:
        #     near_prob.append(pos[el[0]][el[1]])  # тут вероятности
        #     # на расстоянии 1 от прошлого предикт_поз
        # print('А вот сами вероятнсти', near_prob)
        # temp = sorted(near_prob)
        # print('Две наиббольшие', temp[-1], temp[-2])
        # if temp[-1] == temp[-2]:
        #     print('Есть одинаковые')
        #     el_num = random.randint(4, 5)
        #     print('Рандмно выбирали (порядковый номер в исходном):', el_num,
        #           'т.е.', [lst_prob[el_num][0], lst_prob[el_num][1]])
        #     return [lst_prob[el_num][0], lst_prob[el_num][1]]
        #
        # else:
        #     print('Одинаковых нет')
        #     for i in range(len(near_prob)):
        #         if near_prob[i] > max_prob:
        #             max_prob = near_prob[i]
        #             el_num = i
        #     print('Взяли наибольшую:', max_prob, 'т.е.',
        #           [lst_prob[el_num][0], lst_prob[el_num][1]])
        #     return [lst_prob[el_num][0], lst_prob[el_num][1]]
    else:
        print('Максимум {} явно больше медианы {}'.format(round(max_prob, 3),
                                                          round(med, 3)))
        temp = maxs_coords(pos)
        # print(temp)
        nm = random.randint(0, len(temp) - 1)
        print('Рандомно выбрано', temp[nm], 'из', temp)
        return temp[nm]


if UNDETERMINED_START:
    position = [[1 / (width * height)] * width for i in range(height)]
    predict_pos = [random.randint(0, 7), random.randint(0, 7)]
    print('Робот случайно считает, что он в', predict_pos)
    max_prob = position[0][0]
else:
    position = [[0] * width for i in range(height)]
    position[start[0]][start[1]] = 1
    predict_pos = argmax(position)
    max_prob = 1
even_flag = not (start[0] % 2)

real_pos = [start[0], start[1]]


def test_move_up_down():
    p = [[0] * width for i in range(height)]
    for i in range(height):
        for j in range(width):
            if j == (real_pos[1] + i // 2 - real_pos[0] // 2) % 8 or j == (
                    real_pos[1] + i // 2 + 4 - real_pos[0] // 2) % 8:
                p[i][j] = 1


#     print_t(p)
#     print('sfgfdgf')
# test_move_up_down()


def test_move_diagonal():
    p = [[0] * width for i in range(height)]
    for i in range(height):
        for j in range(width):
            if j == (real_pos[1] - (i + 1) // 2 + (
                    real_pos[0] - 1) // 2 + 1) % 8 or j == (
                    real_pos[1] - (i + 1) // 2 + 4 + (
                    real_pos[0] - 1) // 2 + 1) % 8:
                p[i][j] = 1


#     print_t(p)
#     print('sfgfdgf')
# test_move_diagonal()

# real_pos = [1, 6]
# even_flag = not (real_pos[0] % 2)


def test_move_horiz():
    p = [[0] * width for i in range(height)]
    for i in range(height):
        for j in range(width):
            if i == real_pos[0]:
                p[i][j] = 1
    # print_t(p)
    # print('sfgfdgf')


# test_move_horiz()

sign = lambda x: x // abs(x)  # получаем знак числа

base_point = 0
p_sum_base_point = 0


def copy_list_2d(lst):
    new_lst = [[] * len(lst[0]) for i in range(len(lst))]
    for i in range(len(lst)):
        for el in lst[i]:
            new_lst[i].append(el)
    return new_lst


def move_horiz(pos, direc, main):  # direc < 0 - назад, direc > 0 - вперёд
    global base_point
    global p_sum_base_point
    direc = sign(direc)
    # print('По горизонтали, ', direc)
    pos_new = [[] * width for i in range(height)]

    for i in range(height):
        if i == real_pos[0]:
            for j in range(width):
                if main:  # если направление основное (прямо)
                    p_sum = pos[i][
                                (j - direc) % width] * p_forward * p_straight
                    p_sum += pos[i][(j - direc + 1 * sign(
                        direc)) % width] * p_stay * p_straight
                    p_sum += pos[i][(j - direc + 2 * sign(
                        direc)) % width] * p_back * p_straight
                else:  # если направление неосновновное (поворот)
                    p_sum = pos[i][
                                (j - direc) % width] * p_forward * p_turn
                    p_sum += pos[i][(j - direc + 1 * sign(
                        direc)) % width] * p_stay * p_turn
                    p_sum += pos[i][(j - direc + 2 * sign(
                        direc)) % width] * p_back * p_turn
                pos_new[i].append(p_sum)
        else:
            for j in range(width):
                pos_new[i].append(pos[i][j])

    if main:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        pos_new[real_pos[0]][real_pos[1]] = p_sum_base_point
        p_sum_base_point = 0
    else:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        base_point = pos[real_pos[0]][real_pos[1]]

    real_pos[1] = (real_pos[1] + direc * main) % width

    return pos_new


# диагональ increas - такая, как возрастающая прямая
# диагональ decreas - такая, как убывающая прямая (ранее была up_down)

def move_increas_diag(pos, direc, main):
    global base_point
    global p_sum_base_point
    direc = sign(direc)
    global even_flag
    # pos_new = [[] * width for i in range(height)]
    pos_new = copy_list_2d(pos)
    line_new = []
    diag1 = {(0, 0): pos[0][0], (7, 0): pos[7][0], (6, 1): pos[6][1],
             (5, 1): pos[5][1], (4, 2): pos[4][2], (3, 2): pos[3][2],
             (2, 3): pos[2][3], (1, 3): pos[1][3], (0, 4): pos[0][4],
             (7, 4): pos[7][4], (6, 5): pos[6][5], (5, 5): pos[5][5],
             (4, 6): pos[4][6], (3, 6): pos[3][6], (2, 7): pos[2][7],
             (1, 7): pos[1][7]}
    diag2 = {(0, 1): pos[0][1], (7, 1): pos[7][1], (6, 2): pos[6][2],
             (5, 2): pos[5][2], (4, 3): pos[4][3], (3, 3): pos[3][3],
             (2, 4): pos[2][4], (1, 4): pos[1][4], (0, 5): pos[0][5],
             (7, 5): pos[7][5], (6, 6): pos[6][6], (5, 6): pos[5][6],
             (4, 7): pos[4][7], (3, 7): pos[3][7], (2, 0): pos[2][0],
             (1, 0): pos[1][0]}
    diag3 = {(0, 2): pos[0][2], (7, 2): pos[7][2], (6, 3): pos[6][3],
             (5, 3): pos[5][3], (4, 4): pos[4][4], (3, 4): pos[3][4],
             (2, 5): pos[2][5], (1, 5): pos[1][5], (0, 6): pos[0][6],
             (7, 6): pos[7][6], (6, 7): pos[6][7], (5, 7): pos[5][7],
             (4, 0): pos[4][0], (3, 0): pos[3][0], (2, 1): pos[2][1],
             (1, 1): pos[1][1]}
    diag4 = {(0, 3): pos[0][3], (7, 3): pos[7][3], (6, 4): pos[6][4],
             (5, 4): pos[5][4], (4, 5): pos[4][5], (3, 5): pos[3][5],
             (2, 6): pos[2][6], (1, 6): pos[1][6], (0, 7): pos[0][7],
             (7, 7): pos[7][7], (6, 0): pos[6][0], (5, 0): pos[5][0],
             (4, 1): pos[4][1], (3, 1): pos[3][1], (2, 2): pos[2][2],
             (1, 2): pos[1][2]}
    diags = (diag1, diag2, diag3, diag4)
    num = None
    coord = (real_pos[0], real_pos[1])
    for d in range(len(diags)):
        if (real_pos[0], real_pos[1]) in diags[d]:
            num = d
            break
    line = []
    # print(num)
    for key, value in diags[num].items():
        line.append(value)
    for i in range(len(line)):
        if main:
            p_sum = line[(i - direc) % len(line)] * p_forward * p_straight
            p_sum += line[(i - direc + 1 * sign(direc)) % len(
                line)] * p_stay * p_straight
            p_sum += line[(i - direc + 2 * sign(direc)) % len(
                line)] * p_back * p_straight
        else:
            p_sum = line[(i - direc) % len(line)] * p_forward * p_turn
            p_sum += line[(i - direc + 1 * sign(direc)) % len(
                line)] * p_stay * p_turn
            p_sum += line[(i - direc + 2 * sign(direc)) % len(
                line)] * p_back * p_turn
        line_new.append(p_sum)
    count = 0
    for key in diags[num]:
        pos_new[key[0]][key[1]] = line_new[count]
        count += 1

    if main:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        pos_new[real_pos[0]][real_pos[1]] = p_sum_base_point
        p_sum_base_point = 0
    else:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        base_point = pos[real_pos[0]][real_pos[1]]

    # если четное и вверх(вправо!)
    if (even_flag and (sign(direc) + 1)) or (
            not even_flag and not (sign(direc) + 1)):
        real_pos[0] = (real_pos[0] - sign(direc) * main) % height
    else:
        real_pos[0] = (real_pos[0] - sign(direc) * main) % height
        real_pos[1] = (real_pos[1] + sign(direc) * main) % width

    even_flag = not even_flag if main else even_flag

    return pos_new


def move_decreas_dig(pos, direc, main):
    global base_point
    global p_sum_base_point
    direc = sign(direc)
    global even_flag
    # pos_new = [[] * width for i in range(height)]
    pos_new = copy_list_2d(pos)
    line_new = []
    diag1 = {(0, 0): pos[0][0], (1, 0): pos[1][0], (2, 1): pos[2][1],
             (3, 1): pos[3][1], (4, 2): pos[4][2], (5, 2): pos[5][2],
             (6, 3): pos[6][3], (7, 3): pos[7][3], (0, 4): pos[0][4],
             (1, 4): pos[1][4], (2, 5): pos[2][5], (3, 5): pos[3][5],
             (4, 6): pos[4][6], (5, 6): pos[5][6], (6, 7): pos[6][7],
             (7, 7): pos[7][7]}
    diag2 = {(0, 1): pos[0][1], (1, 1): pos[1][1], (2, 2): pos[2][2],
             (3, 2): pos[3][2], (4, 3): pos[4][3], (5, 3): pos[5][3],
             (6, 4): pos[6][4], (7, 4): pos[7][4], (0, 5): pos[0][5],
             (1, 5): pos[1][5], (2, 6): pos[2][6], (3, 6): pos[3][6],
             (4, 7): pos[4][7], (5, 7): pos[5][7], (6, 0): pos[6][0],
             (7, 0): pos[7][0]}
    diag3 = {(0, 2): pos[0][2], (1, 2): pos[1][2], (2, 3): pos[2][3],
             (3, 3): pos[3][3], (4, 4): pos[4][4], (5, 4): pos[5][4],
             (6, 5): pos[6][5], (7, 5): pos[7][5], (0, 6): pos[0][6],
             (1, 6): pos[1][6], (2, 7): pos[2][7], (3, 7): pos[3][7],
             (4, 0): pos[4][0], (5, 0): pos[5][0], (6, 1): pos[6][1],
             (7, 1): pos[7][1]}
    diag4 = {(0, 3): pos[0][3], (1, 3): pos[1][3], (2, 4): pos[2][4],
             (3, 4): pos[3][4], (4, 5): pos[4][5], (5, 5): pos[5][5],
             (6, 6): pos[6][6], (7, 6): pos[7][6], (0, 7): pos[0][7],
             (1, 7): pos[1][7], (2, 0): pos[2][0], (3, 0): pos[3][0],
             (4, 1): pos[4][1], (5, 1): pos[5][1], (6, 2): pos[6][2],
             (7, 2): pos[7][2]}
    diags = (diag1, diag2, diag3, diag4)
    num = None
    coord = (real_pos[0], real_pos[1])
    for d in range(len(diags)):
        if (real_pos[0], real_pos[1]) in diags[d]:
            num = d
            break
    line = []
    # print(num)
    for key, value in diags[num].items():
        line.append(value)
    for i in range(len(line)):
        if main:
            p_sum = line[(i - direc) % len(line)] * p_forward * p_straight
            p_sum += line[(i - direc + 1 * sign(direc)) % len(
                line)] * p_stay * p_straight
            p_sum += line[(i - direc + 2 * sign(direc)) % len(
                line)] * p_back * p_straight
        else:
            p_sum = line[(i - direc) % len(line)] * p_forward * p_turn
            p_sum += line[(i - direc + 1 * sign(direc)) % len(
                line)] * p_stay * p_turn
            p_sum += line[(i - direc + 2 * sign(direc)) % len(
                line)] * p_back * p_turn
        line_new.append(p_sum)
    count = 0
    for key in diags[num]:
        pos_new[key[0]][key[1]] = line_new[count]
        count += 1

    if main:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        pos_new[real_pos[0]][real_pos[1]] = p_sum_base_point
        p_sum_base_point = 0
    else:
        p_sum_base_point += pos_new[real_pos[0]][real_pos[1]]
        base_point = pos[real_pos[0]][real_pos[1]]

    # если чётное и вправо!! (вниз)
    if (even_flag and (sign(direc) + 1)) or (
            not even_flag and not (sign(direc) + 1)):
        real_pos[0] = (real_pos[0] + sign(direc) * main) % height
    else:
        real_pos[0] = (real_pos[0] + sign(direc) * main) % height
        real_pos[1] = (real_pos[1] + sign(direc) * main) % width

    even_flag = not even_flag if main else even_flag

    return pos_new


measurment = []
print('Исходные координаты: ', start, '; робот считает, что он в: ',
      predict_pos, '\n',
      sep='')
print_p(position)


def move(m_type=0):
    global position
    if not m_type:
        case = random.randint(1, 6)
        path.append(case)
    else:
        case = m_type
    if case == 1:
        position = move_decreas_dig(position, -1, 0)  # 6
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_horiz(position, 1, 0)  # 2
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_increas_diag(position, 1, 1)  # 1
    elif case == 2:
        position = move_increas_diag(position, 1, 0)  # 1
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_decreas_dig(position, 1, 0)  # 3
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_horiz(position, 1, 1)  # 2
    elif case == 3:
        position = move_horiz(position, 1, 0)  # 2
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_increas_diag(position, -1, 0)  # 4
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_decreas_dig(position, 1, 1)  # 3
    elif case == 4:
        position = move_decreas_dig(position, 1, 0)  # 3
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_horiz(position, -1, 0)  # 5
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_increas_diag(position, -1, 1)  # 4
    elif case == 5:
        position = move_increas_diag(position, -1, 0)  # 4
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_decreas_dig(position, -1, 0)  # 6
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_horiz(position, -1, 1)  # 5
    elif case == 6:
        position = move_horiz(position, -1, 0)  # 5
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_increas_diag(position, 1, 0)  # 1
        position[real_pos[0]][real_pos[1]] = base_point
        position = move_decreas_dig(position, -1, 1)  # 6
    else:
        print('Невозможно!')
        exit(0)
    measurment.append(world[real_pos[0]][real_pos[1]])


mismatch_counter = 0
inter_mismatch_counter = 0
miscolor_counter = 0
finish_counter = 0
step = 0
pos_error = []
value_max_prob = []

if RANDOM_MOVE:
    while (step < limit_step):
        # for gg in range(509):

        color_error = False
        random_prob = random.random()
        if color_error_prob > random_prob:
            color_error = True

        value_max_prob.append(max_prob)
        move()
        print('Движение "', path[step], '":', sep='')
        print_p(position)
        predict_pos = argmax(position)
        print('Действительные координаты: ', real_pos,
              '; робот считает, что он в: ',
              predict_pos, '\n', sep='')

        if real_pos != predict_pos:
            inter_mismatch_counter += 1

        real_color = measurment[step]
        rob_color = change_color(measurment[step])
        if color_error:
            position = sense(position, rob_color)
            print('Сенсим цвет. Реальный цвет: ', real_color,
                  ', а робот считает, что: ', rob_color, sep='')
            miscolor_counter += 1
        else:
            position = sense(position, real_color)
            print('Сенсим цвет. Реальный цвет: ', real_color,
                  ', и робот с этим согласен', sep='')

        print_p(position)
        predict_pos = argmax(position)
        print('Действительные координаты: ', real_pos,
              '; робот считает, что он в: ',
              predict_pos, '\n', sep='')

        if real_pos != predict_pos:
            mismatch_counter += 1
            pos_error.append(distance(real_pos, predict_pos))
        else:
            pos_error.append(0)

        if int(
                real_color) == 3 and max_prob > 0.2 and predict_pos == finish or int(
            real_color) != 3 and max_prob > 0.8 and predict_pos == finish:
            print('Доехали до финиша! Робот распознал его с',
                  finish_counter + 1,
                  'раза.')
            break

        if real_pos == finish:
            finish_counter += 1
        step += 1
    else:
        step -= 1
        print(
            'Робот разрядился, но так и не доехал! Проезжал мимо финиша раз:',
            finish_counter)
    # pos_error.append(0)
    # step += 1
    step += 1
else:
    for go in path:
        color_error = False
        random_prob = random.random()
        if color_error_prob > random_prob:
            color_error = True

        value_max_prob.append(max_prob)
        move(go)
        print('Движение "', path[step], '":', sep='')
        print_p(position)
        predict_pos = argmax(position)
        print('Действительные координаты: ', real_pos,
              '; робот считает, что он в: ',
              predict_pos, '\n', sep='')

        if real_pos != predict_pos:
            inter_mismatch_counter += 1

        real_color = measurment[step]
        rob_color = change_color(measurment[step])
        if color_error:
            position = sense(position, rob_color)
            print('Сенсим цвет. Реальный цвет: ', real_color,
                  ', а робот считает, что: ', rob_color, sep='')
            miscolor_counter += 1
        else:
            position = sense(position, real_color)
            print('Сенсим цвет. Реальный цвет: ', real_color,
                  ', и робот с этим согласен', sep='')

        print_p(position)
        predict_pos = argmax(position)
        print('Действительные координаты: ', real_pos,
              '; робот считает, что он в: ',
              predict_pos, '\n', sep='')

        if real_pos != predict_pos:
            mismatch_counter += 1
            pos_error.append(distance(real_pos, predict_pos))
        else:
            pos_error.append(0)

        step += 1

if UNDETERMINED_START:
    print('Робот изначально не знал своё местоположение.')
else:
    print('Робот изначально знал своё местоположение.')
print('Вероятность точного перемещения робота (куда он хотел):',
      '{:.3f}'.format(p_exact))
print('Вероятность ложного определения цвета: ',
      '{:.3f}'.format(color_error_prob))
print('Робот проехал ячеек:', step)
print('Ошибок датчка цвета:', miscolor_counter)
print('Ошибок навигационной системы: ', mismatch_counter,
      ' (промежуточных ошибок: ', inter_mismatch_counter, ')', sep='')
print('Путь:', path)
print('Данные датчика:', measurment)

print('Ошибки', pos_error)
print('Вероятности', value_max_prob)

plt.figure(
    'Зависимость ошибки системы навигации от пройденного пути (фактически от времени)')
plt.subplot(2, 2, 1)
plt.title('Зависимость ошибки системы навигации от времени')
plt.ylabel('Расстояние между действительным положением и вычисляемым')
plt.xlabel(
    'Время в единицах равных времени проезда на 1 ячейку')
x = [i for i in range(step)]
plt.plot(x, pos_error)
plt.grid()

filter(pos_error)

plt.subplot(2, 2, 2)
plt.title(
    'Фильтрованная зависимость ошибки системы навигации от времени')
plt.ylabel('Условные единицы ошибки')
plt.xlabel('Время в единицах равных времени проезда на 1 ячейку')
x = [i for i in range(step)]
plt.plot(x, pos_error)
plt.grid()

# plt.figure(
#     'Зависимость величины максимальной вероятности местоположения робота от времени')
plt.subplot(2, 2, 3)
plt.title(
    'Максимальная вероятность местоположения робота от времени')
plt.ylabel('Максимальная вероятность')
plt.xlabel(
    'Время в единицах равных времени проезда на 1 ячейку')
x = [i for i in range(step)]
plt.plot(x, value_max_prob)
plt.grid()

filter(value_max_prob)

plt.subplot(2, 2, 4)
plt.title(
    'Фильтрованная максимальная вероятность местоположения робота от времени')
plt.ylabel('Максимальная вероятность')
plt.xlabel(
    'Время в единицах равных времени проезда на 1 ячейку')
x = [i for i in range(step)]
plt.plot(x, value_max_prob)
plt.grid()

plt.show()

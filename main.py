import csv
import random

WORLD_NUMBER = 0


# 0-зеленый 1-красный 2-черный 3- желтый 4-голубой (просто индикатор)

def print_p(array):
    odd = True
    for stroka in array:
        odd = not odd
        if odd:
            print('   ', '   ',
                  ",  ".join(['{:.3f}'.format(x) for x in stroka]))
        else:
            print('   ', ",  ".join(['{:.3f}'.format(x) for x in stroka]))
    print('\n')


def print_t(array):
    for el in array:
        print(el)


width = 8
height = 8

world = []

hit = 0.8
miss = 0.1
test_color = '0'
stone_counter = 0

p_back = 0.05
p_stay = 0.1
p_exact = 1 - p_back - p_stay

if WORLD_NUMBER == 1:
    NAME = 'map1.csv'
    start = (2, 3)
    finish = (5, 6)
elif WORLD_NUMBER == 2:
    NAME = 'map2.csv'
    start = (2, 3)
    finish = (5, 6)
elif WORLD_NUMBER == 3:
    NAME = 'map3.csv'
    start = (2, 3)
    finish = (5, 6)
elif WORLD_NUMBER == 0:
    NAME = 'map0.csv'
    start = (0, 0)
    finish = (5, 5)

try:
    with open(NAME, newline='') as myFile:
        reader = csv.reader(myFile, delimiter='/', quoting=csv.QUOTE_NONE)
        for el in reader:
            temp = el[0].split(';')
            for cell in temp:
                if cell == '2':
                    stone_counter += 1
            world.append(temp)
except NameError:
    print('Такого мира нет!')
    exit(0)

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
        item = int(item)
        print(item, end='  ')
    print()


# printt(probability)
# print('########################')

def sense(prob, color):
    new_probability = [[] * width for i in range(height)]
    summ = 0
    for i in range(height):
        for j in range(width):
            match = (color == world[i][j])
            new_probability[i].append(
                prob[i][j] * (match * hit + (1 - match) * miss))
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

position = [[0] * width for i in range(height)]
position[start[0]][start[1]] = 1
# position = [[i * width + j + 10 for j in range(width)] for i in range(height)]
even_flag = not (start[0] % 2)


def max_in_table():
    pass


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


def move_horiz(pos, direc):  # direc < 0 - назад, direc > 0 - вперёд
    # print('По горизонтали, ', direc)
    pos_new = [[] * width for i in range(height)]
    for i in range(height):
        if i == real_pos[0]:
            for j in range(width):
                p_sum = pos[i][(j - direc) % width] * p_exact
                p_sum += pos[i][(j - direc + 1 * sign(direc)) % width] * p_stay
                p_sum += pos[i][(j - direc + 2 * sign(direc)) % width] * p_back
                pos_new[i].append(p_sum)
        else:
            for j in range(width):
                pos_new[i].append(pos[i][j])
    real_pos[1] += direc
    return pos_new


# диагональ increas - такая, как возрастающая прямая
# диагональ decreas - такая, как убывающая прямая (ранее была up_down)

def move_increas_diag(pos, direc):
    pos_new = [[] * width for i in range(height)]
    diag1 = {(0, 0): pos[0][0], (7, 0): pos[7][0], (6, 1): pos[6][1], (5, 1): pos[5][1], (4, 2): pos[4][2], (3, 2): pos[3][2], (2, 3): pos[2][3], (1, 3): pos[1][3], (0, 4): pos[0][4], (7, 4): pos[7][4], (6, 5): pos[6][5], (5, 5): pos[5][5], (4, 6): pos[4][6], (3, 6): pos[3][6], (2, 7): pos[2][7], (1, 7): pos[1][7]}
    diag2 = {(0, 1): pos[0][1], (7, 1): pos[7][1], (6, 2): pos[6][2], (5, 2): pos[5][2], (4, 3): pos[4][3], (3, 3): pos[3][3], (2, 4): pos[2][4], (1, 4): pos[1][4], (0, 5): pos[0][5], (7, 5): pos[7][5], (6, 6): pos[6][6], (5, 6): pos[5][6], (4, 7): pos[4][7], (3, 7): pos[3][7], (2, 0): pos[2][0], (1, 0): pos[1][0]}
    diag3 = {(0, 2): pos[0][2], (7, 2): pos[7][2], (6, 3): pos[6][3], (5, 3): pos[5][3], (4, 4): pos[4][4], (3, 4): pos[3][4], (2, 5): pos[2][5], (1, 5): pos[1][5], (0, 6): pos[0][6], (7, 6): pos[7][6], (6, 7): pos[6][7], (5, 7): pos[5][7], (4, 0): pos[4][0], (3, 0): pos[3][0], (2, 1): pos[2][1], (1, 1): pos[1][1]}
    diag4 = {(0, 3): pos[0][3], (7, 3): pos[7][3], (6, 4): pos[6][4], (5, 4): pos[5][4], (4, 5): pos[4][5], (3, 5): pos[3][5], (2, 6): pos[2][6], (1, 6): pos[1][6], (0, 7): pos[0][7], (7, 7): pos[7][7], (6, 0): pos[6][0], (5, 0): pos[5][0], (4, 1): pos[4][1], (3, 1): pos[3][1], (2, 2): pos[2][2], (1, 2): pos[1][2]}
    for i in range(height):
        for j in range(width):
            pass


def move_increas_up(pos, direc):
    pos_new = [[] * width for i in range(height)]
    diag1 = {(0, 0): pos[0][0], (1, 0): pos[1][0], (2, 1): pos[2][1], (3, 1): pos[3][1], (4, 2): pos[4][2], (5, 2): pos[5][2], (6, 3): pos[6][3], (7, 3): pos[7][3], (0, 4): pos[0][4], (1, 4): pos[1][4], (2, 5): pos[2][5], (3, 5): pos[3][5], (4, 6): pos[4][6], (5, 6): pos[5][6], (6, 7): pos[6][7], (7, 7): pos[7][7]}
    diag2 = {(0, 1): pos[0][1], (1, 1): pos[1][1], (2, 2): pos[2][2], (3, 2): pos[3][2], (4, 3): pos[4][3], (5, 3): pos[5][3], (6, 4): pos[6][4], (7, 4): pos[7][4], (0, 5): pos[0][5], (1, 5): pos[1][5], (2, 6): pos[2][6], (3, 6): pos[3][6], (4, 7): pos[4][7], (5, 7): pos[5][7], (6, 0): pos[6][0], (7, 0): pos[7][0]}
    diag3 = {(0, 2): pos[0][2], (1, 2): pos[1][2], (2, 3): pos[2][3], (3, 3): pos[3][3], (4, 4): pos[4][4], (5, 4): pos[5][4], (6, 5): pos[6][5], (7, 5): pos[7][5], (0, 6): pos[0][6], (1, 6): pos[1][6], (2, 7): pos[2][7], (3, 7): pos[3][7], (4, 0): pos[4][0], (5, 0): pos[5][0], (6, 1): pos[6][1], (7, 1): pos[7][1]}
    diag4 = {(0, 3): pos[0][3], (1, 3): pos[1][3], (2, 4): pos[2][4], (3, 4): pos[3][4], (4, 5): pos[4][5], (5, 5): pos[5][5], (6, 6): pos[6][6], (7, 6): pos[7][6], (0, 7): pos[0][7], (1, 7): pos[1][7], (2, 0): pos[2][0], (3, 0): pos[3][0], (4, 1): pos[4][1], (5, 1): pos[5][1], (6, 2): pos[6][2], (7, 2): pos[7][2]}
    for i in range(height):
        for j in range(width):
            pass


move_increas_diag(position, 1)
print('Исходное:')
print_p(position)

path = []
measurment = []


def random_move(num=1):
    global position
    for count in range(num):
        case = random.randint(1, 6)
        case = 2
        path.append(case)
        if case == 1:
            if even_flag:
                measurment.append(world[real_pos[0] - 1][real_pos[1]])
            else:
                measurment.append(world[real_pos[0] - 1][real_pos[1] + 1])
        elif case == 2:
            position = move_horiz(position, 1)
            measurment.append(world[real_pos[0]][real_pos[1] + 1])
        elif case == 3:
            if even_flag:
                measurment.append(world[real_pos[0] + 1][real_pos[1]])
            else:
                measurment.append(world[real_pos[0] + 1][real_pos[1] + 1])
        elif case == 4:
            if even_flag:
                measurment.append(world[real_pos[0] + 1][real_pos[1] - 1])
            else:
                measurment.append(world[real_pos[0] + 1][real_pos[1]])
        elif case == 5:
            position = move_horiz(position, -1)
            measurment.append(world[real_pos[0]][real_pos[1] - 1])
        elif case == 6:
            if even_flag:
                measurment.append(world[real_pos[0] - 1][real_pos[1] - 1])
            else:
                measurment.append(world[real_pos[0] - 1][real_pos[1]])
        else:
            print('Невозможно!')
            exit(0)


for step in range(5):
    random_move()
    print('After move "', path[step], '":', sep='')
    print_p(position)
    position = sense(position, measurment[step])
    print('After sense:')
    print_p(position)
    # position = sense(position, measurment[step])
    # print('After sense:')
    # print_p(position)

# print('Путь:')
# print(path)
# print('Данные датчика:')
# print(measurment)


##### ТО К ЧЕМУ НЕ НАВЕСИТЬ ВЕРОЯТНОСТЬ !!!!!! (((((((
# #   num всегда -1 или 1!!!!!!!!!!!!!
# def vertical_move(pos, num):  # стркоа чётная (с 0) - вверх-вправо
#     global even_flag
#     # pos_new = [[0] * width for i in range(height)]
#     # for i in range(height):
#     #     for j in range(width):
#     #         if j == real_pos[1]:
#     #             pos_new[i][j] = pos[(i + num) % height][j]
#     #         else:
#     #             pos_new[i][j] = pos[i][j]
#     # real_pos[0] = (real_pos[0] - num) % height
#     # if even_flag:
#     #     pos_new[real_pos[0]-num][real_pos[1]-1]=p_left*pos_new[real_pos[0]][real_pos[1]]
#     #     pos_new[real_pos[0]][real_pos[1]+1]=p_right*pos_new[real_pos[0]][real_pos[1]]
#     # else:
#     #     pos_new[real_pos[0]][real_pos[1] - 1] = p_left*pos_new[real_pos[0]][real_pos[1]]
#     #     pos_new[real_pos[0]-num][real_pos[1] + 1] = p_right*pos_new[real_pos[0]][real_pos[1]]
#     # pos_new[real_pos[0]][real_pos[1]] *= p_exact
#     beginnig_j = ()
#     for i in range(height):
#         for j in range(width):
#             if j == real_pos[1]:
#                 pass
#
#     if num % 2:  # если num нечётное, что флаг чётности меняется
#         even_flag = not even_flag
#     return pos
#
#
# def horizontal_move(pos, num, prob):
#     pos_new = [[0] * width for i in range(height)]
#     for i in range(height):
#         if i == real_pos[0]:
#             for j in range(width):
#                 pos_new[i][j] = pos[i][(j - num) % width] * prob
#         else:
#             pos_new[i] = pos[i]
#         if even_flag:
#             pass
#     real_pos[1] = (real_pos[1] + num) % width
#     return pos_new
#
#
# def diag_increas_move(pos, num, prob):
#     global even_flag
#     pos_new = [[0] * width for i in range(height)]
#     coord_sum = (real_pos[0] + real_pos[1]) % 8
#     for i in range(height):
#         for j in range(width):
#             if (i + j) % 8 == coord_sum:
#                 pos_new[i][j] = pos[(i + num) % height][
#                                     (j - num) % width] * prob
#             else:
#                 pos_new[i][j] = pos[i][j]
#     real_pos[0] = (real_pos[0] - num) % height
#     real_pos[1] = (real_pos[1] + num) % width
#     if num % 2:  # если num нечётное, что флаг чётности меняется
#         even_flag = not even_flag
#     return pos_new
#
#
# def diag_decreas_move(pos, num, prob):
#     global even_flag
#     pos_new = [[0] * width for i in range(height)]
#     coord_dif = (real_pos[0] - real_pos[1]) % 8
#     for i in range(height):
#         for j in range(width):
#             if (i - j) % 8 == coord_dif:
#                 pos_new[i][j] = pos[(i + num) % height][
#                                     (j + num) % width] * prob
#             else:
#                 pos_new[i][j] = pos[i][j]
#     real_pos[0] = (real_pos[0] - num) % height
#     real_pos[1] = (real_pos[1] - num) % width
#     if num % 2:  # если num нечётное, что флаг чётности меняется
#         even_flag = not even_flag
#     return pos_new
#
#
# print_t(position)
# print('-----------')
# # position = vertical_move(position, -3)
# # print_t(position)
# # print(real_pos)
# #
# # position = horizontal_move(position, 2)
# # print_t(position)
# # print(real_pos)
# #
# # position = diagonal_move(position, 12)
# # print_t(position)
# # print(real_pos)
# # position=diag_decreas_move(position,1)
# # print_t(position)
# # print(real_pos)
#
# track = []
#
#
# def simple_move():
#     global position
#     # case = random.randint(1, 6)
#     case = 3
#     track.append(case)
#     if case == 1:
#         if even_flag:
#             position = vertical_move(position, 1)
#         else:
#             position = diag_increas_move(position, 1)
#     elif case == 2:
#         if even_flag:
#             position = vertical_move(position, 1)
#             position = horizontal_move(position, 1, p_exact)
#             position = vertical_move(position, -1)
#         else:
#             position = diag_increas_move(position, 1, p_left)
#             position = horizontal_move(position, 1, p_exact)
#             position = diag_decreas_move(position, -1, p_right)
#     elif case == 3:
#         if even_flag:
#             position = vertical_move(position, -1)
#         else:
#             position = diag_decreas_move(position, -1, p_exact)
#     elif case == 4:
#         if even_flag:
#             position = vertical_move(position, -1)
#             position = diag_increas_move(position, -1, p_exact)
#             position = horizontal_move(position, -1, p_right)
#         else:
#             position = diag_decreas_move(position, -1, p_left)
#             position = vertical_move(position, -1)
#             position = horizontal_move(position, -1, p_right)
#     elif case == 5:
#         if even_flag:
#             position = diag_increas_move(position, -1, p_left)
#             position = horizontal_move(position, -1, p_exact)
#             position = diag_decreas_move(position, 1, p_right)
#         else:
#             position = vertical_move(position, -1)
#             position = horizontal_move(position, -1, p_exact)
#             position = vertical_move(position, 1)
#     elif case == 6:
#         if even_flag:
#             position = horizontal_move(position, -1, p_left)
#             position = diag_decreas_move(position, 1, p_exact)
#             position = vertical_move(position, 1)
#         else:
#             position = horizontal_move(position, -1, p_left)
#             position = vertical_move(position, 1)
#             position = diag_increas_move(position, 1, p_right)
#     else:
#         print('Не может быть!')
#         exit(0)
#
#
# for i in range(1): simple_move()
# print(track)
# print_p(position)
# print(real_pos)

# ТОЛЬКО ДЛЯ ПИТОН 3 (где словарь упорядочен!) !!!
# 0-зеленый 1-красный 2-черный 3- желтый 4-голубой (просто индикатор)
import csv
import random

WORLD_NUMBER = 0  # номер карты

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

color_error_prob = 0.2


def print_p(array):
    odd = True
    for stroka in array:
        odd = not odd
        if odd:
            print('   ', '   ',
                  ",  ".join(['{:.3f}'.format(x) for x in stroka]))
        else:
            print('   ', ",  ".join(['{:.3f}'.format(x) for x in stroka]))
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

try:
    with open(NAME, newline='') as myFile:
        reader = csv.reader(myFile, delimiter='/', quoting=csv.QUOTE_NONE)
        for el in reader:
            line = el[0].split(';')
            for cell in line:
                if cell == '2':
                    stone_counter += 1
            world.append(line)
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


def argmax(pos):
    coord = [0, 0]
    global max_prob
    max_prob = 0
    for i in range(height):
        for j in range(width):
            if pos[i][j] > max_prob:
                max_prob = pos[i][j]
                coord[0] = i
                coord[1] = j
    # print(max_prob)
    return coord


# position = [[0] * width for i in range(height)]
# position[start[0]][start[1]] = 1
position = [[1 / (width * height)] * width for i in range(height)]
even_flag = not (start[0] % 2)
max_prob = 1

predict_pos = argmax(position)
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
    direc = sign(direc)
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
    real_pos[1] = (real_pos[1] + direc) % width
    return pos_new


# диагональ increas - такая, как возрастающая прямая
# диагональ decreas - такая, как убывающая прямая (ранее была up_down)

def move_increas_diag(pos, direc):
    direc = sign(direc)
    global even_flag
    # pos_new = [[] * width for i in range(height)]
    pos_new = pos.copy()
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
        p_sum = line[(i - direc) % len(line)] * p_exact
        p_sum += line[(i - direc + 1 * sign(direc)) % len(line)] * p_stay
        p_sum += line[(i - direc + 2 * sign(direc)) % len(line)] * p_back
        line_new.append(p_sum)
    count = 0
    for key in diags[num]:
        pos_new[key[0]][key[1]] = line_new[count]
        count += 1
    # если четное и вверх(вправо!)
    if (even_flag and (sign(direc) + 1)) or (
            not even_flag and not (sign(direc) + 1)):
        real_pos[0] = (real_pos[0] - sign(direc)) % height
    else:
        real_pos[0] = (real_pos[0] - sign(direc)) % height
        real_pos[1] = (real_pos[1] + sign(direc)) % width
    even_flag = not even_flag
    return pos_new


def move_decreas_dig(pos, direc):
    direc = sign(direc)
    global even_flag
    # pos_new = [[] * width for i in range(height)]
    pos_new = pos.copy()
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
        p_sum = line[(i - direc) % len(line)] * p_exact
        p_sum += line[(i - direc + 1 * sign(direc)) % len(line)] * p_stay
        p_sum += line[(i - direc + 2 * sign(direc)) % len(line)] * p_back
        line_new.append(p_sum)
    count = 0
    for key in diags[num]:
        pos_new[key[0]][key[1]] = line_new[count]
        count += 1
    # если чётное и вправо!! (вниз)
    if (even_flag and (sign(direc) + 1)) or (
            not even_flag and not (sign(direc) + 1)):
        real_pos[0] = (real_pos[0] + sign(direc)) % height
    else:
        real_pos[0] = (real_pos[0] + sign(direc)) % height
        real_pos[1] = (real_pos[1] + sign(direc)) % width
    even_flag = not even_flag
    return pos_new


path = []
measurment = []
print('Исходное:')
print_p(position)


def random_move(num=1):
    global position
    for n in range(num):
        case = random.randint(1, 6)
        path.append(case)
        if case == 1:
            position = move_increas_diag(position, 1)
        elif case == 2:
            position = move_horiz(position, 1)
        elif case == 3:
            position = move_decreas_dig(position, 1)
        elif case == 4:
            position = move_increas_diag(position, -1)
        elif case == 5:
            position = move_horiz(position, -1)
        elif case == 6:
            position = move_decreas_dig(position, -1)
        else:
            print('Невозможно!')
            exit(0)
        measurment.append(world[real_pos[0]][real_pos[1]])


mismath_counter = 0
miscolor_counter = 0
finish_counter = 0
step = 0
while (True):
    # for gg in range(509):
    color_error = False
    random_prob = random.random()
    if color_error_prob > random_prob:
        color_error = True
    random_move()
    print('Движение "', path[step], '":', sep='')
    print_p(position)
    predict_pos = argmax(position)
    print('Действительные координаты: ', real_pos,
          '; робот считает, что он в: ',
          predict_pos, '\n', sep='')
    if real_pos != predict_pos:
        mismath_counter += 1
    real_color = measurment[step]
    rob_color = change_color(measurment[step])
    if color_error:
        position = sense(position, rob_color)
        print('Сенсим цвет. Реальный цвет: ', real_color,
              ', а робот считает, что: ', rob_color)
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
        mismath_counter += 1
    if int(
            real_color) == 3 and max_prob > 0.2 and predict_pos == finish or int(
        real_color) != 3 and max_prob > 0.8 and predict_pos == finish:
        print('Доехали до финиша! Робот распознал его с', finish_counter + 1,
              'раза.')
        break
    if real_pos == finish:
        finish_counter += 1
    step += 1
print('Робот проехал ячеек:', step)
print('Вероятность ложного определения цвета: ', color_error_prob * 100, '%',
      sep='')
print('Ошибок датчка цвета:', miscolor_counter)
print('Ошибок навигационной системы:', mismath_counter)
print('Путь:', path)
print('Данные датчика:', measurment)
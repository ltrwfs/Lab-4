LENGTH = 4
WIDTH = 2
MAX_VOLUME = LENGTH*WIDTH - 1        # Вычитаем 1 т.к. берём антидот сразу же
basic_points = 10

items = {
    'r' : { 'points': 25, 'volume': 3},
    'p' : { 'points': 15, 'volume': 2},
    'a' : { 'points': 15, 'volume': 2},
    'm' : { 'points': 20, 'volume': 2},
    'i' : { 'points': 5, 'volume': 1},
    'k' : { 'points': 15, 'volume': 1},
    'x' : { 'points': 20, 'volume': 3},
    't' : { 'points': 25, 'volume': 1},
    'f' : { 'points': 15, 'volume': 1},
    's' : { 'points': 20, 'volume': 2},
    'c' : { 'points': 20, 'volume': 2},

}

items_list = list(items.values())
items_names = list(items.keys())


def gen_table(items, max_volume=MAX_VOLUME):
    table = [[0 for c in range(max_volume)] for _ in range(len(items))]
    for i, (_, value) in enumerate(items.items()):
        points = value['points']
        volume = value['volume']

        for limit_volume in range(1, max_volume+1):
            col = limit_volume - 1
            if i == 0:
                table[i][col] =  0 if volume > limit_volume else points
            else:
                prev_points = table[i-1][col]
                if volume > limit_volume:
                    table[i][col] = prev_points
                else:
                    used =  0 if col < volume else table[i-1][col-volume]
                    new_points = used + points

                    res = max(new_points, prev_points)
                    table[i][col] = res 
    return table


# По таблице определяем, какие предметы взяли и считаем очки выживания
def define_items(table):
    all_points = 0
    for item in items:
        all_points += items[item]['points']
    points = max(table[-1])
    score = basic_points + points - (all_points - points)

    index = table[-1].index(points)
    line = len(table) - 1
    chosen_items = []
    while (line > 0) and (table[line][index] > 0):
        while table[line-1][index] == table[line][index]:
            line -= 1
        chosen_items.append(line)
        if index >= items_list[line]['volume']:
            index -= items_list[line]['volume']
        else:
            index = 0
        line -= 1
    
    items['d'] = {'points': 10, 'volume': 1}
    items_names.append('d')
    items_list.append(items['d'])
    chosen_items.append(len(items)-1)
    score += items['d']['points']
    
    return chosen_items, score


def pack(items, length=LENGTH, width=WIDTH):
    volumes = {        # Сортируем предметы по объёму
        1: [], 
        2: [], 
        3: [], 
        4: [],

    }
    for item in items:
        volume = items_list[item]['volume']
        volumes[volume].append(f'[{items_names[item]}]')
    backpack = [[0] * length for _ in range(width)]
    
    while len(volumes[3]) > 0:
        if backpack[0][0] == 0:
            for i in range(3):
                backpack[0][i] = volumes[3][0]
            volumes[3].pop(0)
        else:
            for i in range(3):
                backpack[1][i] = volumes[3][0]
            volumes[3].pop(0)

    while len(volumes[2]) > 0:
        if backpack[0][0] == 0:
            backpack[0][0] = volumes[2][0]
            backpack[0][1] = volumes[2][0]
        elif backpack[0][2] == 0:
            backpack[0][2] = volumes[2][0]
            backpack[0][3] = volumes[2][0]
        elif backpack[0][3] == 0:
            backpack[0][3] = volumes[2][0]
            backpack[1][3] = volumes[2][0]
        elif backpack[1][0] == 0:
            backpack[1][0] = volumes[2][0]
            backpack[1][1] = volumes[2][0]
        else:
            backpack[1][2] = volumes[2][0]
            backpack[1][3] = volumes[2][0]
        volumes[2].pop(0)

    for l in range(length):
        if len(volumes[1]) == 0: break
        for w in range(width):
            if len(volumes[1]) == 0: break
            if backpack[w][l] == 0:
                backpack[w][l] = volumes[1][0]
                volumes[1].pop(0)

    return backpack


if __name__ == '__main__':
    table = gen_table(items)
    i = 0
    chosen_items, score = define_items(table)
    backpack = pack(chosen_items)

    for line in backpack:
        print(*line, sep=',')
    print('Итоговые очки выживания:',score) 
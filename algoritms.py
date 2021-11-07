from collections import deque
from queue import PriorityQueue
from copy import deepcopy

def dijkstra(result, map, start, end):
    # Реализация алгоритма дейкстры.

    # На вход принимает 4-ре параметра
    # result - синхронизированная очередь, через которую алгоритм отсылает результаты своей работы.
    #          Первый зашел - первый вышел
    # map    - map - карта - двумерный числовой массив.
    #          0 означает непроходимое препятствие
    #          Все прочие числа означают стоимость перехода
    # start  - координаты точки старта в формате [i, j], где i - строка, а j - столбец
    # end    - координаты конечной точки в формате [i, j]

    start = [start[0], start[1], 0  ]
    # Создаем массив из 3-х элементов. [i, j, d], где d - длинна кратчайшего пути до этой точки

    end   = [end[0]  , end[1]  , 1_000_000]
    # Аналогично

    map_size = [len(map), len(map[0])]
    # Узнаем и запоминаем размер карты. Пригодится чтобы проверять,
    # не вышли мы за ее пределы, когда будем брать соседей клетки


    visited = [0]*map_size[0]
    for i in range(0, map_size[0]):
        visited[i] = [0]*map_size[1]
    visited[start[0]][start[1]] = 1
    # Создаем массив посещенных клеток, все элементы которого
    # За исключением стартовой клетки имеют значение 0
    # 1 - клетка посещена. 2 - клетка не была посещена
    # В самом алгоритме роли не играет, но отправляется интерфейсу
    # Чтобы он знал, какие клетки отмечать как пройденные

    nums = [1_000_000]*map_size[0]
    for i in range(0, map_size[0]):
        nums[i] = [1_000_000]*map_size[1]
    nums[start[0]][start[1]] = 0
    # Создаем массив минимальных дистанций до клеток
    # Элемент nums[i][j] хранит в себе значение длинны минимального пути до клетки [i][j]
    # Изначально минимальная дистанция принимается за миллион, что созвучно с бесконечностью,
    # а потому все ячейки массива, за исключением ячейки старта хранят в себе миллион. Минимальный путь до старта 0

    result.put([deepcopy(visited), deepcopy(nums)])
    # Отправляем интерфейсу изначальное состояние, которое мы имеем.
    # Это будет нулевым кадром работы алгоритма

    frontier = PriorityQueue()
    frontier.put([0, start])
    # Создаем очередь с приоритетом которая будет хранить перечень граничных клеток и помещаем туда стартовую клетку с приоритетом 0
    # Очередь с приоритетом - первым выходит тот, у кого первый элемент массива самый маленький
    # Таким образом в первую очередь очередь будет выбирать граничные клетки с самым маленьким путем до них

    find_end = False
    # Создаем переменную, по которой будем смотреть нашли ли мы конечную точку.
    # Нужна чтобы не восстанавливать маршрут до конечной точки, если таковая не была достигнута

    frontier_size = 1
    # Кол-во клеток на границе. Сколько клеток граничит с неисследованными местами, столько мы и рассмотрим,
    # Прежде чем сохраним еще один кадр работы алгоритма
    # Отвечает за то, чтобы алгоритм показывал не то, как он рассматривал каждую клетку за шаг,
    # а то как изменилась вся граница целиком за один шаг

    while not frontier.empty() and not find_end:
    # Пока на границе есть клетки, которые можно рассмотреть и мы еще не встретили конечную клетку
        a = frontier_size # Запоминаем размер границы
        for c in range(0, a): # И ровно столько сколько элементов на границе в данный, столько мы и рассмотрим за один подход
            current = frontier.get()[1] # Просим дать нам клетку на границе с минимальным путем до нее
            frontier_size -= 1          # Забрали клетку на рассмотрение, уменьшили размер границы
            if current[0] == end[0] and current[1] == end[1]: # Если текущая рассматриваемая клетка равна конечной, то
                end[2] = current[2] # Минимальный путь до конечной равен минимальному пути до рассматриваемой
                find_end = True     # Путь найден
                break

            neigbours = get_neigbours_cross(current[0], current[1], map_size)
            # Получаем соседей текущей клетки сверху, снизу, слева и справа
            # Каждый сосед это его координаты на карте в формате [i, j]
            for i, j in neigbours:  # Для всех соседей
                if map[i][j] == 0:  # Если это препятствие, то пропускаем этого нерадивого соседа
                    continue
                visited[i][j] = 1    # Отмечаем его как посещенного
                d = current[2] + map[i][j]  # Расчитываем кратчайший путь до него
                                            # как путь до текущй клетки + стоимость перехода в него(вес клетки)
                if d < nums[i][j]:          # Если новый путь оказался короче, чем тот, что мы запомнили ранее
                    nums[i][j] = d          # Тогда обновляем значение в карте минимальных путей
                    frontier.put([d, [i, j, d]])
                    # Если мы здесь, то мы пересмотрели путь до данной клетки, а следовательно
                    # Нужно пересмотреть путь и до соседних.
                    # Мы добавляем текущую клетку к границе
                    frontier_size += 1 # И увеличиваем счетчик размера границы

        result.put([deepcopy(visited), deepcopy(nums)])
        # Каждый раз, когда мы рассмотрели столько клеток, сколько было в границе на начало цикла for,
        # т.е. каждый раз, когда мы сдвинули всю границу на шаг вперед
        # Мы отсылаем это интерфесу чтобы он это поймал, запомнил и показывал пользователю

    result.put("endOfAlgorithm")
    # Когда цикл while завершится мы передаем интерфейсу сигнал о том, что поиск окончен.

    # Восстанавливаем путь
    if find_end:
        # Только если мы достигли конечной точки
        path = [] # Путь будем хранить тут
        path.append([current[0], current[1]]) # Добавляем в путь [i, j] текущей точки
        min = 1_000_000
        # Нам нужно будет переходить на того соседа, у кого самый короткий путь
        # Изначально самый короткий путь принимаем за миллион
        while min != 0:
        # До тех пор пока самый короткий путь не равен 0
        # т.е. не достигнуто начало
            min = 1_000_000 # Каждый раз сбрасываем самый минимальный путь
            min_pos = []    # Сбрасываем координаты соседа с самым минимальным путем
            neigbours = get_neigbours_square(current[0], current[1], map_size)
            # Запрашиваем все 8 соседей вокруг клетки
            for i, j in neigbours:   # и для каждого
                if nums[i][j] < min:
                    min = nums[i][j]
                    min_pos = [i, j]
                    # находим и запоминаем координаты соседа с самым минимальным путем до старта
            current[0] = min_pos[0]
            current[1] = min_pos[1]
            # Переходим на его мето
            path.append(min_pos)
            # Добавляем его к маршруту
        result.put(path)
        # После восстановления пути отправляем его последним кадром интерфейсу


def BFS(result, map, start, end):
    # Волновой алгоритм

    start = {"i" : start[0],
             "j" : start[1],
             "d" : 0       }

    end = {"i" : end[0],
           "j" : end[1],
           "d" : 0     }

    map_size = [len(map), len(map[0])]

    visited = [0]*map_size[0]
    for i in range(0, map_size[0]):
        visited[i] = [0]*map_size[1]
    visited[start["i"]][start["j"]] = 1
    # создаем массив посещенных клеток размером с карту
    # изначально все клетки не посещены и раны 0
    # посещена только клетка старта

    nums = [0]*map_size[0]
    for i in range(0, map_size[0]):
        nums[i] = [0]*map_size[1]
    # массив, который хранит сколько шагов потребовалось чтобы достичь этой клетки

    result.put([deepcopy(visited), deepcopy(nums)])
    # Отправили начальное состояние интерфейсу

    frontier = deque()      # Создали список клеток на фронте. Очередь типа первый зашел - первый вышел
    frontier.append(start)  # Добавили туда старт

    d = 0 # изначальное количество шагов до клетки равно 0
    find_end = False # нашли ли конечную точку
    while frontier and not find_end:
    # пока на фронте есть клетки и не найдет конец
        d += 1 # увеличиваем счетчик шагов до клетки
        a = len(frontier)     # запоминаем протяженность фронта
        for c in range(0, a): # сколько клеток было на фронте на момент старта, столько и проверяем
            current = frontier.popleft() # достаем из фронта клетку
            if current["i"] == end["i"] and current["j"] == end["j"]: # если текущая = конечная
                end["d"] = current["d"] # кол-во шагов до нее равно кол-ву шагов до текущей клетки
                find_end = True         # конец нашли
                break # стоп машина

            neigbours = get_neigbours_cross(current["i"], current["j"], map_size)
            # просим соседей по плюсиком
            # нам дадут массив из пар строка столбец
            for i, j in neigbours: # для каждого такого соседа
                if map[i][j] == 0 or visited[i][j]:
                    # если по карте там ноль, т.е. препятствие или если мы уже были в этой клетке
                    continue # пропускаем ее
                frontier.append({"i" : i,
                                 "j" : j,
                                 "d" : d})
                                 # иначе добавляем ее к фронту, чтобы рассмотреть теперь уже ее соседей
                visited[i][j] = 1 # отмечаем как посещеную
                nums[i][j]    = d # записываем сколько шагов нужно чтобы дойти до нее
        result.put([deepcopy(visited), deepcopy(nums)])
        # отсылаем кадр интерфейсу

    result.put("endOfAlgorithm") # говорим интерфейсу об окончании работы

    if find_end:   # ищем путь если мы встретили конечную точку
        path = []  # массив координат клеток пути
        path.append([current["i"], current["j"]]) # добавляем конечную точку в путь и от нее стартуем
        d = current["d"]
        # кол-во шагов равно кол-ву шагов до текущей клетки.
        # мы будем выбирать тех соседей, до которых меньше всего шагать от старта
        while d != 0: # пока кол-во шагов до старта не равно 0, старт типа достигнут
            neigbours = get_neigbours_square(current["i"], current["j"], map_size)
            # Просим соседей по вертикли, горизонтали и по диагонали\
            # Функция нам набор пар строка столбец
            for i, j in neigbours: # для каждого соседа
                if nums[i][j] == d - 1 or nums[i][j] == d - 2:
                    # Если до него шагать на 1 или 2(в случае диагонали) шага меньше, то
                    path.append([i, j]) # добавляем его в путь
                    current["i"] = i
                    current["j"] = j
                    # становимся на его место
                    d = d - 1 if nums[i][j] == d - 1 else d - 2
                    # если он был меньше на 1, то уменьшаем d на 1, иначе на 2
                    break # если мы уже нашли нашу любовь, то остальных соседей не рассматрииваем
        result.put(path)  # Отправляем маршрут интерфейсу


def get_neigbours_square(i, j, map_size):
    # функция получения всех соседей
    neigbours  = get_neigbours_corners(i, j, map_size)
    # получить соседей по диагонали
    neigbours += get_neigbours_cross(i, j, map_size)
    # сложить с соседями по горизонтали и вертикали
    return neigbours
    # вернуть


def get_neigbours_corners(i, j, map_size):
    # функция получения соседей по диагонали
    neigbours = [] # массив соседей
    coords    = [] # тоже массив соседей, но он еще не прошел проверку что не выходит за пределы карты

    coords.append([i-1, j-1]) # добавить на проверку левого верхнего
    coords.append([i-1, j+1]) # правого верхнего
    coords.append([i+1, j-1]) # левого нижего
    coords.append([i+1, j+1]) # правого нижнего

    for i, j in coords: # для всех координат, что нужно проверить
        if 0 <= i < map_size[0]:        # строка в предела карты
            if 0 <= j < map_size[1]:    # и столбец тоже
                neigbours.append([i, j]) # добавляем к списку проверенных соедей

    return neigbours
    # возращаем соседей

def get_neigbours_cross(i, j, map_size):
    # возвращает соседей по вертикали и горизонтали
    neigbours = []
    coords = []

    coords.append([i  , j-1]) # левый
    coords.append([i+1, j  ]) # нижний
    coords.append([i  , j+1]) # правый
    coords.append([i-1, j  ]) # верхний

    for i, j in coords:
        if 0 <= i < map_size[0]:
            if 0 <= j < map_size[1]:
                neigbours.append([i, j]) #проверяем
    # отправляем
    return neigbours
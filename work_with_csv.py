import csv
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
import math
import numpy


def graph_log(file_name):
    """анализируем выбранный файл, находит первое значение приближенное к 0.5 после нормировки(индекс этого значения
     должен быть больше индекса самого большого значения), теперь спсиок x(градусы) и y(время) должны  начинаться
      с этого самого элемента, все элементы списка с x должны быть прологарифмированы.
     """
    try:
        y_greeds = []  # список для новых y
        x_time = []  # список для новых x
        log_time, log_greeds = evidence(file_name)
        assert log_time and log_greeds
        maxx = log_greeds.index(max(log_greeds))
        for indx, i in enumerate(log_greeds):
            if log_greeds.index(i) > maxx and (round(i, 1) == 0.5 or round(i, 1) == 0.4 or round(i, 1) == 0.6):
                y_greeds = log_greeds[indx:]
                x_time = log_time[indx:]
                break

        try:
            """если не получилось прологировать значит есть значения меньше нуля, идем в except и сужаем список 
            до значений больше нуля"""
            y_greeds = [math.log(j) for j in y_greeds]  # логирую все элементы списка
            return x_time, y_greeds
        except ValueError:
            y_greeds = list(sorted(y_greeds, reverse=True))
            x_time = list(sorted(x_time, reverse=True))
            for j in y_greeds:
                if j <= 0:
                    ed = y_greeds.index(j)
                    y_greeds = y_greeds[:ed]
                    x_time = x_time[:ed]
                    break
            return x_time, y_greeds
    except AssertionError:
        return False, False


def approximation(file_name):
    try:
        new_y = []
        x, y = graph_log(file_name)
        assert x, y
        x1 = graph_log(file_name)[0]
        x = numpy.array(x)
        y = numpy.array(y)
        reg = linear_model.LinearRegression()
        reg.fit(x.reshape(-1, 1), y)
        for i in x:
            """reg._coef[0] - Аx, reg.intercept_ - Bx,
             mean_absolute_error - погрешность получившегося графика"""
            new_y.append(i * reg.coef_[0] + reg.intercept_)

        return x1, new_y, reg.coef_[0], reg.intercept_, mean_absolute_error(y, new_y)

    except AssertionError:
        return False, False, False, False, False


def evidence(file_name):
    try:
        def str_with_e(what_list):
            """преоброзую строку с е в *10**,чтобы можно было воспользоваться eval()"""
            index_e = new_row[what_list].find('e')  # ищу е
            index_e += 2  # нахожу индекс нуля
            new_row[what_list] = new_row[what_list][:index_e] + new_row[what_list][
                                                                index_e + 1:]  # убираю этот ноль из строки
            return new_row[0]

        def normal_to(lst: list):
            """производит нормировку значений"""
            maximmum = max(lst)
            lst = [i / maximmum for i in lst]
            return lst

        number_of_row_in_file = -1
        time_list = []
        greeds = []

        with open(file_name) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                """прохожусь по двум столбцам и сортирую их данные по двум спискам"""
                number_of_row_in_file += 1
                if number_of_row_in_file > 4:  # в первых пяти строк нет нужных данных, опускаем эти строки
                    new_row = row[0].split(',')
                    if 'e' not in new_row[0]:
                        time_list.append(float(new_row[0]))
                    elif 'e' in new_row[0]:
                        time_list.append(eval(str_with_e(0)))
                    if 'e' not in new_row[1]:
                        greeds.append(float(new_row[1]))
                    elif 'e' in new_row[1]:
                        greeds.append(eval(str_with_e(1)))
        greeds = normal_to(greeds)

        return time_list, greeds
    except Exception:
        return False, False

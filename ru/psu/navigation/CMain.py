import traceback
import sys
from numpy import*
import time
import matplotlib.pyplot as plt
import pandas as pd


class CMain:

    def __init_plants__(self):
        self.plants = []
        # Щирина линии
        self.lineWidth = 20
        # Скорость
        self.speed = 5
        self.step_count = 1000
        # Значения углов.
        self.__init_angles__()

    # ***************************************************************************************************
    # Создание матрицы углов.                                                                           *
    # ***************************************************************************************************
    def __init_angles__(self):
        # Движение по окружности
        self.angles = [
            [315, 315, 270, 225, 225, 225, 225],
            [315, 290, 225, 180, 180, 180, 225],
            [315, 280, 190, 135, 110, 135, 160],
            [315, 270, 250,  45,  70,  90, 135],
            [340, 315, 300, 315,  45,  90, 135],
            [40,   15,   0,   0,  30,  90, 135],
            [45,   45,  45,  45,  80,  90, 135]
        ]
        # Окружность с выемкой.
        # self.angles = [
        #     [315, 315, 270, 225, 225, 225, 225],
        #     [315, 290, 225, 180, 180, 180, 225],
        #     [315, 280, 190,  80, 150, 225, 225],
        #     [315, 270, 250,  70, 135, 170, 180],
        #     [340, 315, 300, 315,  45,  90, 135],
        #     [40,   15,   0,   0,  30,  90, 135],
        #     [45,   45,  45,  45,  80,  90, 135]
        # ]

    # ***************************************************************************************************
    # Расчёт истинности высказываний о том, что координата х принадлежит линии с номером num.           *
    # @param x - координата для проверки.                                                               *
    # @param num - номер линии.                                                                         *
    # @return степень истинности.                                                                       *
    # ***************************************************************************************************
    def truth_func_location(self, x, num):
        if x <= (num-1)*self.lineWidth:
            return 0
        if x >= (num+1)*self.lineWidth:
            return 0
        if (num-1)*self.lineWidth < x <= num*self.lineWidth:
            return (x-(num-1)*self.lineWidth)/self.lineWidth
        return ((num+1)*self.lineWidth-x)/self.lineWidth

    # ***************************************************************************************************
    # Корректировка угла в зависимости от углов, которые уже есть в сумме.                              *
    # @param a - новый угол.                                                                            *
    # @param mid_angle - средний угол из тех, что уже обработали.                                       *
    # @return степень истинности.                                                                       *
    # ***************************************************************************************************
    @staticmethod
    def correct_angle(a, mid_angle):
        if a-mid_angle > 180:
            return a-360
        if mid_angle-a > 180:
            return a+360
        return a

    # ***************************************************************************************************
    # Нечёткий расчёт угла дальнейшего движения по текущим координатам x и y.                           *
    # @param x - текущая координата х.                                                                  *
    # @param y - текущая координата y.                                                                  *
    # @return угол дальнейшего движения относительно горизонтальной оси.                                *
    # ***************************************************************************************************
    def calculate_angle(self, x, y):

        numerator = 0
        denominator = 0
        mid_angle = 0
        count = 0
        # По всем строкам в матрице углов - ось Оу
        for i in range(7):
            # По всем столбцам в матрице углов - ось Оx
            for j in range(7):
                truth = self.truth_func_location(x, j-3)*self.truth_func_location(y, 3-i)

                if truth > 0:
                    # Сместить на 2PI при необходимости.
                    a = CMain.correct_angle(self.angles[i][j], mid_angle)

                    mid_angle = (mid_angle*count + a)/(count+1)
                    count += 1
                    numerator += truth*a
                    denominator += truth

        if denominator == 0:
            return 0

        return numerator/denominator

    # ***************************************************************************************************
    # Основной метод программы.                                                                         *
    # ***************************************************************************************************
    def main(self):
        self.__init_plants__()
        ti = time.clock()

        # Начальное расположение
        x = 0
        y = 0

        # Добавляем новые значения в массив для отрисовки.
        arr = [{'n': 0, 'x': x, 'y': y}]

        for k in range(self.step_count):
            # Новый угол поворота.
            a = self.calculate_angle(x, y)/180*pi
            # Новые координаты
            x = x + self.speed*cos(a)
            y = y + self.speed*sin(a)
            # Добавляем новые значения в массив для отрисовки.
            arr.append({'n': k+1, 'x': x, 'y': y})

        # Строим график с рассчитанными данными.
        df = pd.DataFrame(arr)
        # df = df.sort(['n'])  # dict doesn't preserve order
        df.plot(x='x', y='y', marker='.')
        plt.show()

        # print('Optimize root time', round(time.clock() - ti, 3), 'seconds')


try:
    main = CMain()
    main.main()
except Exception:
    print('Ошибка в программе.')
    # Подробности исключения через traceback
    traceback.print_exc(limit=2, file=sys.stdout)
finally:
    # Информируем о завершении работы программы
    print("Программа завершена.")
from math import *

eps = 1e-5  # eps необходимо поместить в одно место(второе в Ball.py)

# Для синтаксического сахара необходим конструктор, принимающий на вход два объекта класса Coordinate


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.abs = sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        # Следующие три строки исключают возможность деления на ноль
        distY = abs(self.y2 - self.y1)
        if distY < eps:
            distY = eps
        # Угол направления линии
        self.alphaTau = acos((self.x2 - self.x1) / self.abs) * (self.y2 - self.y1) / distY
        # Угол нормали к линии
        self.alphaNorm = self.alphaTau + (pi / 2)

    def crossLine(self, x0, y0, radius):
        # Проверка на пересечение шариком заданной линии
        h = self.distanceToLine(x0, y0)
        # Координаты точки на прямой этой линии до которой от центра шарика расстояние h
        xH = x0 + h * cos(pi - self.alphaNorm)
        yH = y0 - h * sin(pi - self.alphaNorm)
        if (h < radius) and self.isLine(xH, yH):
            return True
        else:
            return False

    def isLine(self, x0, y0):
        # Проверка точки на принадлежность линии прямоугольнику, в котором линия - диагональ
        return (((x0 - self.x2 < eps) and (self.x1 - x0 < eps)) or
                ((self.x2 - x0 < eps) and (x0 - self.x1 < eps))) \
               and (((y0 - self.y2 < eps) and (self.y1 - y0 < eps)) or
                    ((self.y2 - y0 < eps) and (y0 - self.y1 < eps)))

    def distanceToLine(self, x0, y0):
        # Определение расстояния от точки до линии(находится как высота треугольника)
        a = sqrt((self.x2 - x0) ** 2 + (self.y2 - y0) ** 2)
        b = sqrt((self.x1 - x0) ** 2 + (self.y1 - y0) ** 2)
        c = self.abs
        p = (a + b + c) / 2
        h = 2 * sqrt(p * (p - a) * (p - b) * (p - c)) / c
        return h

    def crossVerticalUp(self, x0, y0):
        # Проверка на пересечение линии и луча проведенного из этой точки вертикально вверх
        yH = self.y1 + (x0 - self.x1) * tan(self.alphaTau)
        temp = (((x0 - self.x2 < eps) and (self.x1 - x0 < eps)) or
                ((self.x2 - x0 < eps) and (x0 - self.x1 < eps))) and y0 - yH < eps
        return temp

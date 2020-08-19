from GlobalUtils import *


class Line:
    def __init__(self, coordinate1, coordinate2):
        self.currentX1 = coordinate1.x
        self.currentX2 = coordinate2.x
        self.currentY1 = coordinate1.y
        self.currentY2 = coordinate2.y
        self.startX1 = coordinate1.x
        self.startY1 = coordinate1.y
        self.startX2 = coordinate2.x
        self.startY2 = coordinate2.y
        self.abs = sqrt((self.startX2 - self.startX1) ** 2 + (self.startY2 - self.startY1) ** 2)
        # Следующие три строки исключают возможность деления на ноль
        distY = abs(self.startY2 - self.startY1)
        if distY < eps:
            distY = eps
        # Угол направления линии
        self.alphaTau = acos((self.startX2 - self.startX1) / self.abs) * (self.startY2 - self.startY1) / distY
        # Угол нормали к линии
        self.alphaNorm = self.alphaTau + (pi / 2)
        self.id = 0

    def setID(self, id):
        self.id = id

    def crossLine(self, x0, y0, radius):
        # Проверка на пересечение шариком заданной линии
        h = self.distanceToLine(x0, y0)
        # Координаты точки на прямой этой линии до которой от центра шарика расстояние h
        xH = x0 + h * cos(pi - self.alphaNorm)
        yH = y0 - h * sin(pi - self.alphaNorm)
        if (h < radius) and (self.isLine(xH, yH) or abs(self.currentX1 - self.currentX2) < eps or abs(self.currentY1 - self.currentY2) < eps):
            return True
        else:
            return False

    def isLine(self, x0, y0):
        # Проверка точки на принадлежность линии прямоугольнику, в котором линия - диагональ
        return (((x0 - self.currentX2 < eps) and (self.currentX1 - x0 < eps)) or
                ((self.currentX2 - x0 < eps) and (x0 - self.currentX1 < eps))) \
               and (((y0 - self.currentY2 < eps) and (self.currentY1 - y0 < eps)) or
                    ((self.currentY2 - y0 < eps) and (y0 - self.currentY1 < eps)))

    def distanceToLine(self, x0, y0):
        # Определение расстояния от точки до линии(находится как высота треугольника)
        a = sqrt((self.currentX2 - x0) ** 2 + (self.currentY2 - y0) ** 2)
        b = sqrt((self.currentX1 - x0) ** 2 + (self.currentY1 - y0) ** 2)
        c = self.abs
        p = (a + b + c) / 2
        h = 2 * sqrt(p * (p - a) * (p - b) * (p - c)) / c
        return h

    def crossVerticalUp(self, x0, y0):
        # Проверка на пересечение линии и луча проведенного из этой точки вертикально вверх
        yH = self.currentY1 + (x0 - self.currentX1) * tan(self.alphaTau)
        return y0 < yH and ((self.currentX1 <= x0 < self.currentX2) or (self.currentX2 <= x0 < self.currentX1))

    def setCoordinates(self, coordinate1, coordinate2):
        self.currentX1 = coordinate1.x
        self.currentX2 = coordinate2.x
        self.currentY1 = coordinate1.y
        self.currentY2 = coordinate2.y

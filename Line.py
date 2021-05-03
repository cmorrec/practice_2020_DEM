from GlobalUtils import *


# На данный момент класс не используется и является лишь родителем используемого
# класса MoveLine


class Line:
    def __init__(self, coordinate):
        self.x1 = coordinate.x1
        self.x2 = coordinate.x2
        self.y1 = coordinate.y1
        self.y2 = coordinate.y2
        print(self.x1, self.y1, self.x2, self.y2,)
        self.abs = self.findAbs()
        # Угол направления линии
        self.alphaTau = self.findTau()
        # Угол нормали к линии
        self.alphaNorm = self.alphaTau + (pi / 2)

    def crossLine(self, x0, y0, radius):
        # Проверка на пересечение шариком заданной линии
        h = self.distanceToLine(x0, y0)
        # Координаты точки на прямой этой линии до которой от центра шарика расстояние h
        xH = x0 + h * cos(pi - self.alphaNorm)
        yH = y0 - h * sin(pi - self.alphaNorm)
        xH2 = x0 + h * cos(pi - (-1) * self.alphaNorm)
        yH2 = y0 - h * sin(pi - (-1) * self.alphaNorm)
        if (h < radius) and (self.isLine(xH, yH) or self.isLine(xH2, yH2) or abs(self.x1 - self.x2) < eps or abs(
                self.y1 - self.y2) < eps):
            if self.x1 == .2:
                print("1")
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
        h = 2 * sqrt(abs(p * (p - a) * (p - b) * (p - c))) / c
        return h

    def crossVerticalUp(self, x0, y0):
        # Проверка на пересечение линии и луча проведенного из этой точки вертикально вверх
        yH = self.y1 + (x0 - self.x1) * tan(self.alphaTau)
        return y0 < yH and ((self.x1 <= x0 < self.x2) or (self.x2 <= x0 < self.x1))

    def findAbs(self):
        return sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

    def findTau(self):
        return atan2(self.y2 - self.y1, self.x2 - self.x1 + eps)

    def findNorm(self):
        return atan2(self.y2 - self.y1, self.x2 - self.x1 + eps) + (pi / 2)

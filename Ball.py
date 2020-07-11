from math import *
from Wall import *


class Ball:
    def __init__(self, x, y, canvas, color, radius, alpha, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocityAbsolute = velocity
        self.alphaRadian = alpha * pi / 180
        self.velocityX = velocity * cos(self.alphaRadian)
        self.velocityY = velocity * sin(self.alphaRadian)
        self.canvas = canvas
        self.id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        self.starts = False
        self.started = False
        self.canvas.bind_all('<KeyPress-s>', self.start)  # s - начало движения
        self.canvas.bind_all('<KeyPress-e>', self.exit)  # e - конец движения

    def start(self, event):
        self.started = True

    def exit(self, event):
        self.started = False

    def drawPolygon(self, wall):
        self.movePolygon(wall)  # фактическое движение
        self.canvas.move(self.id, self.velocityX, self.velocityY)  # прорисовка движения

    def movePolygon(self, wall):
        pos = self.canvas.coords(self.id)  # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        if self.crossPolygon(wall):
            self.resetPolygon(wall)
        elif not self.isInsidePolygon(wall):
            self.comeBack(wall)
        # Обновление направлений скоростей
        self.velocityX = self.velocityAbsolute * cos(self.alphaRadian)
        self.velocityY = self.velocityAbsolute * sin(self.alphaRadian)

    def crossPolygon(self, wall):
        # Проверяет пересечение как минимум с одной линией
        for line in wall.lines:
            if line.crossLine(self.x, self.y, self.radius):
                return True
        return False

    def resetPolygon(self, wall):
        # Находим линию, которую пересекает шарик и изменяем угол шарика по известной формуле:
        # alpha = 2 * beta - alpha
        for line in wall.lines:
            if line.crossLine(self.x, self.y, self.radius):
                # Проверка на то двигается ли мячик к линии или от нее
                # (во втором случае менять направление не нужно)
                if self.resetForLine(line, wall):
                    self.alphaRadian = 2 * line.alphaTau - self.alphaRadian
                    return

    def resetForLine(self, line, wall):
        # Проверяем расстояние сейчас и в следующий момент времени
        # (с учетом нахождения внутри стен)
        # Если сейчас расстояние больше - мячик двигается к стенке
        distNow = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon(wall):
            distNow *= -1

        self.x += self.velocityX
        self.y += self.velocityY
        distAfter = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon(wall):
            distAfter *= -1
        self.x -= self.velocityX
        self.y -= self.velocityY

        return distNow > distAfter

    def isInsidePolygon(self, wall):
        # Направляем луч из центра шарика вертикально вверх и считаем количество пересечений с линиями стенки
        # Если количество пересечений кратно двум, значит мяч вышел за границу стенки
        summary = 0
        for line in wall.lines:
            if line.crossVerticalUp(self.x, self.y):
                summary += 1
        if summary % 2 == 1:
            return True
        else:
            return False

    def comeBack(self, wall):
        # Возвращаем мяч в стенки в случае его выброса:
        # Находим линию к которой мячу будет логичнее всего стремиться
        # (меньше всего расстояние и перпендекуляр попадает в линию(в отрезок линии))
        # и меняем направление в соответсвие с этой линией
        eps = 1e-5  # eps необходимо поместить в одно место(второе в Line.py)
        distances = []
        for line in wall.lines:
            distances.append(line.distanceToLine(self.x, self.y))
        minDistance = min(distances)
        key = True

        while key:
            for line in wall.lines:
                if abs(line.distanceToLine(self.x, self.y) - minDistance) < eps:
                    h = line.distanceToLine(self.x, self.y)
                    xH = self.x + h * cos(pi - line.alphaNorm)
                    yH = self.y - h * sin(pi - line.alphaNorm)
                    if line.isLine(xH, yH) or len(distances) == 1:
                        key = False
                    else:
                        distances.remove(minDistance)
                        minDistance = min(distances)

        for line in wall.lines:
            if abs(line.distanceToLine(self.x, self.y) - minDistance) < eps:
                self.alphaRadian = 2 * line.alphaTau - self.alphaRadian
                return

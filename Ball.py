from MoveWall import *


# Для синтаксического сахара необходимо в конструкторе проверять на принадлежность стенке


class Ball:
    def __init__(self, x, y, radius, alpha, velocity, cn, cs, color, canvas):
        self.x = x
        self.y = y
        self.theta = 0
        self.mass = density * pi * radius ** 2
        # Коэффициент контактного демпфирования в нормальном направлении
        self.cn = cn
        # Коэффициент контактного демпфирования в тангенциальном направлении
        self.cs = cs
        self.radius = radius
        self.accelerationX = accelerationX
        self.accelerationY = accelerationY
        self.velocityAbsolute = velocity
        self.alphaRadian = alpha * pi / 180
        self.velocityX = velocity * cos(self.alphaRadian)
        self.velocityY = velocity * sin(self.alphaRadian)
        self.velocityTheta = 0
        self.canvas = canvas
        self.id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        self.id2 = canvas.create_line(x, y, x + radius * cos(self.theta), y + radius * sin(self.theta), width=2,
                                      fill="black")
        self.isCrossAnything = False

    def drawPolygon(self):
        self.movePolygon()  # фактическое движение
        self.canvas.move(self.id, self.velocityX, self.velocityY)  # прорисовка движения

    def rotationIndicator(self):
        self.theta += (self.velocityTheta * deltaTime) % (2 * pi)
        self.canvas.coords(self.id2, self.x, self.y, self.x + self.radius * cos(self.theta),
                           self.y + self.radius * sin(self.theta))
        self.canvas.move(self.id2, self.velocityX, self.velocityY)

    def movePolygon(self):
        pos = self.canvas.coords(self.id)  # овал задается по 4-м коордиатам по которым
        self.x = (pos[0] + pos[2]) / 2  # можно найти координаты центра
        self.y = (pos[1] + pos[3]) / 2

        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        if self.crossPolygon():
            self.resetPolygon()
        elif not self.isInsidePolygon():
            self.comeBack()
        # Обновление направлений скоростей
        self.velocityX = self.velocityAbsolute * cos(self.alphaRadian) + self.accelerationX
        self.velocityY = self.velocityAbsolute * sin(self.alphaRadian) + self.accelerationY
        self.changeVelocity(atan2(self.velocityY, self.velocityX + eps),
                            sqrt((self.velocityX ** 2) + (self.velocityY ** 2)))

    def crossPolygon(self):
        # Проверяет пересечение как минимум с одной линией
        for line in MoveWall.getInstance().lines:
            if line.crossLine(self.x, self.y, self.radius):
                return True
        return False

    def resetPolygon(self):
        # Находим линию, которую пересекает шарик и изменяем угол шарика по известной формуле:
        # alpha = 2 * beta - alpha
        wall = MoveWall.getInstance()
        for line in wall.lines:
            if line.crossLine(self.x, self.y, self.radius):
                # Проверка на то двигается ли мячик к линии или от нее
                # (во втором случае менять направление не нужно)
                if self.resetForLine(line):
                    self.alphaRadian = 2 * line.alphaTau - self.alphaRadian
                    alphaRadianLocal = self.alphaRadian - line.alphaNorm
                    velocityXLocal = self.velocityAbsolute * cos(alphaRadianLocal)
                    velocityYLocal = self.velocityAbsolute * sin(alphaRadianLocal)
                    velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
                    velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
                    velocityXLocal += velocityXLocalWall
                    velocityYLocal += velocityYLocalWall
                    dampeningNormal = velocityXLocal * cn_wall
                    dampeningTangent = velocityYLocal * cs_wall
                    self.velocityTheta += 1 / self.radius * (1 - cs_wall) * (
                            velocityYLocal - velocityYLocalWall - (self.velocityTheta * self.radius))
                    velocityXLocalNew = dampeningVelocity(dampeningNormal, velocityXLocal)
                    velocityYLocalNew = dampeningVelocity(dampeningTangent, velocityYLocal)
                    self.changeVelocity(atan2(velocityYLocalNew, velocityXLocalNew + eps) + line.alphaNorm,
                                        sqrt(velocityXLocalNew ** 2 + velocityYLocalNew ** 2))

    def resetForLine(self, line):
        # Проверяем расстояние сейчас и в следующий момент времени
        # (с учетом нахождения внутри стен)
        # Если сейчас расстояние больше - мячик двигается к стенке
        distNow = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon():
            distNow *= -1

        self.x += self.velocityX
        self.y += self.velocityY
        distAfter = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon():
            distAfter *= -1
        self.x -= self.velocityX
        self.y -= self.velocityY

        return distNow > distAfter

    def isInsidePolygon(self):
        # Направляем луч из центра шарика вертикально вверх и считаем количество пересечений с линиями стенки
        # Если количество пересечений кратно двум, значит мяч вышел за границу стенки
        summary = 0
        for line in MoveWall.getInstance().lines:
            if line.crossVerticalUp(self.x, self.y):
                summary += 1
        if summary % 2 == 1:
            return True
        else:
            return False

    def comeBack(self):
        # Возвращаем мяч в стенки в случае его выброса:
        # Находим линию к которой мячу будет логичнее всего стремиться
        # (меньше всего расстояние и перпендекуляр попадает в линию(в отрезок линии))
        # и меняем направление в соответсвии с этой линией
        distances = []
        for line in MoveWall.getInstance().lines:
            distances.append(line.distanceToLine(self.x, self.y))
        minDistance = min(distances)
        key = True

        while key:
            for line in MoveWall.getInstance().lines:
                if abs(line.distanceToLine(self.x, self.y) - minDistance) < eps:
                    h = line.distanceToLine(self.x, self.y)
                    xH = self.x + h * cos(pi - line.alphaNorm)
                    yH = self.y - h * sin(pi - line.alphaNorm)
                    if line.isLine(xH, yH) or len(distances) == 1:
                        key = False
                    else:
                        distances.remove(minDistance)
                        minDistance = min(distances)

        for line in MoveWall.getInstance().lines:
            if abs(line.distanceToLine(self.x, self.y) - minDistance) < eps:
                self.alphaRadian = 2 * line.alphaTau - self.alphaRadian
                return

    def changeVelocity(self, newAlpha, newVelocityAbsolute):
        # Изменение вектора скорости
        self.alphaRadian = newAlpha
        self.velocityAbsolute = newVelocityAbsolute
        self.velocityX = newVelocityAbsolute * cos(newAlpha)
        self.velocityY = newVelocityAbsolute * sin(newAlpha)

    def getAlpha(self):
        return self.alphaRadian * 180 / pi

    def getAcceleration(self):
        return self.velocityAbsolute / deltaTime

    def setAcceleration(self):
        if self.isCrossAnything:
            self.removeAcceleration()
        else:
            self.addAcceleration()

    def removeAcceleration(self):
        self.accelerationX = 0
        self.accelerationY = 0

    def addAcceleration(self):
        self.accelerationX = MoveWall.getInstance().accelerationX
        self.accelerationY = MoveWall.getInstance().accelerationY

    def methodWall(self, wall):
        # Решение задачи о нецентральном упругом ударе двух дисков, путём приведения к задаче о
        # столкновении шаров по оси Х(линия столкновения становится горизонтальной, происходит
        # переход в локальную систему координат)
        # Также учет диссипации при каждом столкновении шаров

        # Угол между линией удара и горизонталью
        gamma = atan2((i.y - j.y), (i.x - j.x))
        # Углы направления шаров в локальной системе координат
        alphaRadian1Local = i.alphaRadian - gamma
        alphaRadian2Local = j.alphaRadian - gamma
        # Скорости шаров в локальной системе координат
        velocity1XLocal = i.velocityAbsolute * cos(alphaRadian1Local)
        velocity1YLocal = i.velocityAbsolute * sin(alphaRadian1Local)
        velocity2XLocal = j.velocityAbsolute * cos(alphaRadian2Local)
        velocity2YLocal = j.velocityAbsolute * sin(alphaRadian2Local)

        # Непосредственно решение задачи о нецентральном упругом ударе двух дисков
        velocity1XLocalNew = ((i.mass - j.mass) * velocity1XLocal + 2 * j.mass * velocity2XLocal) / (i.mass + j.mass)
        velocity2XLocalNew = (2 * i.mass * velocity1XLocal + (j.mass - i.mass) * velocity2XLocal) / (i.mass + j.mass)
        # Демпфирование
        dampeningNormalI = (velocity1XLocalNew - velocity2XLocalNew) * i.cn
        dampeningNormalJ = (velocity2XLocalNew - velocity1XLocalNew) * j.cn
        dampeningTangentI = (velocity1YLocal - velocity2YLocal - (
                    i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * i.cs
        dampeningTangentJ = (velocity2YLocal - velocity1YLocal - (
                    i.velocityTheta * i.radius + j.velocityTheta * j.radius)) * j.cs
        # Учет демпфирования
        velocity1XLocalNew = dampeningVelocity(dampeningNormalI, velocity1XLocalNew)
        velocity2XLocalNew = dampeningVelocity(dampeningNormalJ, velocity2XLocalNew)
        velocity1YLocal = dampeningVelocity(dampeningTangentI, velocity1YLocal)
        velocity2YLocal = dampeningVelocity(dampeningTangentJ, velocity2YLocal)
        # Задание новой угловой скорости дисков
        rotation(i, j, velocity1YLocal, velocity2YLocal)
        # Возвращение к глобальной системе координат
        newAlphaI = atan2(velocity1YLocal, velocity1XLocalNew + eps) + gamma
        newAlphaJ = atan2(velocity2YLocal, velocity2XLocalNew + eps) + gamma
        newVelocityAbsoluteI = sqrt(velocity1XLocalNew ** 2 + velocity1YLocal ** 2)
        newVelocityAbsoluteJ = sqrt(velocity2XLocalNew ** 2 + velocity2YLocal ** 2)
        # Задание нового вектора скорости
        i.changeVelocity(newAlphaI, newVelocityAbsoluteI)
        j.changeVelocity(newAlphaJ, newVelocityAbsoluteJ)

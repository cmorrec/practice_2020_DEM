from MoveWall import *


# Для синтаксического сахара необходимо в конструкторе проверять на принадлежность стенке


class Ball:
    def __init__(self, x, y, radius, alpha, velocity, velocityTheta, cn, cs, density, Emod, nu, color, canvas):
        self.x = x
        self.y = y
        self.Emod = Emod
        self.nu = nu
        self.xLastDraw = x
        self.yLastDraw = y
        self.theta = 0
        self.radius = radius
        self.density = density
        self.mass = density * 4 / 3 * pi * radius ** 3
        self.momentInertial = 0.4 * self.mass * (self.radius ** 2)
        # Коэффициент контактного демпфирования в нормальном направлении
        self.cn = cn
        # Коэффициент контактного демпфирования в тангенциальном направлении
        self.cs = cs
        self.accelerationX = MoveWall.getInstance().accelerationX
        self.accelerationY = MoveWall.getInstance().accelerationY
        self.jerk = 0
        self.velocityAbsolute = velocity
        self.alphaRadian = alpha * pi / 180
        self.velocityX = velocity * cos(self.alphaRadian)
        self.velocityY = velocity * sin(self.alphaRadian)
        self.velocityTheta = velocityTheta
        self.accelerationTheta = 0
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_oval(displayRatio * (x - radius), displayRatio * (y - radius),
                                     displayRatio * (x + radius), displayRatio * (y + radius), fill=color)
        self.id2 = canvas.create_line(displayRatio * x, displayRatio * y, displayRatio * (x + radius * cos(self.theta)),
                                      displayRatio * (y + radius * sin(self.theta)), width=2, fill="black")
        self.isCrossAnything = False

    def canvasMove(self):
        self.canvas.move(self.id, displayRatio * (self.x - self.xLastDraw), displayRatio * (self.y - self.yLastDraw))

    def rotationIndicator(self):
        self.canvas.coords(self.id2, displayRatio * self.x, displayRatio * self.y,
                           displayRatio * (self.x + self.radius * cos(self.theta)),
                           displayRatio * (self.y + self.radius * sin(self.theta)))

    def draw(self):
        self.canvasMove()  # прорисовка движения
        self.rotationIndicator()
        self.xLastDraw = self.x
        self.yLastDraw = self.y

    def move(self):
        self.wallInteract()
        self.transfer()

    def wallInteract(self):
        # Смена направления происходит в двух случаях(для обоих разные последствия):
        #   - Пересечения мячом линии стенки
        #   - Выхода за границы стенки(скорость больше радиуса * 2)
        if self.crossPolygon():
            self.expand()
        elif not self.isInsidePolygon():
            self.comeBack()

    def transfer(self):
        # Обновление направлений скоростей
        self.addAccelerationInteractionMethod()
        self.x += self.velocityX * deltaTime + 0.5 * self.accelerationX * (deltaTime ** 2)
        self.y += self.velocityY * deltaTime + 0.5 * self.accelerationY * (deltaTime ** 2)
        self.theta = (self.theta + self.velocityTheta * deltaTime + 0.5 * self.accelerationTheta * (deltaTime ** 2)) % (
                    2 * pi)
        self.addVelocity(self.accelerationX, self.accelerationY, self.accelerationTheta)

    def addAccelerationInteractionMethod(self):
        pass

    def crossPolygon(self):
        # Проверяет пересечение как минимум с одной линией
        for line in MoveWall.getInstance().lines:
            if line.crossLine(self.x, self.y, self.radius):
                return True
        return False

    def expand(self):
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
                    if wall.flagMove:
                        velocityXLocalWall = wall.velocityAbsolute * cos(alphaRadianLocal)
                        velocityYLocalWall = wall.velocityAbsolute * sin(alphaRadianLocal)
                    else:
                        velocityXLocalWall = 0
                        velocityYLocalWall = 0
                    velocityXLocal += velocityXLocalWall
                    dampeningNormal = velocityXLocal * cn_wall
                    # dampeningTangent = (velocityYLocal - velocityYLocalWall) * cs_wall  # убрать скорость стенки

                    # self.rotationHerzWall(velocityYLocal, velocityYLocalWall, velocityXLocal, velocityXLocalWall)

                    velocityXLocalNew = dampeningVelocity(dampeningNormal, velocityXLocal)
                    # velocityYLocalNew = dampeningVelocity(dampeningTangent, velocityYLocal)

                    self.changeVelocity(atan2(velocityYLocal, velocityXLocalNew + eps) + line.alphaNorm,
                                        sqrt(velocityXLocalNew ** 2 + velocityYLocal ** 2))

    def resetForLine(self, line):
        # Проверяем расстояние сейчас и в следующий момент времени
        # (с учетом нахождения внутри стен)
        # Если сейчас расстояние больше - мячик двигается к стенке
        distNow = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon():
            distNow *= -1

        self.displace()
        distAfter = line.distanceToLine(self.x, self.y)
        if not self.isInsidePolygon():
            distAfter *= -1
        self.velocityX *= -1
        self.velocityY *= -1
        self.displace()
        self.velocityX *= -1
        self.velocityY *= -1

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

    def displace(self):
        self.x += self.velocityX * deltaTime
        self.y += self.velocityY * deltaTime

    def addVelocity(self, accelerationX, accelerationY, accelerationTheta):
        self.velocityX += accelerationX * deltaTime
        self.velocityY += accelerationY * deltaTime
        self.changeVelocity(atan2(self.velocityY, self.velocityX + eps),
                            sqrt((self.velocityX ** 2) + (self.velocityY ** 2)))
        self.velocityTheta += accelerationTheta * deltaTime
